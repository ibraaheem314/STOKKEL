"""
Validators centralisés pour toutes les données
"""

from typing import Optional, Tuple
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Erreur de validation"""
    pass

class DataValidator:
    """Validateur de données centralisé"""
    
    @staticmethod
    def validate_sales_dataframe(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """
        Valide un DataFrame de ventes
        
        Returns:
            (is_valid, error_message)
        """
        required_columns = ['product_id', 'date', 'quantity']
        
        # Vérifier les colonnes
        missing = set(required_columns) - set(df.columns)
        if missing:
            return False, f"Colonnes manquantes: {', '.join(missing)}"
        
        # Vérifier les types
        if not pd.api.types.is_numeric_dtype(df['quantity']):
            return False, "La colonne 'quantity' doit contenir des nombres"
        
        # Vérifier les valeurs négatives
        if (df['quantity'] < 0).any():
            return False, "La colonne 'quantity' ne peut pas contenir de valeurs négatives"
        
        # Vérifier les dates
        try:
            pd.to_datetime(df['date'])
        except Exception:
            return False, "Format de date invalide dans la colonne 'date'"
        
        # Vérifier que le DataFrame n'est pas vide
        if len(df) == 0:
            return False, "Le fichier ne contient aucune donnée"
        
        return True, None
    
    @staticmethod
    def validate_product_data(
        data: pd.DataFrame,
        product_id: str,
        min_points: int = 7
    ) -> Tuple[bool, Optional[str]]:
        """
        Valide les données d'un produit pour la prévision
        """
        if len(data) < min_points:
            return False, f"Données insuffisantes: {len(data)} points (minimum {min_points})"
        
        if data['quantity'].sum() == 0:
            return False, "Toutes les ventes sont à zéro"
        
        # Vérifier la continuité temporelle
        data_sorted = data.sort_values('date')
        date_range = (data_sorted['date'].max() - data_sorted['date'].min()).days
        
        if date_range < min_points:
            return False, f"Période trop courte: {date_range} jours (minimum {min_points})"
        
        return True, None
    
    @staticmethod
    def validate_forecast_params(horizon_days: int, max_horizon: int = 365):
        """Valide les paramètres de prévision"""
        if horizon_days <= 0:
            raise ValidationError("L'horizon doit être > 0")
        
        if horizon_days > max_horizon:
            raise ValidationError(f"Horizon maximum: {max_horizon} jours")
    
    @staticmethod
    def validate_recommendation_params(
        current_stock: float,
        lead_time_days: int,
        service_level_percent: int
    ):
        """Valide les paramètres de recommandation"""
        if current_stock < 0:
            raise ValidationError("Le stock actuel ne peut pas être négatif")
        
        if lead_time_days <= 0:
            raise ValidationError("Le délai de livraison doit être > 0")
        
        if not (80 <= service_level_percent <= 99):
            raise ValidationError("Le niveau de service doit être entre 80 et 99%")