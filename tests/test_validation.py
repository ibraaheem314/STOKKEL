"""
Tests pour le système de validation
"""

import pytest
import pandas as pd
from datetime import datetime, date
from app.validators import DataValidator
from app.exceptions import DataValidationError, InsufficientDataError, InvalidProductError

class TestDataValidator:
    """Tests du validateur de données"""
    
    def test_validate_sales_dataframe_valid(self):
        """Test validation DataFrame valide"""
        df = pd.DataFrame({
            'product_id': ['P001', 'P001', 'P001'],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'quantity': [10, 15, 12]
        })
        
        is_valid, error = DataValidator.validate_sales_dataframe(df)
        assert is_valid
        assert error is None
    
    def test_validate_sales_dataframe_missing_columns(self):
        """Test validation DataFrame avec colonnes manquantes"""
        df = pd.DataFrame({
            'product_id': ['P001'],
            'quantity': [10]
            # Manque 'date'
        })
        
        is_valid, error = DataValidator.validate_sales_dataframe(df)
        assert not is_valid
        assert "Colonnes manquantes" in error
    
    def test_validate_sales_dataframe_negative_quantities(self):
        """Test validation DataFrame avec quantités négatives"""
        df = pd.DataFrame({
            'product_id': ['P001'],
            'date': ['2024-01-01'],
            'quantity': [-10]  # Négatif !
        })
        
        is_valid, error = DataValidator.validate_sales_dataframe(df)
        assert not is_valid
        assert "négatives" in error
    
    def test_validate_sales_dataframe_empty(self):
        """Test validation DataFrame vide"""
        df = pd.DataFrame(columns=['product_id', 'date', 'quantity'])
        
        is_valid, error = DataValidator.validate_sales_dataframe(df)
        assert not is_valid
        assert "vide" in error
    
    def test_validate_sales_dataframe_invalid_date(self):
        """Test validation DataFrame avec dates invalides"""
        df = pd.DataFrame({
            'product_id': ['P001'],
            'date': ['invalid_date'],
            'quantity': [10]
        })
        
        is_valid, error = DataValidator.validate_sales_dataframe(df)
        assert not is_valid
        assert "date" in error
    
    def test_validate_forecast_request_valid(self):
        """Test validation requête prévision valide"""
        is_valid, error = DataValidator.validate_forecast_request("P001", 30)
        assert is_valid
        assert error is None
    
    def test_validate_forecast_request_invalid_product_id(self):
        """Test validation requête prévision avec product_id invalide"""
        # Product ID vide
        is_valid, error = DataValidator.validate_forecast_request("", 30)
        assert not is_valid
        assert "chaîne non vide" in error
        
        # Product ID trop long
        long_id = "P" * 51
        is_valid, error = DataValidator.validate_forecast_request(long_id, 30)
        assert not is_valid
        assert "trop long" in error
    
    def test_validate_forecast_request_invalid_horizon(self):
        """Test validation requête prévision avec horizon invalide"""
        # Horizon négatif
        is_valid, error = DataValidator.validate_forecast_request("P001", -1)
        assert not is_valid
        assert ">= 1" in error
        
        # Horizon trop grand
        is_valid, error = DataValidator.validate_forecast_request("P001", 400)
        assert not is_valid
        assert "<= 365" in error
    
    def test_validate_recommendation_request_valid(self):
        """Test validation requête recommandation valide"""
        is_valid, error = DataValidator.validate_recommendation_request(
            "P001", 100.0, 7, 95.0
        )
        assert is_valid
        assert error is None
    
    def test_validate_recommendation_request_invalid_stock(self):
        """Test validation requête recommandation avec stock invalide"""
        # Stock négatif
        is_valid, error = DataValidator.validate_recommendation_request(
            "P001", -10.0, 7, 95.0
        )
        assert not is_valid
        assert "négatif" in error
    
    def test_validate_recommendation_request_invalid_lead_time(self):
        """Test validation requête recommandation avec délai invalide"""
        # Délai négatif
        is_valid, error = DataValidator.validate_recommendation_request(
            "P001", 100.0, -1, 95.0
        )
        assert not is_valid
        assert "négatif" in error
    
    def test_validate_recommendation_request_invalid_service_level(self):
        """Test validation requête recommandation avec niveau de service invalide"""
        # Niveau de service négatif
        is_valid, error = DataValidator.validate_recommendation_request(
            "P001", 100.0, 7, -10.0
        )
        assert not is_valid
        assert "entre 0 et 100" in error
        
        # Niveau de service > 100
        is_valid, error = DataValidator.validate_recommendation_request(
            "P001", 100.0, 7, 150.0
        )
        assert not is_valid
        assert "entre 0 et 100" in error

class TestExceptions:
    """Tests des exceptions personnalisées"""
    
    def test_insufficient_data_error(self):
        """Test exception données insuffisantes"""
        error = InsufficientDataError(
            "Pas assez de données", 
            min_required=30, 
            actual=10
        )
        
        assert error.error_code == "INSUFFICIENT_DATA"
        assert error.details["min_required"] == 30
        assert error.details["actual"] == 10
        assert "recommendation" in error.details
    
    def test_invalid_product_error(self):
        """Test exception produit invalide"""
        error = InvalidProductError("P999", ["P001", "P002"])
        
        assert error.error_code == "INVALID_PRODUCT"
        assert error.details["product_id"] == "P999"
        assert "P001" in error.details["available_products"]
        assert "recommendation" in error.details
    
    def test_data_validation_error(self):
        """Test exception validation données"""
        error = DataValidationError("Format invalide", "product_id", "P999")
        
        assert error.error_code == "DATA_VALIDATION_ERROR"
        assert error.details["field"] == "product_id"
        assert error.details["value"] == "P999"
        assert "recommendation" in error.details
