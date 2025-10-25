"""
Gestion de l'état de session Streamlit
"""

import streamlit as st
from typing import Any, Dict


def initialize_session_state():
    """Initialise toutes les variables de session"""
    
    # État des données
    if 'data_uploaded' not in st.session_state:
        st.session_state.data_uploaded = False
    
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    
    if 'mapped_data' not in st.session_state:
        st.session_state.mapped_data = None
    
    if 'column_mapping' not in st.session_state:
        st.session_state.column_mapping = {}
    
    # Produits
    if 'products' not in st.session_state:
        st.session_state.products = []
    
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None
    
    # Prévisions
    if 'forecasts_cache' not in st.session_state:
        st.session_state.forecasts_cache = {}
    
    if 'last_forecast' not in st.session_state:
        st.session_state.last_forecast = None
    
    # Recommandations
    if 'recommendations_cache' not in st.session_state:
        st.session_state.recommendations_cache = {}
    
    if 'batch_recommendations' not in st.session_state:
        st.session_state.batch_recommendations = None
    
    # Configuration
    if 'api_url' not in st.session_state:
        st.session_state.api_url = "http://localhost:8000"
    
    if 'api_token' not in st.session_state:
        st.session_state.api_token = "stokkel_mvp_token_2024"
    
    if 'default_lead_time' not in st.session_state:
        st.session_state.default_lead_time = 7
    
    if 'default_service_level' not in st.session_state:
        st.session_state.default_service_level = 95
    
    # UI State
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Accueil"
    
    if 'show_advanced_options' not in st.session_state:
        st.session_state.show_advanced_options = False
    
    # Statistiques
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            'total_forecasts': 0,
            'total_recommendations': 0,
            'api_calls_today': 0,
            'stockouts_avoided': 0,
            'savings_fcfa': 0
        }


def set_session_value(key: str, value: Any):
    """Définit une valeur dans la session"""
    st.session_state[key] = value


def get_session_value(key: str, default: Any = None) -> Any:
    """Récupère une valeur de la session"""
    return st.session_state.get(key, default)


def clear_session():
    """Réinitialise toute la session"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()


def update_stats(stat_key: str, increment: int = 1):
    """Met à jour une statistique"""
    if 'stats' in st.session_state and stat_key in st.session_state.stats:
        st.session_state.stats[stat_key] += increment


def get_stats() -> Dict[str, Any]:
    """Retourne toutes les statistiques"""
    return st.session_state.get('stats', {})