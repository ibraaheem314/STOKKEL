"""
Tests pour le système d'authentification JWT
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import authenticate_user, create_access_token, get_user

client = TestClient(app)

class TestAuthentication:
    """Tests du système d'authentification"""
    
    def test_login_success(self):
        """Test login avec credentials valides"""
        response = client.post(
            "/auth/token",
            data={"username": "demo", "password": "demo"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "demo"
    
    def test_login_invalid_credentials(self):
        """Test login avec credentials invalides"""
        response = client.post(
            "/auth/token",
            data={"username": "demo", "password": "wrong"}
        )
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        """Test login avec utilisateur inexistant"""
        response = client.post(
            "/auth/token",
            data={"username": "nonexistent", "password": "password"}
        )
        
        assert response.status_code == 401
    
    def test_get_user_info(self):
        """Test récupération des infos utilisateur"""
        # Login d'abord
        login_response = client.post(
            "/auth/token",
            data={"username": "demo", "password": "demo"}
        )
        token = login_response.json()["access_token"]
        
        # Test endpoint /me
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "demo"
        assert data["role"] == "user"
    
    def test_get_user_info_invalid_token(self):
        """Test /me avec token invalide"""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_get_user_info_no_token(self):
        """Test /me sans token"""
        response = client.get("/auth/me")
        
        assert response.status_code == 401
    
    def test_authenticate_user_valid(self):
        """Test fonction authenticate_user avec credentials valides"""
        user = authenticate_user("demo", "demo")
        assert user is not None
        assert user.username == "demo"
        assert user.role == "user"
    
    def test_authenticate_user_invalid(self):
        """Test fonction authenticate_user avec credentials invalides"""
        user = authenticate_user("demo", "wrong")
        assert user is None
    
    def test_get_user_existing(self):
        """Test get_user avec utilisateur existant"""
        user = get_user("demo")
        assert user is not None
        assert user.username == "demo"
    
    def test_get_user_nonexistent(self):
        """Test get_user avec utilisateur inexistant"""
        user = get_user("nonexistent")
        assert user is None
    
    def test_create_access_token(self):
        """Test création de token JWT"""
        token = create_access_token({"sub": "demo"})
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_protected_endpoint_without_auth(self):
        """Test endpoint protégé sans authentification"""
        response = client.get("/forecast/P001")
        assert response.status_code == 401
    
    def test_protected_endpoint_with_auth(self):
        """Test endpoint protégé avec authentification"""
        # Login d'abord
        login_response = client.post(
            "/auth/token",
            data={"username": "demo", "password": "demo"}
        )
        token = login_response.json()["access_token"]
        
        # Test endpoint protégé (même si pas de données, l'auth doit passer)
        response = client.get(
            "/forecast/P001",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Peut être 404 (pas de données) ou 400 (validation), mais pas 401
        assert response.status_code != 401
