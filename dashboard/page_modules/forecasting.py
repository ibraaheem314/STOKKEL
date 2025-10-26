"""
🎨 STOKKEL DASHBOARD - Prévisions (Design Unique)
=================================================

Page de prévisions avec le nouveau design system
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.unique_design_system import (
    apply_stokkel_design, 
    create_kpi_card, 
    create_alert, 
    create_section_header
)
from components.api_client import with_loading

@with_loading("Génération de la prévision en cours...")
def generate_forecast(api_client, product_id, horizon_days):
    """Génère une prévision pour un produit"""
    forecast_data = api_client.get_forecast(product_id, horizon_days)
    if forecast_data:
        # Mettre en cache
        cache_key = f"{product_id}_{horizon_days}"
        st.session_state.forecasts_cache[cache_key] = forecast_data
        st.session_state.last_forecast = forecast_data
    return forecast_data

def render(api_client):
    """
    Page de prévisions avec design unique Stokkel
    """
    
    # Appliquer le design system
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # ============================================
    # HEADER SECTION
    # ============================================
    
    st.markdown(create_section_header(
        "📈 Prévisions de Ventes",
        "Génération de prévisions probabilistes avec IA"
    ), unsafe_allow_html=True)
    
    # ============================================
    # KPIs DE PRÉVISION
    # ============================================
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Précision Moyenne",
            value="91.2%",
            delta=3.5,
            icon="🎯"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Produits Prévisibles",
            value="8/12",
            delta=1,
            icon="📊"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="Horizon",
            value="30j",
            delta=0,
            icon="📅"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            label="Dernière Génération",
            value="2h",
            delta=0,
            icon="🔄"
        ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SÉLECTION PRODUIT
    # ============================================
    
    st.markdown(create_section_header(
        "🎯 Sélection du Produit",
        "Choisissez le produit pour générer la prévision"
    ), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        product = st.selectbox(
            "Produit",
            ["P001 - Smartphone Galaxy", "P002 - Laptop Pro", "P003 - Écouteurs Wireless"],
            help="Sélectionnez le produit à analyser"
        )
    
    with col2:
        horizon = st.selectbox(
            "Horizon",
            [7, 14, 30, 60],
            help="Nombre de jours à prévoir"
        )
    
    with col3:
        confidence = st.selectbox(
            "Niveau de Confiance",
            [80, 90, 95],
            help="Intervalle de confiance"
        )
    
    # ============================================
    # GÉNÉRATION PRÉVISION
    # ============================================
    
    if st.button("🚀 Générer la Prévision", type="primary"):
        with st.spinner("Génération de la prévision en cours..."):
            import time
            time.sleep(3)
        
        st.success("✅ Prévision générée avec succès!")
        
        # ============================================
        # GRAPHIQUE DE PRÉVISION
        # ============================================
        
        st.markdown(create_section_header(
            "📊 Résultats de Prévision",
            f"Prévision pour {product} sur {horizon} jours"
        ), unsafe_allow_html=True)
        
        # Données simulées
        dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
        historical = [50 + i*0.5 + (i%7)*10 for i in range(60)]
        forecast = [80 + i*0.3 + (i%5)*8 for i in range(30)]
        
        # Création du graphique
        fig = go.Figure()
        
        # Données historiques
        fig.add_trace(go.Scatter(
            x=dates[:60],
            y=historical,
            mode='lines',
            name='Historique',
            line=dict(color='#1B4965', width=2)
        ))
        
        # Prévision
        fig.add_trace(go.Scatter(
            x=dates[60:90],
            y=forecast,
            mode='lines',
            name='Prévision',
            line=dict(color='#D2691E', width=3)
        ))
        
        # Intervalle de confiance
        upper_bound = [f + 15 for f in forecast]
        lower_bound = [f - 15 for f in forecast]
        
        fig.add_trace(go.Scatter(
            x=dates[60:90],
            y=upper_bound,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates[60:90],
            y=lower_bound,
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(210, 105, 30, 0.2)',
            line=dict(width=0),
            name=f'Intervalle {confidence}%',
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title=f"Prévision de Ventes - {product}",
            xaxis_title="Date",
            yaxis_title="Quantité Vendue",
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # MÉTRIQUES DE PRÉVISION
        # ============================================
        
        st.markdown(create_section_header(
            "📊 Métriques de Performance",
            "Évaluation de la qualité de la prévision"
        ), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_kpi_card(
                label="MAPE",
                value="8.5%",
                delta=-1.2,
                icon="🎯"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_kpi_card(
                label="RMSE",
                value="12.3",
                delta=-0.8,
                icon="📊"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_kpi_card(
                label="R²",
                value="0.89",
                delta=0.05,
                icon="📈"
            ), unsafe_allow_html=True)
    
    # ============================================
    # ALERTES
    # ============================================
    
    st.markdown(create_alert(
        "💡 Conseil: Les prévisions sont plus précises avec au moins 60 jours d'historique et des données sans trous.",
        alert_type="info"
    ), unsafe_allow_html=True)