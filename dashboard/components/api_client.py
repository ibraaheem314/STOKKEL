"""
Client API pour communiquer avec le backend Stokkel
"""

import requests
import streamlit as st
from typing import Optional, Dict, Any
import time
from functools import wraps


def handle_api_errors(func):
    """Décorateur pour gérer les erreurs API"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            st.error("⚠️ **Impossible de se connecter à l'API**\n\nVérifiez que le serveur backend est démarré.")
            return None
        except requests.exceptions.Timeout:
            st.error("⏱️ **Timeout**\n\nLe serveur met trop de temps à répondre.")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ **Erreur HTTP {e.response.status_code}**\n\n{e.response.text}")
            return None
        except Exception as e:
            st.error(f"❌ **Erreur inattendue**\n\n{str(e)}")
            return None
    return wrapper


class APIClient:
    """Client pour interagir avec l'API Stokkel"""
    
    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or st.session_state.get('api_url', 'http://localhost:8000')
        self.token = token or st.session_state.get('api_token', 'stokkel_mvp_token_2024')
        self.timeout = 30  # seconds
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        })
    
    @handle_api_errors
    def health_check(self) -> Optional[Dict[str, Any]]:
        """Vérifie la santé de l'API"""
        response = self.session.get(
            f"{self.base_url}/health",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors
    def upload_sales(self, file_data) -> Optional[Dict[str, Any]]:
        """Upload les données de ventes"""
        files = {'file': ('sales_data.csv', file_data, 'text/csv')}

        # Utiliser une session temporaire sans Content-Type pour l'upload de fichier
        headers = {
            'Authorization': f'Bearer {self.token}'
        }


        response = requests.post(
            f"{self.base_url}/upload_sales",
            files=files,
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors
    def get_products(self) -> Optional[Dict[str, Any]]:
        """Récupère la liste des produits"""
        response = self.session.get(
            f"{self.base_url}/products",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors
    def get_forecast(self, product_id: str, horizon_days: int = 30) -> Optional[Dict[str, Any]]:
        """Récupère les prévisions pour un produit"""
        response = self.session.get(
            f"{self.base_url}/forecast/{product_id}",
            params={'horizon_days': horizon_days},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors
    def get_recommendation(
        self,
        product_id: str,
        current_stock: int,
        lead_time_days: int,
        service_level_percent: int
    ) -> Optional[Dict[str, Any]]:
        """Récupère les recommandations pour un produit"""
        response = self.session.get(
            f"{self.base_url}/recommendation/{product_id}",
            params={
                'current_stock': current_stock,
                'lead_time_days': lead_time_days,
                'service_level_percent': service_level_percent
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors
    def get_batch_recommendations(
        self,
        lead_time_days: int,
        service_level_percent: int
    ) -> Optional[Dict[str, Any]]:
        """Récupère les recommandations pour tous les produits"""
        response = self.session.post(
            f"{self.base_url}/batch_recommendations",
            params={
                'lead_time_days': lead_time_days,
                'service_level_percent': service_level_percent
            },
            timeout=60  # Plus long timeout pour batch
        )
        response.raise_for_status()
        return response.json()
    
    def test_connection(self) -> bool:
        """Teste la connexion à l'API"""
        try:
            result = self.health_check()
            return result is not None and result.get('status') == 'ok'
        except:
            return False


def with_loading(message: str = "Chargement..."):
    """Décorateur pour afficher un spinner pendant les appels API"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                
                if result is not None:
                    st.session_state.stats['api_calls_today'] += 1
                    if elapsed > 2:
                        st.info(f"⏱️ Opération terminée en {elapsed:.1f} secondes")
                
                return result
        return wrapper
    return decorator