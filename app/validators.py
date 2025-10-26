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
        
        # Vérifier que le DataFrame n'est pas vide
        if len(df) == 0:
            return False, "Le fichier ne contient aucune donnée (vide)"
        
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
        
        # Support des formats Prophet (y, ds) et standard (quantity, date)
        quantity_col = 'y' if 'y' in data.columns else 'quantity'
        date_col = 'ds' if 'ds' in data.columns else 'date'
        
        if quantity_col not in data.columns:
            return False, f"Colonne de quantité manquante: {quantity_col}"
        if date_col not in data.columns:
            return False, f"Colonne de date manquante: {date_col}"
        
        if data[quantity_col].sum() == 0:
            return False, "Toutes les ventes sont à zéro"
        
        # Vérifier la continuité temporelle
        data_sorted = data.sort_values(date_col)
        date_range = (data_sorted[date_col].max() - data_sorted[date_col].min()).days
        
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
    
    @staticmethod
    def validate_forecast_request(product_id: str, horizon_days: int) -> Tuple[bool, Optional[str]]:
        """
        Valide une requête de prévision
        
        Args:
            product_id: Identifiant du produit
            horizon_days: Nombre de jours à prévoir
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # Validation product_id
        if not product_id or not isinstance(product_id, str):
            return False, "product_id doit être une chaîne non vide"
        
        if len(product_id) > 50:
            return False, "product_id trop long (max 50 caractères)"
        
        # Validation horizon_days
        if not isinstance(horizon_days, int):
            return False, "horizon_days doit être un entier"
        
        if horizon_days < 1:
            return False, "horizon_days doit être >= 1"
        
        if horizon_days > 365:
            return False, "horizon_days doit être <= 365"
        
        # Warning pour horizons longs
        if horizon_days > 90:
            import warnings
            warnings.warn("Prévisions au-delà de 90 jours peuvent être moins précises")
        
        return True, None
    
    @staticmethod
    def validate_recommendation_request(
        product_id: str, 
        current_stock: float, 
        lead_time_days: int, 
        service_level_percent: float
    ) -> Tuple[bool, Optional[str]]:
        """
        Valide une requête de recommandation
        
        Args:
            product_id: Identifiant du produit
            current_stock: Stock actuel
            lead_time_days: Délai de livraison
            service_level_percent: Niveau de service
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # Validation product_id
        if not product_id or not isinstance(product_id, str):
            return False, "product_id doit être une chaîne non vide"
        
        # Validation current_stock
        if not isinstance(current_stock, (int, float)):
            return False, "current_stock doit être numérique"
        
        if current_stock < 0:
            return False, "current_stock ne peut pas être négatif"
        
        # Validation lead_time_days
        if not isinstance(lead_time_days, int):
            return False, "lead_time_days doit être un entier"
        
        if lead_time_days < 0:
            return False, "lead_time_days ne peut pas être négatif"
        
        if lead_time_days > 365:
            return False, "lead_time_days doit être <= 365"
        
        # Validation service_level_percent
        if not isinstance(service_level_percent, (int, float)):
            return False, "service_level_percent doit être numérique"
        
        if service_level_percent < 0 or service_level_percent > 100:
            return False, "service_level_percent doit être entre 0 et 100"
        
        return True, None