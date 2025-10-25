"""
Tests de l'API Stokkel
======================
Tests basiques des endpoints principaux.

Pour exécuter:
    pytest tests/test_api.py -v
    
Ou pour tous les tests:
    pytest tests/ -v --cov=app
"""

import pytest
from fastapi.testclient import TestClient
import pandas as pd
from io import BytesIO
import sys
import os

# Ajouter le dossier parent au path pour importer l'app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.data_utils import generate_synthetic_sales

# Client de test
client = TestClient(app)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_csv_data():
    """Génère des données CSV de test."""
    df = generate_synthetic_sales(num_products=2, num_days=90, seed=42)
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer.getvalue()


@pytest.fixture
def uploaded_data(sample_csv_data):
    """Upload les données et retourne la réponse."""
    response = client.post(
        "/upload_sales",
        files={"file": ("test_sales.csv", sample_csv_data, "text/csv")}
    )
    assert response.status_code == 200
    return response.json()


# ============================================================================
# TESTS HEALTH CHECK
# ============================================================================

def test_health_check():
    """Test du endpoint de santé."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint():
    """Test du endpoint racine."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "api_name" in data


# ============================================================================
# TESTS UPLOAD DE DONNÉES
# ============================================================================

def test_upload_sales_success(sample_csv_data):
    """Test upload de fichier CSV valide."""
    response = client.post(
        "/upload_sales",
        files={"file": ("sales.csv", sample_csv_data, "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure de la réponse
    assert "message" in data
    assert "summary" in data
    assert data["summary"]["num_products"] == 2
    assert data["summary"]["total_rows"] == 180  # 2 produits * 90 jours


def test_upload_sales_invalid_file():
    """Test upload d'un fichier invalide."""
    invalid_data = b"not,a,valid,csv\n1,2"
    
    response = client.post(
        "/upload_sales",
        files={"file": ("invalid.csv", invalid_data, "text/csv")}
    )
    
    # Devrait retourner une erreur 400
    assert response.status_code == 400


def test_upload_sales_missing_columns():
    """Test upload CSV avec colonnes manquantes."""
    invalid_df = pd.DataFrame({
        'product_id': ['PROD_001'],
        'date': ['2024-01-01']
        # Manque 'quantity'
    })
    
    csv_buffer = BytesIO()
    invalid_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    response = client.post(
        "/upload_sales",
        files={"file": ("missing_cols.csv", csv_buffer.getvalue(), "text/csv")}
    )
    
    assert response.status_code == 400
    assert "manquantes" in response.json()["detail"].lower()


# ============================================================================
# TESTS PRÉVISIONS
# ============================================================================

def test_forecast_endpoint(uploaded_data):
    """Test du endpoint de prévision."""
    # Récupérer le premier produit
    product_id = uploaded_data["summary"]["products"][0]["product_id"]
    
    response = client.get(
        f"/forecast/{product_id}",
        params={"horizon_days": 30}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure de la réponse
    assert "product_id" in data
    assert "daily_forecast" in data
    assert "total_demand" in data
    assert len(data["daily_forecast"]) == 30
    
    # Vérifier les quantiles
    first_day = data["daily_forecast"][0]
    assert "p10" in first_day
    assert "p50" in first_day
    assert "p90" in first_day
    assert first_day["p10"] <= first_day["p50"] <= first_day["p90"]


def test_forecast_invalid_product():
    """Test prévision pour un produit inexistant."""
    response = client.get("/forecast/INVALID_PRODUCT")
    assert response.status_code == 404


def test_forecast_without_upload():
    """Test prévision sans avoir uploadé de données."""
    # Réinitialiser (simuler une nouvelle session)
    response = client.get("/forecast/PROD_001")
    assert response.status_code in [400, 404]  # Devrait échouer


# ============================================================================
# TESTS RECOMMANDATIONS
# ============================================================================

def test_recommendation_endpoint(uploaded_data):
    """Test du endpoint de recommandation."""
    product_id = uploaded_data["summary"]["products"][0]["product_id"]
    
    response = client.get(
        f"/recommendation/{product_id}",
        params={
            "current_stock": 500,
            "lead_time_days": 7,
            "service_level_percent": 95.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure
    assert "recommendation_action" in data
    assert "quantity_to_order" in data
    assert "reorder_point" in data
    assert "safety_stock" in data
    assert "urgency_level" in data
    assert "message" in data
    
    # Vérifier les valeurs logiques
    assert data["reorder_point"] > 0
    assert data["safety_stock"] >= 0
    assert data["urgency_level"] in ["low", "medium", "high", "critical"]


def test_recommendation_critical_stock(uploaded_data):
    """Test recommandation avec stock critique."""
    product_id = uploaded_data["summary"]["products"][0]["product_id"]
    
    response = client.get(
        f"/recommendation/{product_id}",
        params={
            "current_stock": 10,  # Stock très bas
            "lead_time_days": 7,
            "service_level_percent": 95.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Devrait recommander une commande urgente
    assert data["urgency_level"] in ["high", "critical"]
    assert data["quantity_to_order"] > 0


def test_recommendation_sufficient_stock(uploaded_data):
    """Test recommandation avec stock suffisant."""
    product_id = uploaded_data["summary"]["products"][0]["product_id"]
    
    response = client.get(
        f"/recommendation/{product_id}",
        params={
            "current_stock": 10000,  # Stock très élevé
            "lead_time_days": 7,
            "service_level_percent": 95.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Ne devrait pas recommander de commande
    assert data["recommendation_action"] == "STOCK_SUFFICIENT"
    assert data["quantity_to_order"] == 0


# ============================================================================
# TESTS BATCH
# ============================================================================

def test_batch_forecast(uploaded_data):
    """Test prévisions en batch."""
    product_ids = [p["product_id"] for p in uploaded_data["summary"]["products"]]
    
    response = client.post(
        "/batch_forecast",
        json={
            "product_ids": product_ids,
            "horizon_days": 30
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(product_ids)


# ============================================================================
# TESTS PRODUITS
# ============================================================================

def test_list_products(uploaded_data):
    """Test liste des produits disponibles."""
    response = client.get("/products")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # 2 produits dans les données de test


# ============================================================================
# TESTS DE VALIDATION
# ============================================================================

def test_invalid_horizon_days(uploaded_data):
    """Test avec un horizon invalide."""
    product_id = uploaded_data["summary"]["products"][0]["product_id"]
    
    # Horizon négatif
    response = client.get(
        f"/forecast/{product_id}",
        params={"horizon_days": -10}
    )
    assert response.status_code == 422  # Validation error


def test_invalid_service_level(uploaded_data):
    """Test avec un service level invalide."""
    product_id = uploaded_data["summary"]["products"][0]["product_id"]
    
    # Service level > 100%
    response = client.get(
        f"/recommendation/{product_id}",
        params={
            "current_stock": 500,
            "lead_time_days": 7,
            "service_level_percent": 150.0
        }
    )
    assert response.status_code == 422  # Validation error


# ============================================================================
# MAIN - Pour exécution directe
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])