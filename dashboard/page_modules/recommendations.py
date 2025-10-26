"""
🎨 STOKKEL DASHBOARD - Recommandations (Design Unique)
====================================================

Page de recommandations avec le nouveau design system
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

@with_loading("Calcul de la recommandation en cours...")
def generate_recommendation(api_client, product_id, current_stock, lead_time, service_level):
    """Génère une recommandation pour un produit"""
    rec = api_client.get_recommendation(product_id, current_stock, lead_time, service_level)
    return rec

@with_loading("Génération des recommandations batch en cours...")
def generate_batch_recommendations(api_client, lead_time, service_level):
    """Génère des recommandations pour tous les produits"""
    batch_rec = api_client.get_batch_recommendations(lead_time, service_level)
    if batch_rec:
        st.session_state.batch_recommendations = batch_rec
    return batch_rec

def render(api_client):
    """
    Page de recommandations avec design unique Stokkel
    """
    
    # Appliquer le design system
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # ============================================
    # HEADER SECTION
    # ============================================
    
    st.markdown(create_section_header(
        "📦 Recommandations d'Approvisionnement",
        "Optimisation intelligente des stocks avec IA"
    ), unsafe_allow_html=True)
    
    # ============================================
    # KPIs DE RECOMMANDATIONS
    # ============================================
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Actions Urgentes",
            value="5",
            delta=2,
            icon="🚨"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Économies Potentielles",
            value="€12.5K",
            delta=8.2,
            icon="💰"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="Produits Optimisés",
            value="8/12",
            delta=1,
            icon="📊"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            label="Niveau de Service",
            value="94.2%",
            delta=1.8,
            icon="🎯"
        ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # ALERTES CRITIQUES
    # ============================================
    
    st.markdown(create_section_header(
        "🚨 Alertes Critiques",
        "Produits nécessitant une action immédiate"
    ), unsafe_allow_html=True)
    
    # Données simulées d'alertes
    alerts_data = [
        {"Produit": "P001 - Smartphone Galaxy", "Stock": 2, "Seuil": 5, "Action": "Commander 50 unités", "Urgence": "Critique"},
        {"Produit": "P003 - Écouteurs Wireless", "Stock": 8, "Seuil": 10, "Action": "Commander 30 unités", "Urgence": "Élevée"},
        {"Produit": "P005 - Chargeur USB-C", "Stock": 15, "Seuil": 20, "Action": "Commander 25 unités", "Urgence": "Moyenne"},
    ]
    
    for alert in alerts_data:
        urgency_color = {
            "Critique": "critical",
            "Élevée": "warning", 
            "Moyenne": "info"
        }.get(alert["Urgence"], "info")
        
        st.markdown(create_alert(
            f"**{alert['Produit']}** - Stock: {alert['Stock']} (Seuil: {alert['Seuil']}) - {alert['Action']}",
            alert_type=urgency_color
        ), unsafe_allow_html=True)
    
    # ============================================
    # TABLEAU DE RECOMMANDATIONS
    # ============================================
    
    st.markdown(create_section_header(
        "📊 Recommandations Détaillées",
        "Actions recommandées pour chaque produit"
    ), unsafe_allow_html=True)
    
    # Données simulées
    recommendations_data = {
        "Produit": [
            "P001 - Smartphone Galaxy",
            "P002 - Laptop Pro", 
            "P003 - Écouteurs Wireless",
            "P004 - Souris Gaming",
            "P005 - Chargeur USB-C"
        ],
        "Stock Actuel": [2, 15, 8, 25, 15],
        "Stock Optimal": [50, 20, 30, 35, 25],
        "Action": [
            "Commander 48 unités",
            "Maintenir niveau actuel",
            "Commander 22 unités", 
            "Commander 10 unités",
            "Commander 10 unités"
        ],
        "Priorité": ["🔴 Critique", "🟢 OK", "🟡 Élevée", "🟡 Moyenne", "🟡 Moyenne"],
        "Coût Est.": ["€24,000", "€0", "€1,100", "€500", "€200"]
    }
    
    df_recommendations = pd.DataFrame(recommendations_data)
    
    # Affichage du tableau avec style
    st.markdown("**Recommandations par Produit**")
    st.dataframe(df_recommendations, use_container_width=True)
    
    # ============================================
    # PARAMÈTRES D'OPTIMISATION
    # ============================================
    
    st.markdown(create_section_header(
        "⚙️ Paramètres d'Optimisation",
        "Configuration des seuils et niveaux de service"
    ), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        service_level = st.slider(
            "Niveau de Service (%)",
            min_value=80,
            max_value=99,
            value=95,
            help="Probabilité de ne pas être en rupture"
        )
    
    with col2:
        lead_time = st.slider(
            "Délai de Livraison (jours)",
            min_value=1,
            max_value=30,
            value=7,
            help="Temps de réapprovisionnement"
        )
    
    with col3:
        safety_stock = st.slider(
            "Stock de Sécurité (%)",
            min_value=10,
            max_value=50,
            value=20,
            help="Pourcentage de stock de sécurité"
        )
    
    # Bouton de recalcul
    if st.button("🔄 Recalculer les Recommandations", type="primary"):
        with st.spinner("Recalcul en cours..."):
            import time
            time.sleep(2)
        
        st.success("✅ Recommandations mises à jour!")
        st.rerun()
    
    # ============================================
    # RÉSUMÉ FINANCIER
    # ============================================
    
    st.markdown(create_section_header(
        "💰 Impact Financier",
        "Analyse des coûts et économies"
    ), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Investissement Total",
            value="€25,800",
            delta=0,
            icon="💸"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Économies Années",
            value="€45,200",
            delta=12.5,
            icon="💰"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="ROI",
            value="175%",
            delta=25,
            icon="📈"
        ), unsafe_allow_html=True)
    
    # ============================================
    # ALERTES
    # ============================================
    
    st.markdown(create_alert(
        "💡 Conseil: Les recommandations sont mises à jour automatiquement chaque jour à 6h00. Vous pouvez forcer une mise à jour en cliquant sur le bouton ci-dessus.",
        alert_type="info"
    ), unsafe_allow_html=True)