"""
🎨 STOKKEL DASHBOARD - Gestion des Données (Design Unique)
==========================================================

Page de gestion des données avec le nouveau design system
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from components.unique_design_system import (
    apply_stokkel_design, 
    create_kpi_card, 
    create_alert, 
    create_section_header
)
from components.api_client import with_loading

def render(api_client):
    """
    Page de gestion des données avec design unique Stokkel
    """
    
    # Appliquer le design system
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # ============================================
    # HEADER SECTION
    # ============================================
    
    st.markdown(create_section_header(
        "📊 Gestion des Données",
        "Upload et configuration des données de ventes historiques"
    ), unsafe_allow_html=True)
    
    # ============================================
    # STATS RAPIDES
    # ============================================
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Produits",
            value="12",
            delta=2,
            icon="📦"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Enregistrements",
            value="1,247",
            delta=156,
            icon="📈"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="Période",
            value="90j",
            delta=0,
            icon="📅"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            label="Dernière MAJ",
            value="2h",
            delta=0,
            icon="🔄"
        ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # UPLOAD SECTION
    # ============================================
    
    st.markdown(create_section_header(
        "📤 Upload de Données",
        "Téléchargez vos fichiers CSV de ventes"
    ), unsafe_allow_html=True)
    
    # Zone d'upload
    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV",
        type=['csv'],
        help="Format requis: product_id, date, quantity"
    )
    
    if uploaded_file is not None:
        try:
            # Simulation de traitement
            with st.spinner("Traitement des données..."):
                import time
                time.sleep(2)
            
            st.success("✅ Données chargées avec succès!")
            
            # Aperçu des données
            df = pd.read_csv(uploaded_file)
            st.markdown("**Aperçu des données:**")
            st.dataframe(df.head(10), use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement: {str(e)}")
    
    # ============================================
    # CONFIGURATION
    # ============================================
    
    st.markdown(create_section_header(
        "⚙️ Configuration",
        "Paramètres de traitement des données"
    ), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox(
            "Format de date",
            ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"],
            help="Format des dates dans vos données"
        )
    
    with col2:
        st.selectbox(
            "Séparateur CSV",
            [",", ";", "|"],
            help="Séparateur utilisé dans votre fichier CSV"
        )
    
    # ============================================
    # ALERTES
    # ============================================
    
    st.markdown(create_alert(
        "💡 Conseil: Assurez-vous que vos données contiennent au moins 30 jours d'historique pour des prévisions optimales.",
        alert_type="info"
    ), unsafe_allow_html=True)