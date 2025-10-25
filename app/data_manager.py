"""
Gestionnaire de données pour Stokkel
Gère le stockage et la récupération des données de ventes
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from pathlib import Path
import json

from .config import settings
from .validators import DataValidator, ValidationError

logger = logging.getLogger(__name__)


class DataManager:
    """Gestionnaire centralisé des données de ventes"""
    
    def __init__(self):
        self.data_dir = Path(settings.data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.sales_data: Optional[pd.DataFrame] = None
        self.products_cache: Dict = {}
    
    def _detect_column_mapping(self, df: pd.DataFrame) -> dict:
        """Détecte automatiquement le mapping des colonnes"""
        mapping = {}
        
        # Mapping des colonnes communes
        column_mappings = {
            'product_id': ['reference_article', 'product_id', 'id', 'ref', 'reference'],
            'date': ['date_vente', 'date', 'date_vente', 'timestamp', 'created_at'],
            'quantity': ['quantite_vendue', 'quantity', 'qty', 'amount', 'volume']
        }
        
        for target_col, possible_cols in column_mappings.items():
            for col in df.columns:
                if col.lower() in [c.lower() for c in possible_cols]:
                    mapping[col] = target_col
                    break
        
        return mapping
        
    def load_sales_data(self, filepath: str) -> Dict:
        """
        Charge les données de ventes depuis un fichier CSV
        
        Args:
            filepath: Chemin vers le fichier CSV
            
        Returns:
            Dict avec les statistiques de chargement
        """
        try:
            # Lecture du CSV
            df = pd.read_csv(filepath)
            
            # Détection automatique du mapping des colonnes
            column_mapping = self._detect_column_mapping(df)
            
            # Application du mapping si détecté
            if column_mapping:
                logger.info(f"🔄 Mapping automatique détecté: {column_mapping}")
                df = df.rename(columns=column_mapping)
            
            # Validation des colonnes requises
            required_cols = ['product_id', 'date', 'quantity']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                raise ValueError(f"Colonnes manquantes: {missing_cols}")
            
            # Validation centralisée
            is_valid, error_msg = DataValidator.validate_sales_dataframe(df)
            if not is_valid:
                raise ValidationError(error_msg)
            
            # Conversion et nettoyage
            df['date'] = pd.to_datetime(df['date'])
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
            
            # Suppression des valeurs invalides
            df = df.dropna(subset=['product_id', 'date', 'quantity'])
            df = df[df['quantity'] >= 0]  # Pas de quantités négatives
            
            # Tri par date
            df = df.sort_values(['product_id', 'date'])
            
            # Stockage
            self.sales_data = df
            self._update_products_cache()
            
            # Sauvegarde locale
            self._save_data()
            
            # Statistiques
            stats = {
                'message': 'Données chargées avec succès',
                'products_count': df['product_id'].nunique(),
                'total_records': len(df),
                'date_range': {
                    'start': df['date'].min().strftime('%Y-%m-%d'),
                    'end': df['date'].max().strftime('%Y-%m-%d')
                }
            }
            
            logger.info(f"Données chargées: {stats['products_count']} produits, "
                       f"{stats['total_records']} enregistrements")
            
            return stats
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {str(e)}")
            raise
    
    def get_product_data(self, product_id: str) -> pd.DataFrame:
        """
        Récupère les données d'un produit spécifique
        
        Args:
            product_id: Identifiant du produit
            
        Returns:
            DataFrame avec les données du produit
        """
        if self.sales_data is None:
            raise ValueError("Aucune donnée chargée")
        
        product_data = self.sales_data[
            self.sales_data['product_id'] == product_id
        ].copy()
        
        if product_data.empty:
            raise ValueError(f"Produit {product_id} non trouvé")
        
        return product_data.sort_values('date')
    
    def get_all_products(self) -> List[Dict]:
        """
        Récupère la liste de tous les produits avec leurs métadonnées
        
        Returns:
            Liste de dictionnaires contenant les infos produits
        """
        if self.sales_data is None:
            return []
        
        products_info = []
        
        for product_id in self.sales_data['product_id'].unique():
            product_data = self.get_product_data(product_id)
            
            info = {
                'product_id': product_id,
                'data_points': len(product_data),
                'date_range_start': product_data['date'].min().strftime('%Y-%m-%d'),
                'date_range_end': product_data['date'].max().strftime('%Y-%m-%d'),
                'average_daily_sales': float(product_data['quantity'].mean()),
                'total_sales': float(product_data['quantity'].sum()),
                'std_dev': float(product_data['quantity'].std())
            }
            
            products_info.append(info)
        
        return products_info
    
    def get_product_statistics(self, product_id: str) -> Dict:
        """
        Calcule les statistiques détaillées d'un produit
        
        Args:
            product_id: Identifiant du produit
            
        Returns:
            Dict avec les statistiques
        """
        product_data = self.get_product_data(product_id)
        
        stats = {
            'product_id': product_id,
            'total_observations': len(product_data),
            'date_range': {
                'start': product_data['date'].min(),
                'end': product_data['date'].max(),
                'days': (product_data['date'].max() - product_data['date'].min()).days
            },
            'sales': {
                'mean': float(product_data['quantity'].mean()),
                'median': float(product_data['quantity'].median()),
                'std': float(product_data['quantity'].std()),
                'min': float(product_data['quantity'].min()),
                'max': float(product_data['quantity'].max()),
                'total': float(product_data['quantity'].sum())
            },
            'variability': {
                'coefficient_of_variation': float(
                    product_data['quantity'].std() / product_data['quantity'].mean()
                ) if product_data['quantity'].mean() > 0 else 0,
                'iqr': float(
                    product_data['quantity'].quantile(0.75) - 
                    product_data['quantity'].quantile(0.25)
                )
            }
        }
        
        return stats
    
    def prepare_forecast_data(self, product_id: str) -> pd.DataFrame:
        """
        Prépare les données pour le forecasting (format Prophet/SARIMA)
        
        Args:
            product_id: Identifiant du produit
            
        Returns:
            DataFrame formaté pour Prophet (colonnes: ds, y)
        """
        product_data = self.get_product_data(product_id)
        
        # Agrégation journalière (au cas où il y aurait plusieurs entrées par jour)
        daily_data = product_data.groupby('date')['quantity'].sum().reset_index()
        
        # Format Prophet
        forecast_df = pd.DataFrame({
            'ds': daily_data['date'],
            'y': daily_data['quantity']
        })
        
        return forecast_df
    
    def _update_products_cache(self):
        """Met à jour le cache des produits"""
        if self.sales_data is not None:
            self.products_cache = {
                product_id: self.get_product_statistics(product_id)
                for product_id in self.sales_data['product_id'].unique()
            }
    
    def _save_data(self):
        """Sauvegarde les données localement"""
        try:
            if self.sales_data is not None:
                filepath = self.data_dir / "sales_data.csv"
                self.sales_data.to_csv(filepath, index=False)
                
                # Sauvegarde du cache
                cache_filepath = self.data_dir / "products_cache.json"
                with open(cache_filepath, 'w') as f:
                    # Conversion des Timestamps en strings pour JSON
                    cache_serializable = {}
                    for k, v in self.products_cache.items():
                        cache_copy = v.copy()
                        if 'date_range' in cache_copy:
                            cache_copy['date_range'] = {
                                kk: vv.strftime('%Y-%m-%d') if isinstance(vv, datetime) else vv
                                for kk, vv in cache_copy['date_range'].items()
                            }
                        cache_serializable[k] = cache_copy
                    
                    json.dump(cache_serializable, f, indent=2)
                
                logger.info(f"Données sauvegardées: {filepath}")
        except Exception as e:
            logger.warning(f"Erreur lors de la sauvegarde: {str(e)}")
    
    def load_saved_data(self):
        """Charge les données sauvegardées localement"""
        try:
            filepath = self.data_dir / "sales_data.csv"
            if filepath.exists():
                self.sales_data = pd.read_csv(filepath)
                self.sales_data['date'] = pd.to_datetime(self.sales_data['date'])
                
                # Chargement du cache
                cache_filepath = self.data_dir / "products_cache.json"
                if cache_filepath.exists():
                    with open(cache_filepath, 'r') as f:
                        self.products_cache = json.load(f)
                else:
                    self._update_products_cache()
                
                logger.info(f"Données chargées depuis: {filepath}")
                return True
        except Exception as e:
            logger.warning(f"Impossible de charger les données sauvegardées: {str(e)}")
        
        return False
    
    def has_data(self) -> bool:
        """Vérifie si des données sont chargées"""
        return self.sales_data is not None and not self.sales_data.empty
    
    def validate_product(self, product_id: str) -> Tuple[bool, str]:
        """
        Valide qu'un produit a suffisamment de données pour la prévision
        
        Args:
            product_id: Identifiant du produit
            
        Returns:
            Tuple (is_valid, message)
        """
        try:
            product_data = self.get_product_data(product_id)
            
            if len(product_data) < settings.min_data_points:
                return False, f"Données insuffisantes (minimum {settings.min_data_points} points requis)"
            
            # Vérifier qu'il n'y a pas que des zéros
            if product_data['quantity'].sum() == 0:
                return False, "Toutes les ventes sont à zéro"
            
            return True, "Validation réussie"
            
        except Exception as e:
            return False, str(e)


# Instance globale du gestionnaire de données
data_manager = DataManager()