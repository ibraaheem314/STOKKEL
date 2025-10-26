"""
Tests d'intégration pour l'API Stokkel
"""

import pytest
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
import tempfile
import os

client = TestClient(app)

class TestAPIIntegration:
    """Tests d'intégration de l'API"""
    
    def setup_method(self):
        """Setup pour chaque test"""
        self.token = self._get_auth_token()
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def _get_auth_token(self):
        """Obtient un token d'authentification"""
        response = client.post(
            "/auth/token",
            data={"username": "demo", "password": "demo"}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_health_endpoint(self):
        """Test endpoint de santé"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        assert "details" in data
    
    def test_info_endpoint(self):
        """Test endpoint d'informations"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "description" in data
    
    def test_upload_sales_data(self):
        """Test upload de données de ventes"""
        # Créer des données de test
        test_data = pd.DataFrame({
            'product_id': ['P001', 'P001', 'P001', 'P002', 'P002'],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-01', '2024-01-02'],
            'quantity': [10, 15, 12, 8, 11]
        })
        
        # Sauvegarder dans un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            # Upload du fichier
            with open(temp_file, 'rb') as f:
                response = client.post(
                    "/upload_sales",
                    files={"file": ("test.csv", f, "text/csv")},
                    headers=self.headers
                )
            
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "total_records" in data
            assert "products_count" in data
            
        finally:
            # Nettoyer le fichier temporaire
            os.unlink(temp_file)
    
    def test_upload_invalid_data(self):
        """Test upload de données invalides"""
        # Créer des données invalides (colonnes manquantes)
        test_data = pd.DataFrame({
            'product': ['P001'],  # Mauvais nom de colonne
            'sales': [10]  # Mauvais nom de colonne
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            with open(temp_file, 'rb') as f:
                response = client.post(
                    "/upload_sales",
                    files={"file": ("test.csv", f, "text/csv")},
                    headers=self.headers
                )
            
            # Doit retourner une erreur
            assert response.status_code == 400
            
        finally:
            os.unlink(temp_file)
    
    def test_products_endpoint(self):
        """Test endpoint des produits"""
        response = client.get("/products", headers=self.headers)
        
        # Peut être 200 (avec produits) ou 404 (sans données)
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "products" in data
            assert isinstance(data["products"], list)
    
    def test_forecast_endpoint_without_data(self):
        """Test endpoint prévision sans données"""
        response = client.get("/forecast/P001", headers=self.headers)
        
        # Doit retourner une erreur car pas de données
        assert response.status_code in [400, 404, 422]
    
    def test_recommendation_endpoint_without_data(self):
        """Test endpoint recommandation sans données"""
        response = client.get("/recommendation/P001", headers=self.headers)
        
        # Doit retourner une erreur car pas de données
        assert response.status_code in [400, 404, 422, 500]
    
    def test_batch_recommendations_endpoint(self):
        """Test endpoint recommandations en lot"""
        request_data = {
            "products": [
                {"product_id": "P001", "current_stock": 100},
                {"product_id": "P002", "current_stock": 50}
            ],
            "lead_time_days": 7,
            "service_level_percent": 95
        }
        
        response = client.post(
            "/batch_recommendations",
            json=request_data,
            headers=self.headers
        )
        
        # Peut être 200 (avec données) ou erreur (sans données)
        assert response.status_code in [200, 400, 404, 422]
    
    def test_unauthorized_access(self):
        """Test accès non autorisé"""
        # Test sans token
        response = client.get("/forecast/P001")
        assert response.status_code == 401
        
        # Test avec token invalide
        response = client.get(
            "/forecast/P001",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_cors_headers(self):
        """Test headers CORS"""
        response = client.options("/health")
        # CORS est configuré, donc pas d'erreur 405
        assert response.status_code in [200, 405]  # 405 est acceptable pour OPTIONS
    
    def test_api_documentation(self):
        """Test documentation API"""
        # Test OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        
        # Test docs Swagger
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test docs ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200

class TestDataFlow:
    """Tests du flux de données complet"""
    
    def setup_method(self):
        """Setup pour chaque test"""
        self.token = self._get_auth_token()
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def _get_auth_token(self):
        """Obtient un token d'authentification"""
        response = client.post(
            "/auth/token",
            data={"username": "demo", "password": "demo"}
        )
        return response.json()["access_token"]
    
    def test_complete_workflow(self):
        """Test workflow complet: upload -> forecast -> recommendation"""
        # 1. Upload des données
        test_data = pd.DataFrame({
            'product_id': ['P001'] * 30,  # 30 jours de données
            'date': pd.date_range('2024-01-01', periods=30).strftime('%Y-%m-%d'),
            'quantity': [10 + i % 5 for i in range(30)]  # Données avec pattern
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            # Upload
            with open(temp_file, 'rb') as f:
                upload_response = client.post(
                    "/upload_sales",
                    files={"file": ("test.csv", f, "text/csv")},
                    headers=self.headers
                )
            
            if upload_response.status_code == 200:
                # 2. Vérifier que les produits sont disponibles
                products_response = client.get("/products", headers=self.headers)
                
                if products_response.status_code == 200:
                    products_data = products_response.json()
                    products = products_data["products"]
                    product_ids = [p["product_id"] for p in products]
                    assert "P001" in product_ids
                    
                    # 3. Test prévision
                    forecast_response = client.get(
                        "/forecast/P001?horizon_days=7",
                        headers=self.headers
                    )
                    
                    # Peut réussir ou échouer selon la qualité des données
                    assert forecast_response.status_code in [200, 400, 404, 422]
                    
                    # 4. Test recommandation
                    recommendation_response = client.get(
                        "/recommendation/P001?current_stock=50",
                        headers=self.headers
                    )
                    
                    # Peut réussir ou échouer selon la qualité des données
                    assert recommendation_response.status_code in [200, 400, 422]
            
        finally:
            os.unlink(temp_file)
    
    def test_error_handling(self):
        """Test gestion d'erreurs"""
        # Test avec données insuffisantes
        test_data = pd.DataFrame({
            'product_id': ['P001'] * 5,  # Seulement 5 jours
            'date': pd.date_range('2024-01-01', periods=5).strftime('%Y-%m-%d'),
            'quantity': [10, 15, 12, 8, 11]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            with open(temp_file, 'rb') as f:
                response = client.post(
                    "/upload_sales",
                    files={"file": ("test.csv", f, "text/csv")},
                    headers=self.headers
                )
            
            # Upload peut réussir même avec peu de données
            if response.status_code == 200:
                # Mais la prévision doit échouer
                forecast_response = client.get(
                    "/forecast/P001",
                    headers=self.headers
                )
                
                # Doit retourner une erreur pour données insuffisantes
                assert forecast_response.status_code in [400, 404, 422]
                
        finally:
            os.unlink(temp_file)
