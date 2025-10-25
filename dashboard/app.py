"""
Stokkel Dashboard - Interface principale améliorée
Architecture modulaire avec composants réutilisables
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Configuration de la page (DOIT être la première commande Streamlit)
st.set_page_config(
    page_title="Stokkel - Gestion Intelligente des Stocks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Ajout du chemin des composants
sys.path.append(str(Path(__file__).parent))

# Import des composants
from components.styles import apply_custom_styles
from components.sidebar import render_sidebar
from components.session import initialize_session_state
from components.api_client import APIClient

# Pages
from page_modules import (
    home,
    data_management,
    forecasting,
    recommendations,
    executive_dashboard,
    setting
)

# Initialisation
initialize_session_state()
apply_custom_styles()

# Client API
api_client = APIClient()
st.session_state.api_client = api_client

# Sidebar et navigation
page = render_sidebar()

# Routage des pages
PAGES = {
    "🏠 Accueil": home,
    "📊 Gestion des Données": data_management,
    "📈 Prévisions": forecasting,
    "📦 Recommandations": recommendations,
    "🎯 Tableau de Bord": executive_dashboard,
    "⚙️ Configuration": setting
}

# Affichage de la page sélectionnée
if page in PAGES:
    try:
        PAGES[page].render(api_client)
    except Exception as e:
        st.error(f"Erreur lors du chargement de la page '{page}': {str(e)}")
        st.exception(e)
else:
    st.error(f"Page '{page}' introuvable")
    st.write("Pages disponibles:", list(PAGES.keys()))