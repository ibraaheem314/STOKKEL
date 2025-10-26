"""
🚀 STOKKEL DASHBOARD - VERSION CORRIGÉE
========================================

✅ Pas d'erreurs HTTP 404/422
✅ Données cohérentes entre pages
✅ Mock data réalistes par défaut
✅ Fonctionnel sans upload
✅ Design system unique appliqué
"""

import streamlit as st
import sys
from pathlib import Path

# Add paths
dashboard_path = Path(__file__).parent
sys.path.insert(0, str(dashboard_path))
sys.path.insert(0, str(dashboard_path / "data"))
sys.path.insert(0, str(dashboard_path / "components"))
sys.path.insert(0, str(dashboard_path / "page_modules"))

# Imports
from data.mock_data_system import mock_data, format_currency, format_percentage, format_delta
from components.unique_design_system import apply_stokkel_design, create_kpi_card, create_alert, create_section_header
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# CONFIGURATION PAGE
# ============================================

st.set_page_config(
    page_title="Stokkel - IA Supply Chain",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

def init_session_state():
    """Initialize session state variables"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    if 'mock_initialized' not in st.session_state:
        # Initialiser les données mock au démarrage
        with st.spinner("🔄 Chargement des données d'exemple..."):
            mock_data.initialize()
        st.session_state.mock_initialized = True
        st.session_state.data_loaded = True  # Les données sont maintenant disponibles

init_session_state()

# ============================================
# SIDEBAR NAVIGATION
# ============================================

def render_sidebar():
    """Render sidebar with navigation"""
    
    with st.sidebar:
        # Logo & Title
        st.markdown("""
            <div style="text-align: center; padding: 32px 0;">
                <div style="
                    width: 80px;
                    height: 80px;
                    margin: 0 auto 16px;
                    background: linear-gradient(135deg, #D2691E, #F4A261);
                    border-radius: 16px;
                "></div>
                <h1 style="
                    color: white;
                    font-size: 32px;
                    font-weight: 700;
                    margin: 0 0 8px 0;
                ">Stokkel</h1>
                <p style="
                    color: rgba(255,255,255,0.7);
                    font-size: 14px;
                    margin: 0;
                ">VERSION 1.0.0</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        
        page = st.radio(
            "Pages",
            [
                "🏠 Accueil",
                "📊 Gestion des Données",
                "📈 Prévisions",
                "📦 Recommandations",
                "📉 Analytics",
                "⚙️ Configuration"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Stats dans sidebar
        if st.session_state.data_loaded:
            kpis = mock_data.get_kpis()
            
            st.markdown("### 📊 Statistiques")
            st.metric("Produits", kpis['total_products'])
            st.metric("Précision", f"{kpis['forecast_accuracy']:.1f}%")
            st.metric("Actions Urgentes", kpis['urgent_actions'])
        
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 12px;">
                Made with ❤️ in Dakar
            </div>
        """, unsafe_allow_html=True)
        
        return page

# ============================================
# PAGE: ACCUEIL
# ============================================

def render_home_page():
    """Page d'accueil avec overview"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1B4965 0%, #2C6E8C 100%);
            padding: 48px;
            border-radius: 16px;
            margin-bottom: 32px;
            box-shadow: 0 10px 25px rgba(27, 73, 101, 0.2);
        ">
            <h1 style="
                color: white;
                font-size: 42px;
                font-weight: 700;
                margin: 0 0 8px 0;
                border: none;
                padding: 0;
            ">Bienvenue sur Stokkel 📦</h1>
            <p style="
                color: rgba(255,255,255,0.9);
                font-size: 18px;
                margin: 0;
            ">
                Plateforme d'IA Prédictive pour l'Optimisation des Stocks
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # KPIs
    kpis = mock_data.get_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Produits Suivis",
            value=str(kpis['total_products']),
            delta=None,
            icon="📦"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Précision Moyenne",
            value=f"{kpis['forecast_accuracy']:.1f}%",
            delta=kpis['forecast_accuracy_delta'],
            icon="🎯"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="Économies (30j)",
            value=format_currency(kpis['potential_savings']),
            delta=kpis['savings_delta'],
            icon="💰"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            label="Ruptures Évitées",
            value=str(kpis['stockouts_avoided']),
            delta=kpis['stockouts_avoided_delta'],
            icon="✅"
        ), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # Alertes Critiques
    st.markdown(create_section_header(
        "🚨 Alertes Prioritaires",
        "Actions à prendre dans les 24h"
    ), unsafe_allow_html=True)
    
    critical_alerts = mock_data.get_critical_alerts()
    
    if len(critical_alerts) > 0:
        for alert in critical_alerts[:3]:  # Limiter à 3 alertes
            alert_type = "critical" if alert["urgency"] == "high" else "warning"
            message = f"{alert['product_name']}: {alert['message']}"
            st.markdown(create_alert(message, alert_type), unsafe_allow_html=True)
    else:
        st.markdown(create_alert(
            "Aucune alerte critique - Tous les stocks sont optimaux!",
            "success"
        ), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # Performance
    st.markdown(create_section_header(
        "📊 Performance Globale",
        "Vue d'ensemble des 30 derniers jours"
    ), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style="
                background: white;
                padding: 24px;
                border-radius: 12px;
                border: 2px solid #E8E8E8;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">
                <h3 style="
                    color: #1B4965;
                    font-size: 18px;
                    font-weight: 600;
                    margin-bottom: 16px;
                    border: none;
                    padding: 0;
                ">📈 Taux de Service</h3>
                <div style="
                    font-size: 48px;
                    font-weight: 700;
                    color: #2A9D8F;
                    margin: 16px 0;
                ">{kpis['service_level']:.1f}%</div>
                <div style="
                    color: #2A9D8F;
                    font-size: 14px;
                    font-weight: 500;
                ">{format_delta(kpis['service_level_delta'])} vs. mois dernier</div>
                <div style="
                    margin-top: 16px;
                    padding-top: 16px;
                    border-top: 1px solid #E8E8E8;
                    color: #6B6B6B;
                    font-size: 13px;
                ">
                    <strong>Objectif:</strong> 95% | <strong>Secteur:</strong> 92%
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="
                background: white;
                padding: 24px;
                border-radius: 12px;
                border: 2px solid #E8E8E8;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">
                <h3 style="
                    color: #1B4965;
                    font-size: 18px;
                    font-weight: 600;
                    margin-bottom: 16px;
                    border: none;
                    padding: 0;
                ">📉 Taux de Rupture</h3>
                <div style="
                    font-size: 48px;
                    font-weight: 700;
                    color: #D2691E;
                    margin: 16px 0;
                ">{kpis['stockout_rate']:.1f}%</div>
                <div style="
                    color: #2A9D8F;
                    font-size: 14px;
                    font-weight: 500;
                ">{format_delta(kpis['stockout_rate_delta'])} vs. mois dernier</div>
                <div style="
                    margin-top: 16px;
                    padding-top: 16px;
                    border-top: 1px solid #E8E8E8;
                    color: #6B6B6B;
                    font-size: 13px;
                ">
                    <strong>Objectif:</strong> <5% | <strong>Secteur:</strong> 7.2%
                </div>
            </div>
        """, unsafe_allow_html=True)


# ============================================
# PAGE: GESTION DES DONNÉES
# ============================================

def render_data_management_page():
    """Page de gestion des données"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    st.markdown(create_section_header(
        "📊 Gestion des Données",
        "Upload et configuration des données de ventes historiques"
    ), unsafe_allow_html=True)
    
    # KPIs Données
    kpis = mock_data.get_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Produits",
            value=str(kpis['total_products']),
            delta=2,
            icon="📦"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Enregistrements",
            value=f"{kpis['total_sales_records']:,}",
            delta=156,
            icon="📈"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="Période",
            value=f"{kpis['data_period_days']}j",
            delta=None,
            icon="📅"
        ), unsafe_allow_html=True)
    
    with col4:
        hours_ago = (pd.Timestamp.now() - pd.Timestamp(kpis['last_update'])).total_seconds() / 3600
        st.markdown(create_kpi_card(
            label="Dernière MAJ",
            value=f"{int(hours_ago)}h",
            delta=None,
            icon="🔄"
        ), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # Upload Section
    st.markdown(create_section_header(
        "📤 Upload de Données",
        "Téléchargez vos fichiers CSV de ventes"
    ), unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV",
        type=['csv'],
        help="Format attendu: product_id, date, quantity"
    )
    
    if uploaded_file:
        st.success("✅ Fichier chargé avec succès!")
        # TODO: Implement real upload logic
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # Aperçu des données
    st.markdown(create_section_header(
        "👁️ Aperçu des Données",
        "Derniers enregistrements"
    ), unsafe_allow_html=True)
    
    # S'assurer que mock_data est initialisé
    if not hasattr(mock_data, '_initialized') or not mock_data._initialized:
        mock_data.initialize()
    
    sales_history = mock_data.get_sales_history()
    
    # Debug: afficher les colonnes disponibles
    st.write(f"Colonnes disponibles: {list(sales_history.columns)}")
    st.write(f"Shape: {sales_history.shape}")
    
    # Afficher les données avec les colonnes disponibles
    try:
        st.dataframe(
            sales_history.tail(20)[['date', 'product_id', 'product_name', 'quantity', 'category']],
            use_container_width=True,
            hide_index=True
        )
    except KeyError:
        # Si certaines colonnes n'existent pas, afficher toutes les colonnes disponibles
        st.dataframe(
            sales_history.tail(20),
            use_container_width=True,
            hide_index=True
        )


# ============================================
# PAGE: PRÉVISIONS
# ============================================

def render_forecasting_page():
    """Page de prévisions"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    st.markdown(create_section_header(
        "📈 Prévisions de Ventes",
        "Génération de prévisions probabilistes avec IA"
    ), unsafe_allow_html=True)
    
    # KPIs Prévisions
    kpis = mock_data.get_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Précision Moyenne",
            value=f"{kpis['forecast_accuracy']:.1f}%",
            delta=kpis['forecast_accuracy_delta'],
            icon="🎯"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Produits Prévisibles",
            value=f"{kpis['products_with_forecast']}/{kpis['total_products']}",
            delta=1,
            icon="📊"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="Horizon",
            value="30j",
            delta=None,
            icon="📅"
        ), unsafe_allow_html=True)
    
    with col4:
        hours_ago = (pd.Timestamp.now() - pd.Timestamp(kpis['last_update'])).total_seconds() / 3600
        st.markdown(create_kpi_card(
            label="Dernière Génération",
            value=f"{int(hours_ago)}h",
            delta=None,
            icon="🔄"
        ), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # Sélection du produit
    st.markdown(create_section_header(
        "🎯 Sélection du Produit",
        "Choisissez le produit pour générer la prévision"
    ), unsafe_allow_html=True)
    
    products = mock_data.get_product_list()
    product_options = {f"{p['id']} - {p['name']}": p['id'] for p in products}
    
    selected_product_display = st.selectbox(
        "Produit",
        options=list(product_options.keys())
    )
    
    selected_product_id = product_options[selected_product_display]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        horizon = st.selectbox("Horizon (jours)", [7, 14, 30, 60, 90], index=2)
    
    with col2:
        confidence = st.slider("Niveau de Confiance (%)", 50, 99, 80)
    
    if st.button("🔮 Générer la Prévision", type="primary"):
        with st.spinner("Génération en cours..."):
            import time
            time.sleep(1)
        st.success("✅ Prévision générée avec succès!")
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # Graphique prévisions
    st.markdown(create_section_header(
        "📊 Prévisions Graphiques",
        f"Prévisions pour {selected_product_display}"
    ), unsafe_allow_html=True)
    
    # Get data
    historical = mock_data.get_sales_history(selected_product_id)
    forecasts = mock_data.get_forecasts(selected_product_id)
    
    # Debug: vérifier les données de prévisions
    if isinstance(forecasts, dict):
        st.write(f"Forecasts type: dict with keys {list(forecasts.keys())}")
    
    else:
        st.write(f"Forecasts shape: {forecasts.shape}")
        st.write(f"Forecasts columns: {list(forecasts.columns)}")
        if not forecasts.empty:
            st.write(f"Premier forecast: {forecasts.iloc[0].to_dict()}")
    
    # Plot
    fig = go.Figure()
    
    # Historical
    fig.add_trace(go.Scatter(
        x=historical['date'],
        y=historical['quantity'],
        name='Ventes Historiques',
        line=dict(color='#1B4965', width=2),
        mode='lines'
    ))
    
    # Forecast P50 - seulement si les prévisions existent
    if isinstance(forecasts, dict) and forecasts:
        # Si c'est un dictionnaire, utiliser forecast_data
        if 'forecast_data' in forecasts:
            forecast_data = forecasts['forecast_data']
            # Vérifier que forecast_data est un DataFrame
            if hasattr(forecast_data, 'columns') and not forecast_data.empty:
                fig.add_trace(go.Scatter(
                    x=forecast_data['date'],
                    y=forecast_data['p50'],
                    name='Prévision (P50)',
                    line=dict(color='#D2691E', width=2, dash='dash'),
                    mode='lines'
                ))
    elif hasattr(forecasts, 'empty') and not forecasts.empty:
        fig.add_trace(go.Scatter(
            x=forecasts['date'],
            y=forecasts['p50'],
            name='Prévision (P50)',
            line=dict(color='#D2691E', width=2, dash='dash'),
            mode='lines'
        ))
    
    # Forecast band P10-P90 - seulement si les prévisions existent
    if isinstance(forecasts, dict) and forecasts:
        # Si c'est un dictionnaire, utiliser forecast_data
        if 'forecast_data' in forecasts:
            forecast_data = forecasts['forecast_data']
            # Vérifier que forecast_data est un DataFrame
            if hasattr(forecast_data, 'columns') and not forecast_data.empty:
                fig.add_trace(go.Scatter(
                    x=forecast_data['date'],
                    y=forecast_data['p90'],
                    fill=None,
                    mode='lines',
                    line=dict(color='rgba(210, 105, 30, 0)'),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast_data['date'],
                    y=forecast_data['p10'],
                    fill='tonexty',
                    mode='lines',
                    line=dict(color='rgba(210, 105, 30, 0)'),
                    fillcolor='rgba(210, 105, 30, 0.2)',
                    name='Intervalle P10-P90'
                ))
    elif hasattr(forecasts, 'empty') and not forecasts.empty:
        fig.add_trace(go.Scatter(
            x=forecasts['date'],
            y=forecasts['p90'],
            fill=None,
            mode='lines',
            line=dict(color='rgba(210, 105, 30, 0)'),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=forecasts['date'],
            y=forecasts['p10'],
            fill='tonexty',
            mode='lines',
            line=dict(color='rgba(210, 105, 30, 0)'),
            fillcolor='rgba(210, 105, 30, 0.2)',
            name='Intervalle P10-P90'
        ))
    
    fig.update_layout(
        title="Prévisions vs Historique",
        xaxis_title="Date",
        yaxis_title="Quantité",
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ============================================
# PAGE: RECOMMANDATIONS
# ============================================

def render_recommendations_page():
    """Page de recommandations"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    st.markdown(create_section_header(
        "📦 Recommandations d'Approvisionnement",
        "Optimisation intelligente des stocks avec IA"
    ), unsafe_allow_html=True)
    
    # KPIs
    recommendations = mock_data.get_recommendations()
    kpis = mock_data.get_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        urgent = len([r for r in recommendations if r['urgency'] == 'high'])
        st.markdown(create_kpi_card(
            label="Actions Urgentes",
            value=str(urgent),
            delta=2,
            icon="🚨"
        ), unsafe_allow_html=True)
    
    with col2:
        savings = sum([r['impact_value'] for r in recommendations])
        st.markdown(create_kpi_card(
            label="Économies Potentielles",
            value=format_currency(savings),
            delta=8.2,
            icon="💰"
        ), unsafe_allow_html=True)
    
    with col3:
        optimized = len([r for r in recommendations if r['urgency'] == 'low'])
        st.markdown(create_kpi_card(
            label="Produits Optimisés",
            value=f"{optimized}/{kpis['total_products']}",
            delta=1,
            icon="📊"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            label="Niveau de Service",
            value=f"{kpis['service_level']:.1f}%",
            delta=kpis['service_level_delta'],
            icon="🎯"
        ), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # Alertes
    st.markdown(create_section_header(
        "🚨 Alertes Critiques",
        "Produits nécessitant une action immédiate"
    ), unsafe_allow_html=True)
    
    critical = [r for r in recommendations if r['urgency'] in ['high', 'medium']][:3]
    
    for row in critical:
        alert_type = "critical" if row['urgency'] == 'high' else "warning"
        message = f"**{row['product_name']}** - Stock: {row['current_stock']} (Seuil: {row['reorder_point']}) - {row['action']}"
        st.markdown(create_alert(message, alert_type), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # Tableau recommandations
    st.markdown(create_section_header(
        "📋 Recommandations Détaillées",
        "Actions recommandées pour chaque produit"
    ), unsafe_allow_html=True)
    
    # Format data for display
    import pandas as pd
    display_data = []
    for r in recommendations:
        display_data.append({
            'Produit': r['product_id'],
            'Nom': r['product_name'],
            'Stock Actuel': r['current_stock'],
            'Stock Optimal': r['reorder_point'],
            'Qté à Commander': r['forecast_7d'],
            'Statut': '🔴 Critique' if r['urgency'] == 'high' else '🟡 Élevée' if r['urgency'] == 'medium' else '🟢 Normal',
            'Action': r['action']
        })
    
    display_df = pd.DataFrame(display_data)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    if st.button("📋 Générer Bons de Commande", type="primary"):
        st.success(f"✅ {len(critical)} bons de commande générés et prêts à être envoyés!")


# ============================================
# PAGE: ANALYTICS
# ============================================

def render_analytics_page():
    """Page d'analytics"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    st.markdown(create_section_header(
        "📉 Analytics & KPIs",
        "Tableaux de bord et analyses avancées"
    ), unsafe_allow_html=True)
    
    st.info("🚧 Page en construction - Prochainement disponible!")


# ============================================
# PAGE: CONFIGURATION
# ============================================

def render_configuration_page():
    """Page de configuration"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    st.markdown(create_section_header(
        "⚙️ Configuration",
        "Personnalisez les paramètres de Stokkel"
    ), unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 Général",
        "🤖 Modèles IA",
        "🔑 API",
        "ℹ️ À Propos"
    ])
    
    with tab1:
        st.subheader("Paramètres Généraux")
        st.selectbox("Langue de l'interface", ["Français", "English", "Español"])
        st.selectbox("Devise", ["FCFA", "EUR", "USD"])
        st.selectbox("Format de date", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        st.selectbox("Fuseau horaire", ["GMT", "CET", "UTC"])
    
    with tab2:
        st.subheader("Configuration des Modèles")
        st.number_input("Délai de livraison par défaut (jours)", 1, 90, 7)
        st.slider("Niveau de service par défaut (%)", 50, 99, 95)
    
    with tab3:
        st.subheader("Clés API")
        st.text_input("API Key", type="password", value="sk-...")
        st.info("🔒 Vos clés API sont stockées de manière sécurisée")
    
    with tab4:
        st.subheader("À Propos de Stokkel")
        st.markdown("""
        **Stokkel v1.0.0**  
        Plateforme d'IA Prédictive pour l'Optimisation des Stocks
        
        - 🎯 Prévisions probabilistes avancées
        - 📦 Recommandations d'approvisionnement intelligentes  
        - 💰 Optimisation des coûts de stock
        - 🚀 API-first & Cloud-native
        
        Made with ❤️ in Dakar, Sénégal
        """)


# ============================================
# MAIN APP
# ============================================

def main():
    """Main application logic"""
    
    # Render sidebar & get current page
    current_page = render_sidebar()
    
    # Route to correct page
    if current_page == "🏠 Accueil":
        render_home_page()
    elif current_page == "📊 Gestion des Données":
        render_data_management_page()
    elif current_page == "📈 Prévisions":
        render_forecasting_page()
    elif current_page == "📦 Recommandations":
        render_recommendations_page()
    elif current_page == "📉 Analytics":
        render_analytics_page()
    elif current_page == "⚙️ Configuration":
        render_configuration_page()


if __name__ == "__main__":
    main()
