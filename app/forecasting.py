"""
Moteur de prévision des ventes pour Stokkel
Implémente les modèles de forecasting (Prophet, SARIMA)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from pathlib import Path
from threading import Lock

from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
import warnings
warnings.filterwarnings('ignore')

from fastapi import HTTPException, status

from .config import settings
from .schemas import ForecastPoint
from .validators import DataValidator, ValidationError
from .cache import cache

# Exceptions personnalisées
class ForecastError(Exception):
    """Exception personnalisée pour les erreurs de prévision"""
    pass

class InsufficientDataError(ForecastError):
    """Données insuffisantes"""
    pass

logger = logging.getLogger(__name__)


class ForecastEngine:
    """Moteur de prévision thread-safe utilisant Prophet pour les prévisions probabilistes"""
    
    def __init__(self):
        self.models_dir = Path(settings.models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Cache thread-safe
        self.trained_models: Dict[str, Prophet] = {}
        self._cache_locks: Dict[str, Lock] = {}  # Lock par produit
        self._global_lock = Lock()  # Lock pour gérer les locks eux-mêmes
    
    def _get_lock(self, product_id: str) -> Lock:
        """Obtient ou crée un lock pour un produit"""
        with self._global_lock:
            if product_id not in self._cache_locks:
                self._cache_locks[product_id] = Lock()
            return self._cache_locks[product_id]
        
    def generate_forecast(
        self,
        product_id: str,
        historical_data: pd.DataFrame,
        horizon_days: int = 30
    ) -> Tuple[List[ForecastPoint], Dict]:
        """
        Génère une prévision probabiliste pour un produit
        
        Args:
            product_id: Identifiant du produit
            historical_data: DataFrame avec colonnes 'ds' (date) et 'y' (quantité)
            horizon_days: Nombre de jours à prévoir
            
        Returns:
            Tuple (liste de ForecastPoint, metadata dict)
        """
        try:
            logger.info(f"Generation prevision | product={product_id} horizon={horizon_days}j")
            
            # Validation des paramètres
            DataValidator.validate_forecast_params(horizon_days, settings.max_forecast_horizon)
            
            # Validation des données
            is_valid, error_msg = DataValidator.validate_product_data(
                historical_data, product_id, settings.min_data_points
            )
            if not is_valid:
                raise InsufficientDataError(error_msg)
            
            # Vérifier les valeurs nulles
            if historical_data['y'].isna().any():
                logger.warning(f"⚠️ Valeurs manquantes détectées pour {product_id}, nettoyage...")
                historical_data = historical_data.dropna(subset=['y'])
            
            # Vérifier que toutes les valeurs ne sont pas nulles
            if historical_data['y'].sum() == 0:
                raise ForecastError(
                    f"Produit {product_id}: toutes les ventes sont à zéro. "
                    f"Impossible de générer une prévision significative."
                )
            
            # Entraînement ou chargement du modèle
            model = self._get_or_train_model(product_id, historical_data)
            
            # Création du dataframe de dates futures
            future = model.make_future_dataframe(periods=horizon_days, freq='D')
            
            # Génération des prévisions
            forecast = model.predict(future)
            
            # Extraction des prévisions futures uniquement
            future_forecast = forecast.tail(horizon_days)
            
            # Construction des ForecastPoints avec quantiles
            forecast_points = []
            for _, row in future_forecast.iterrows():
                # Prophet fournit yhat_lower et yhat_upper pour l'intervalle de confiance
                # On calcule les quantiles approximatifs
                yhat = max(0, row['yhat'])  # Pas de prévisions négatives
                yhat_lower = max(0, row['yhat_lower'])
                yhat_upper = max(0, row['yhat_upper'])
                
                # Approximation des quantiles
                # P10 ≈ valeur basse de l'intervalle
                # P50 = médiane (yhat)
                # P90 ≈ valeur haute de l'intervalle
                point = ForecastPoint(
                    date=row['ds'].date(),  # Convertir en date object
                    p10=round(yhat_lower, 2),
                    p50=round(yhat, 2),
                    p90=round(yhat_upper, 2)
                )
                forecast_points.append(point)
            
            # Métriques de qualité
            metadata = self._calculate_forecast_metadata(
                model, historical_data, forecast, product_id
            )
            
            logger.info(f"Prévision générée avec succès pour {product_id}")
            
            return forecast_points, metadata
            
        except InsufficientDataError as e:
            # Erreur utilisateur: données insuffisantes
            logger.warning(str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Données insuffisantes",
                    "message": str(e),
                    "product_id": product_id,
                    "data_points": len(historical_data),
                    "required": settings.min_data_points
                }
            )
        
        except ForecastError as e:
            # Erreur métier
            logger.error(str(e))
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "Impossible de générer la prévision",
                    "message": str(e),
                    "product_id": product_id
                }
            )
        
        except Exception as e:
            # Erreur technique inattendue
            logger.error(f"❌ Erreur technique pour {product_id}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Erreur interne du serveur",
                    "message": "Une erreur technique est survenue. Veuillez réessayer.",
                    "product_id": product_id,
                    "support": "Contactez le support si le problème persiste"
                }
            )
    
    def _get_or_train_model(self, product_id: str, data: pd.DataFrame) -> Prophet:
        """
        Récupère un modèle entraîné du cache ou en entraîne un nouveau (thread-safe)
        
        Args:
            product_id: Identifiant du produit
            data: Données d'entraînement
            
        Returns:
            Modèle Prophet entraîné
        """
        # Vérification rapide sans lock
        if product_id in self.trained_models:
            logger.info(f"✅ Modèle en cache pour {product_id}")
            return self.trained_models[product_id]
        
        # Vérifier le cache Redis
        cache_key = f"model:{product_id}"
        cached_model = cache.get(cache_key)
        if cached_model:
            logger.info(f"🔴 Modèle depuis Redis pour {product_id}")
            self.trained_models[product_id] = cached_model
            return cached_model
        
        # Obtenir le lock spécifique au produit
        product_lock = self._get_lock(product_id)
        
        with product_lock:
            # Double-check après avoir acquis le lock
            if product_id in self.trained_models:
                logger.info(f"✅ Modèle en cache (double-check) pour {product_id}")
                return self.trained_models[product_id]
            
            # Vérifier si un modèle sauvegardé existe
            model_path = self.models_dir / f"{product_id}_model.json"
            if model_path.exists():
                try:
                    with open(model_path, 'r') as f:
                        model = model_from_json(f.read())
                    self.trained_models[product_id] = model
                    logger.info(f"📂 Modèle chargé depuis {model_path}")
                    return model
                except Exception as e:
                    logger.warning(f"⚠️ Impossible de charger {model_path}: {e}")
            
            # Entraîner un nouveau modèle
            logger.info(f"🔄 Entraînement d'un nouveau modèle pour {product_id}")
            model = self._train_new_model(product_id, data)
            
            # Sauvegarder dans le cache local
            self.trained_models[product_id] = model
            
            # Sauvegarder dans le cache Redis (TTL 1 heure)
            cache.set(cache_key, model, ttl=settings.cache_ttl_seconds)
            logger.info(f"🔴 Modèle sauvegardé dans Redis pour {product_id}")
            
            return model
    
    def clear_cache(self, product_id: Optional[str] = None):
        """Nettoie le cache de manière thread-safe"""
        if product_id:
            product_lock = self._get_lock(product_id)
            with product_lock:
                if product_id in self.trained_models:
                    del self.trained_models[product_id]
                # Nettoyer aussi le cache Redis
                cache_key = f"model:{product_id}"
                cache.delete(cache_key)
                logger.info(f"🗑️ Cache nettoyé pour {product_id}")
        else:
            with self._global_lock:
                self.trained_models.clear()
                # Nettoyer tout le cache Redis
                cache.clear()
                logger.info("🗑️ Cache complet nettoyé")
    
    def _train_new_model(self, product_id: str, data: pd.DataFrame) -> Prophet:
        """
        Entraîne un nouveau modèle Prophet
        
        Args:
            product_id: Identifiant du produit
            data: Données d'entraînement (colonnes ds, y)
            
        Returns:
            Modèle Prophet entraîné
        """
        logger.info(f"Entraînement d'un nouveau modèle pour {product_id}")
        
        # Configuration du modèle Prophet
        model = Prophet(
            interval_width=settings.prophet_interval_width,
            changepoint_prior_scale=settings.prophet_changepoint_prior_scale,
            seasonality_prior_scale=settings.prophet_seasonality_prior_scale,
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality='auto',
            seasonality_mode='multiplicative'  # Meilleur pour les ventes
        )
        
        # Entraînement
        model.fit(data)
        
        # Sauvegarde du modèle
        self._save_model(product_id, model)
        
        # Cache
        self.trained_models[product_id] = model
        
        logger.info(f"Modèle entraîné et sauvegardé pour {product_id}")
        
        return model
    
    def _save_model(self, product_id: str, model: Prophet):
        """Sauvegarde un modèle Prophet"""
        try:
            model_path = self.models_dir / f"{product_id}_model.json"
            with open(model_path, 'w') as f:
                f.write(model_to_json(model))
            logger.info(f"Modèle sauvegardé: {model_path}")
        except Exception as e:
            logger.warning(f"Impossible de sauvegarder le modèle: {str(e)}")
    
    def _calculate_forecast_metadata(
        self,
        model: Prophet,
        historical_data: pd.DataFrame,
        forecast: pd.DataFrame,
        product_id: str
    ) -> Dict:
        """
        Calcule les métadonnées et métriques de qualité de la prévision
        
        Args:
            model: Modèle Prophet utilisé
            historical_data: Données historiques
            forecast: Prévisions générées
            product_id: Identifiant du produit
            
        Returns:
            Dict contenant les métadonnées
        """
        # Calcul du MAPE (Mean Absolute Percentage Error) sur l'historique
        historical_forecast = forecast[forecast['ds'].isin(historical_data['ds'])]
        
        if len(historical_forecast) > 0:
            actual = historical_data.set_index('ds')['y']
            predicted = historical_forecast.set_index('ds')['yhat']
            
            # Alignement des données
            common_dates = actual.index.intersection(predicted.index)
            actual_aligned = actual[common_dates]
            predicted_aligned = predicted[common_dates]
            
            # Calcul du MAPE (en évitant la division par zéro)
            mask = actual_aligned != 0
            if mask.sum() > 0:
                mape = np.mean(
                    np.abs((actual_aligned[mask] - predicted_aligned[mask]) / actual_aligned[mask])
                ) * 100
            else:
                mape = None
            
            # Calcul du MAE (Mean Absolute Error)
            mae = np.mean(np.abs(actual_aligned - predicted_aligned))
            
            # Calcul du RMSE (Root Mean Squared Error)
            rmse = np.sqrt(np.mean((actual_aligned - predicted_aligned) ** 2))
        else:
            mape, mae, rmse = None, None, None
        
        # Statistiques de base
        avg_demand = historical_data['y'].mean()
        std_demand = historical_data['y'].std()
        
        metadata = {
            'model_used': 'Prophet',
            'training_data_points': len(historical_data),
            'training_period': {
                'start': historical_data['ds'].min().strftime('%Y-%m-%d'),
                'end': historical_data['ds'].max().strftime('%Y-%m-%d')
            },
            'average_daily_demand': round(avg_demand, 2),
            'demand_std_dev': round(std_demand, 2),
            'coefficient_of_variation': round(std_demand / avg_demand, 3) if avg_demand > 0 else None,
            'confidence_level': f"{int(settings.prophet_interval_width * 100)}%",
            'quality_metrics': {
                'mape': round(mape, 2) if mape is not None else 'N/A',
                'mae': round(mae, 2) if mae is not None else 'N/A',
                'rmse': round(rmse, 2) if rmse is not None else 'N/A'
            },
            'forecast_generated_at': datetime.now().isoformat()
        }
        
        return metadata
    
    def clear_cache(self, product_id: Optional[str] = None):
        """
        Nettoie le cache des modèles
        
        Args:
            product_id: Si spécifié, nettoie seulement ce produit, sinon tous
        """
        if product_id:
            if product_id in self.trained_models:
                del self.trained_models[product_id]
                logger.info(f"Cache nettoyé pour {product_id}")
        else:
            self.trained_models.clear()
            logger.info("Cache complet nettoyé")


# Instance globale du moteur de prévision
forecast_engine = ForecastEngine()