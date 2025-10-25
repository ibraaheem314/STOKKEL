"""
Moteur d'optimisation des stocks pour Stokkel
Calcule les recommandations d'approvisionnement optimales
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging
from scipy import stats

from .config import settings
from .schemas import RecommendationResponse

logger = logging.getLogger(__name__)


class StockOptimizer:
    """Optimiseur de stock basé sur les prévisions probabilistes"""
    
    def __init__(self):
        pass
    
    def generate_recommendation(
        self,
        product_id: str,
        forecast_data: pd.DataFrame,
        current_stock: float,
        lead_time_days: int,
        service_level_percent: int
    ) -> RecommendationResponse:
        """
        Génère une recommandation d'approvisionnement optimale
        
        Args:
            product_id: Identifiant du produit
            forecast_data: DataFrame avec les prévisions (colonnes: date, p10, p50, p90)
            current_stock: Stock actuel en unités
            lead_time_days: Délai de livraison fournisseur en jours
            service_level_percent: Niveau de service cible (80-99%)
            
        Returns:
            RecommendationResponse avec l'action recommandée
        """
        try:
            logger.info(f"Génération de recommandation pour {product_id}")
            
            # Calcul de la demande moyenne journalière
            avg_daily_demand = forecast_data['p50'].mean()
            
            # Calcul de la variabilité (écart-type de la demande)
            demand_std = forecast_data['p50'].std()
            
            # Demande pendant le lead time (Lead Time Demand)
            lead_time_demand = avg_daily_demand * lead_time_days
            
            # Calcul du stock de sécurité dynamique
            safety_stock = self._calculate_safety_stock(
                avg_daily_demand=avg_daily_demand,
                demand_std=demand_std,
                lead_time_days=lead_time_days,
                service_level_percent=service_level_percent
            )
            
            # Point de commande (Reorder Point)
            reorder_point = lead_time_demand + safety_stock
            
            # Analyse du stock actuel
            stock_status, action = self._analyze_stock_status(
                current_stock=current_stock,
                reorder_point=reorder_point,
                safety_stock=safety_stock
            )
            
            # Calcul de la quantité à commander
            if action == "Commander":
                quantity_to_order = self._calculate_order_quantity(
                    current_stock=current_stock,
                    reorder_point=reorder_point,
                    avg_daily_demand=avg_daily_demand,
                    lead_time_days=lead_time_days,
                    safety_stock=safety_stock
                )
            else:
                quantity_to_order = 0.0
            
            # Estimation des jours avant rupture
            days_until_stockout = self._estimate_days_until_stockout(
                current_stock=current_stock,
                avg_daily_demand=avg_daily_demand
            )
            
            # Construction des métadonnées
            metadata = {
                'average_daily_demand': round(avg_daily_demand, 2),
                'demand_variability': round(demand_std, 2),
                'lead_time': lead_time_days,
                'service_level': f"{service_level_percent}%",
                'lead_time_demand': round(lead_time_demand, 2),
                'z_score': self._get_z_score(service_level_percent),
                'calculation_method': 'Dynamic Safety Stock with Service Level',
                'recommendation_rationale': self._get_recommendation_rationale(
                    action, current_stock, reorder_point, safety_stock
                )
            }
            
            # Construction de la réponse
            response = RecommendationResponse(
                product_id=product_id,
                recommendation_action=action,
                quantity_to_order=round(quantity_to_order, 2),
                reorder_point=round(reorder_point, 2),
                dynamic_safety_stock=round(safety_stock, 2),
                current_stock_status=stock_status,
                days_until_stockout=days_until_stockout if days_until_stockout else None,
                metadata=metadata
            )
            
            logger.info(f"Recommandation générée pour {product_id}: {action}")
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de recommandation: {str(e)}")
            raise
    
    def _calculate_safety_stock(
        self,
        avg_daily_demand: float,
        demand_std: float,
        lead_time_days: int,
        service_level_percent: int
    ) -> float:
        """
        Calcule le stock de sécurité dynamique
        
        Formule: SS = Z * σ_d * √(LT)
        où:
        - Z est le score Z correspondant au niveau de service
        - σ_d est l'écart-type de la demande journalière
        - LT est le lead time en jours
        
        Args:
            avg_daily_demand: Demande moyenne journalière
            demand_std: Écart-type de la demande
            lead_time_days: Délai de livraison en jours
            service_level_percent: Niveau de service cible (%)
            
        Returns:
            Stock de sécurité calculé
        """
        # Obtention du Z-score correspondant au niveau de service
        z_score = self._get_z_score(service_level_percent)
        
        # Calcul du stock de sécurité
        # Si la variabilité est faible, on utilise un pourcentage de la demande moyenne
        if demand_std < 0.1 * avg_daily_demand:
            # Faible variabilité: stock de sécurité = % de la demande lead time
            safety_stock = 0.15 * avg_daily_demand * lead_time_days
        else:
            # Variabilité normale: formule standard
            safety_stock = z_score * demand_std * np.sqrt(lead_time_days)
        
        # Le stock de sécurité doit être positif
        return max(0, safety_stock)
    
    def _get_z_score(self, service_level_percent: int) -> float:
        """
        Retourne le Z-score correspondant au niveau de service
        
        Args:
            service_level_percent: Niveau de service (80-99%)
            
        Returns:
            Z-score de la distribution normale
        """
        # Conversion en probabilité (0-1)
        probability = service_level_percent / 100.0
        
        # Calcul du Z-score (quantile de la loi normale standard)
        z_score = stats.norm.ppf(probability)
        
        return z_score
    
    def _analyze_stock_status(
        self,
        current_stock: float,
        reorder_point: float,
        safety_stock: float
    ) -> Tuple[str, str]:
        """
        Analyse le statut du stock actuel
        
        Args:
            current_stock: Stock actuel
            reorder_point: Point de commande calculé
            safety_stock: Stock de sécurité
            
        Returns:
            Tuple (status_description, action_recommended)
        """
        if current_stock <= safety_stock:
            status = "🔴 Critique - En dessous du stock de sécurité"
            action = "Commander"
        elif current_stock <= reorder_point:
            status = "🟡 Attention - En dessous du point de commande"
            action = "Commander"
        elif current_stock <= reorder_point * 1.5:
            status = "🟢 Normal - Stock suffisant"
            action = "Surveiller"
        else:
            status = "🟢 Bon - Stock confortable"
            action = "Stock suffisant"
        
        return status, action
    
    def _calculate_order_quantity(
        self,
        current_stock: float,
        reorder_point: float,
        avg_daily_demand: float,
        lead_time_days: int,
        safety_stock: float
    ) -> float:
        """
        Calcule la quantité optimale à commander
        
        Stratégie: Commander pour couvrir le lead time + cycle time
        
        Args:
            current_stock: Stock actuel
            reorder_point: Point de commande
            avg_daily_demand: Demande moyenne journalière
            lead_time_days: Délai de livraison
            safety_stock: Stock de sécurité
            
        Returns:
            Quantité à commander
        """
        # Période de couverture cible (lead time + période de réapprovisionnement)
        # On vise à couvrir 2x le lead time pour éviter les commandes trop fréquentes
        review_period_days = max(14, lead_time_days * 2)
        
        # Stock cible pour la période de couverture
        target_stock = (avg_daily_demand * review_period_days) + safety_stock
        
        # Quantité à commander = Stock cible - Stock actuel
        order_quantity = target_stock - current_stock
        
        # Minimum de commande: au moins couvrir le lead time
        min_order = avg_daily_demand * lead_time_days
        
        # La quantité ne peut pas être négative
        order_quantity = max(0, order_quantity, min_order)
        
        return order_quantity
    
    def _estimate_days_until_stockout(
        self,
        current_stock: float,
        avg_daily_demand: float
    ) -> Optional[int]:
        """
        Estime le nombre de jours avant rupture de stock
        
        Args:
            current_stock: Stock actuel
            avg_daily_demand: Demande moyenne journalière
            
        Returns:
            Nombre de jours ou None si stock confortable
        """
        if avg_daily_demand <= 0:
            return None
        
        days = int(current_stock / avg_daily_demand)
        
        # Retourner seulement si risque dans les 30 prochains jours
        if days <= 30:
            return days
        
        return None
    
    def _get_recommendation_rationale(
        self,
        action: str,
        current_stock: float,
        reorder_point: float,
        safety_stock: float
    ) -> str:
        """
        Génère une explication de la recommandation
        
        Args:
            action: Action recommandée
            current_stock: Stock actuel
            reorder_point: Point de commande
            safety_stock: Stock de sécurité
            
        Returns:
            Texte explicatif
        """
        if action == "Commander":
            if current_stock <= safety_stock:
                return (
                    f"Stock actuel ({current_stock:.0f}) en dessous du stock de sécurité "
                    f"({safety_stock:.0f}). Commande urgente recommandée pour éviter la rupture."
                )
            else:
                return (
                    f"Stock actuel ({current_stock:.0f}) en dessous du point de commande "
                    f"({reorder_point:.0f}). Commande recommandée pour maintenir le niveau de service."
                )
        elif action == "Surveiller":
            return (
                f"Stock actuel ({current_stock:.0f}) proche du point de commande "
                f"({reorder_point:.0f}). Surveillance recommandée."
            )
        else:
            return (
                f"Stock actuel ({current_stock:.0f}) confortable au-dessus du point de commande "
                f"({reorder_point:.0f}). Aucune action nécessaire."
            )
    
    def calculate_batch_recommendations(
        self,
        products_forecasts: Dict[str, pd.DataFrame],
        stock_levels: Optional[Dict[str, float]],
        lead_time_days: int,
        service_level_percent: int
    ) -> Dict:
        """
        Calcule les recommandations pour plusieurs produits
        
        Args:
            products_forecasts: Dict {product_id: forecast_dataframe}
            stock_levels: Dict {product_id: current_stock} ou None
            lead_time_days: Délai de livraison
            service_level_percent: Niveau de service
            
        Returns:
            Dict avec les recommandations et statistiques
        """
        recommendations = []
        
        for product_id, forecast_df in products_forecasts.items():
            # Stock par défaut si non fourni
            current_stock = 0.0
            if stock_levels and product_id in stock_levels:
                current_stock = stock_levels[product_id]
            
            try:
                recommendation = self.generate_recommendation(
                    product_id=product_id,
                    forecast_data=forecast_df,
                    current_stock=current_stock,
                    lead_time_days=lead_time_days,
                    service_level_percent=service_level_percent
                )
                recommendations.append(recommendation)
            except Exception as e:
                logger.error(f"Erreur pour {product_id}: {str(e)}")
                continue
        
        # Statistiques agrégées
        to_order = [r for r in recommendations if r.recommendation_action == "Commander"]
        
        summary = {
            'total_products': len(recommendations),
            'products_to_order': len(to_order),
            'total_quantity_to_order': sum(r.quantity_to_order for r in to_order),
            'total_safety_stock': sum(r.dynamic_safety_stock for r in recommendations),
            'average_service_level': f"{service_level_percent}%"
        }
        
        return {
            'recommendations': recommendations,
            'summary': summary
        }


# Instance globale de l'optimiseur
stock_optimizer = StockOptimizer()