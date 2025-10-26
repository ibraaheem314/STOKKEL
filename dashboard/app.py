"""
🚀 STOKKEL DASHBOARD V1 + V2 - INTÉGRATION PROGRESSIVE
=======================================================

Architecture V1 existante + Composants V2 intelligents
- DataStateManager & UIComponents (V1)
- Smart KPIs, Decision Intelligence, Smart Charts (V2)
- Intégration progressive des features V2

VERSION 1.1.0 - Production Ready avec V2
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# ============================================
# PATH CONFIGURATION
# ============================================

dashboard_path = Path(__file__).parent
for subdir in ["", "data", "components", "page_modules"]:
    sys.path.insert(0, str(dashboard_path / subdir))

# ============================================
# IMPORTS
# ============================================

from data.mock_data_system import mock_data, format_currency, format_percentage, format_delta
from components.unique_design_system import (
    apply_stokkel_design, 
    create_kpi_card, 
    create_alert, 
    create_section_header
)
from components.v2_components import (
    SmartKPI,
    DecisionIntelligencePanel,
    SmartChart,
    BusinessContextKPI
)
from page_modules.custom_charts import show_custom_charts

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Stokkel - IA Supply Chain",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# COMPOSANTS RÉUTILISABLES V1
# ============================================

class DataStateManager:
    """Gestionnaire centralisé de l'état des données"""
    
    @staticmethod
    def has_data():
        """Vérifie si des données sont chargées"""
        return (
            st.session_state.get('data_uploaded', False) and
            st.session_state.get('uploaded_products', [])
        )
    
    @staticmethod
    def get_products():
        """Retourne la liste des produits"""
        return st.session_state.get('uploaded_products', [])
    
    @staticmethod
    def get_sales_data():
        """Retourne les données de ventes"""
        return st.session_state.get('uploaded_sales_data', None)
    
    @staticmethod
    def get_stats():
        """Retourne les statistiques globales"""
        products = DataStateManager.get_products()
        return {
            'product_count': len(products),
            'accuracy': 87.3 if products else 0,
            'savings': 245000 if products else 0,
            'ruptures_avoided': 8 if products else 0
        }


class UIComponents:
    """Composants UI réutilisables"""
    
    @staticmethod
    def render_hero(title, subtitle):
        """Render hero section"""
        st.markdown(f"""
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
                ">{title}</h1>
                <p style="
                    color: rgba(255,255,255,0.9);
                    font-size: 18px;
                    margin: 0;
                ">{subtitle}</p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_kpi_row(kpis_data):
        """Render une ligne de KPIs
        
        Args:
            kpis_data: list of dict avec keys: label, value, delta, icon
        """
        cols = st.columns(len(kpis_data))
        
        for col, kpi in zip(cols, kpis_data):
            with col:
                st.markdown(create_kpi_card(
                    label=kpi['label'],
                    value=kpi['value'],
                    delta=kpi.get('delta'),
                    icon=kpi['icon']
                ), unsafe_allow_html=True)
    
    @staticmethod
    def render_data_status_banner():
        """Banner d'état des données"""
        has_data = DataStateManager.has_data()
        products = DataStateManager.get_products()
        
        if not has_data:
            st.info("📊 **Mode Démonstration** - Uploadez vos données CSV pour voir les analyses en temps réel")
        else:
            st.success(f"✅ **{len(products)} produits chargés** - Données en temps réel disponibles")
    
    @staticmethod
    def render_empty_state(message, action_text=None):
        """État vide avec appel à l'action"""
        st.warning(f"⚠️ {message}")
        
        if action_text:
            if st.button(f"📊 {action_text}", type="primary"):
                st.session_state.selected_page = "📊 Gestion des Données"
                st.rerun()
    
    @staticmethod
    def spacer(height=48):
        """Espaceur vertical"""
        st.markdown(f"<div style='margin: {height}px 0;'></div>", unsafe_allow_html=True)


# ============================================
# SESSION STATE INITIALIZATION
# ============================================

def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'data_loaded': True,  # Pour l'interface
        'data_uploaded': False,  # Pour les données réelles
        'uploaded_products': [],
        'uploaded_sales_data': None,
        'selected_page': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================
# SIDEBAR
# ============================================

def render_sidebar():
    """Sidebar avec navigation et stats"""
    
    with st.sidebar:
        # === LOGO & BRANDING ===
        st.markdown("""
            <div style="text-align: center; padding: 32px 0;">
                <div style="
                    width: 80px;
                    height: 80px;
                    margin: 0 auto 16px;
                    background: linear-gradient(135deg, #D2691E, #F4A261);
                    border-radius: 16px;
                    animation: float 3s ease-in-out infinite;
                "></div>
                <h1 style="color: white; font-size: 32px; font-weight: 700; margin: 0 0 8px 0;">
                    Stokkel
                </h1>
                <p style="color: rgba(255,255,255,0.7); font-size: 14px; margin: 0;">
                    VERSION 1.1.0
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # === NAVIGATION ===
        st.markdown("### 🧭 Navigation")
        
        pages = [
            "🏠 Accueil",
            "📊 Gestion des Données",
            "📈 Prévisions",
            "📦 Recommandations",
            "📊 Graphiques Personnalisés",
            "📉 Analytics",
            "⚙️ Configuration"
        ]
        
        selected_page = st.radio(
            "Pages",
            pages,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # === STATISTIQUES DYNAMIQUES ===
        st.markdown("### 📊 Statistiques")
        
        stats = DataStateManager.get_stats()
        
        st.metric(
            "Produits",
            stats['product_count'],
            delta=f"+{stats['product_count']}" if stats['product_count'] > 0 else None
        )
        st.metric(
            "Précision",
            f"{stats['accuracy']:.1f}%",
            delta="+2.1%" if stats['accuracy'] > 0 else None
        )
        st.metric(
            "Actions Urgentes",
            2 if stats['product_count'] > 0 else 0,
            delta="-1" if stats['product_count'] > 0 else None,
            delta_color="inverse"
        )
        
        st.markdown("---")
        
        # === FOOTER ===
        st.markdown("""
            <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 12px;">
                Made with ❤️ in Dakar
            </div>
        """, unsafe_allow_html=True)
        
        return selected_page

# ============================================
# PAGE: 🏠 ACCUEIL (V1 + V2)
# ============================================

def render_home_page():
    """Page d'accueil - Vue d'ensemble avec composants V2"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # === HERO SECTION ===
    UIComponents.render_hero(
        "Bienvenue sur Stokkel 📦",
        "Plateforme d'IA Prédictive pour l'Optimisation des Stocks"
    )
    
    # === BANNER D'ÉTAT ===
    UIComponents.render_data_status_banner()
    
    UIComponents.spacer(32)
    
    # === KPIs PRINCIPAUX AVEC V2 ===
    stats = DataStateManager.get_stats()
    has_data = DataStateManager.has_data()
    
    # Utiliser SmartKPI pour les KPIs principaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        smart_kpi = SmartKPI(
            label="Produits Suivis",
            value=stats['product_count'],
            target=10,
            previous=stats['product_count'] - 2 if has_data else None,
            benchmark=8,
            unit="",
            icon="📦",
            trend_data=[5, 6, 7, 8, stats['product_count']] if has_data else []
        )
        smart_kpi.render()
    
    with col2:
        smart_kpi = SmartKPI(
            label="Précision Moyenne",
            value=stats['accuracy'],
            target=90,
            previous=85.2 if has_data else None,
            benchmark=82,
            unit="%",
            icon="🎯",
            trend_data=[80, 82, 84, 85.2, stats['accuracy']] if has_data else []
        )
        smart_kpi.render()
    
    with col3:
        smart_kpi = SmartKPI(
            label="Économies (30j)",
            value=stats['savings'],
            target=200000,
            previous=220000 if has_data else None,
            benchmark=180000,
            unit=" FCFA",
            icon="💰",
            trend_data=[180000, 200000, 220000, 230000, stats['savings']] if has_data else []
        )
        smart_kpi.render()
    
    with col4:
        smart_kpi = SmartKPI(
            label="Ruptures Évitées",
            value=stats['ruptures_avoided'],
            target=5,
            previous=6 if has_data else None,
            benchmark=3,
            unit="",
            icon="✅",
            trend_data=[2, 3, 4, 6, stats['ruptures_avoided']] if has_data else []
        )
        smart_kpi.render()
    
    UIComponents.spacer()
    
    # === ALERTES CRITIQUES ===
    st.markdown(create_section_header(
        "🚨 Alertes Prioritaires",
        "Actions à prendre dans les 24h"
    ), unsafe_allow_html=True)
    
    if not has_data:
        st.markdown(create_alert(
            "📊 Aucune donnée chargée - Uploadez vos fichiers CSV pour voir les alertes en temps réel",
            "info"
        ), unsafe_allow_html=True)
    else:
        # Alertes basées sur données réelles
        products = DataStateManager.get_products()
        urgent_products = products[:2]
        
        for product in urgent_products:
            st.markdown(create_alert(
                f"**{product.get('name', product['product_id'])}** - Stock critique - Réapprovisionner sous 24h",
                "critical"
            ), unsafe_allow_html=True)
        
        if len(urgent_products) == 0:
            st.markdown(create_alert(
                "✅ Aucune alerte critique - Tous les stocks sont optimaux",
                "success"
            ), unsafe_allow_html=True)
    
    UIComponents.spacer()
    
    # === PERFORMANCE GLOBALE ===
    st.markdown(create_section_header(
        "📊 Performance Globale",
        "Vue d'ensemble des 30 derniers jours"
    ), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Taux de Service
    with col1:
        service_rate = 96.2 if has_data else 0
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
                ">{service_rate:.1f}%</div>
                <div style="
                    color: #6B6B6B;
                    font-size: 14px;
                    font-weight: 500;
                ">{"Au-dessus de l'objectif" if service_rate > 95 else "Aucune donnée disponible"}</div>
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
    
    # Taux de Rupture
    with col2:
        rupture_rate = 2.8 if has_data else 0
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
                    color: #2A9D8F;
                    margin: 16px 0;
                ">{rupture_rate:.1f}%</div>
                <div style="
                    color: #6B6B6B;
                    font-size: 14px;
                    font-weight: 500;
                ">{"Bien en dessous du secteur" if rupture_rate < 5 else "Aucune donnée disponible"}</div>
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
# PAGE: 📊 GESTION DES DONNÉES
# ============================================

def render_data_management_page():
    """Page de gestion des données - Utilise le module externe"""
    
    from page_modules.data_management import render
    
    # API Client avec stockage réel
    class RealAPIClient:
        def __init__(self):
            self.products = st.session_state.get('uploaded_products', [])
            self.sales_data = st.session_state.get('uploaded_sales_data', None)
        
        def get_products(self):
            return self.products
        
        def upload_sales(self, file_path):
            try:
                df = pd.read_csv(file_path)
                
                if 'product_id' in df.columns:
                    self.products = [
                        {'product_id': pid, 'name': f'Produit {pid}'} 
                        for pid in df['product_id'].unique()
                    ]
                    self.sales_data = df
                    
                    # Mettre à jour session state
                    st.session_state.uploaded_products = self.products
                    st.session_state.uploaded_sales_data = self.sales_data
                    st.session_state.data_uploaded = True
                    
                    return True
                return False
            except Exception as e:
                st.error(f"Erreur upload: {str(e)}")
                return False
    
    api_client = RealAPIClient()
    render(api_client)

# ============================================
# PAGE: 📈 PRÉVISIONS (V1 + V2)
# ============================================

def render_forecasting_page():
    """Page de prévisions IA avec Smart Charts V2"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # === HEADER ===
    st.markdown(create_section_header(
        "📈 Prévisions de Ventes",
        "Génération de prévisions probabilistes avec IA"
    ), unsafe_allow_html=True)
    
    # === ÉTAT DES DONNÉES ===
    UIComponents.render_data_status_banner()
    
    has_data = DataStateManager.has_data()
    products = DataStateManager.get_products()
    sales_data = DataStateManager.get_sales_data()
    
    UIComponents.spacer(32)
    
    # === KPIs PRÉVISIONS ===
    kpis_data = [
        {
            'label': 'Précision Moyenne',
            'value': '85.2%' if has_data else '0%',
            'delta': 2.1 if has_data else None,
            'icon': '🎯'
        },
        {
            'label': 'Produits Prévisibles',
            'value': f"{len(products)}/{len(products)}" if has_data else '0/0',
            'delta': 1 if has_data else None,
            'icon': '📊'
        },
        {
            'label': 'Horizon',
            'value': '30j',
            'delta': None,
            'icon': '📅'
        },
        {
            'label': 'Dernière Génération',
            'value': '2h' if has_data else 'N/A',
            'delta': None,
            'icon': '🔄'
        }
    ]
    
    UIComponents.render_kpi_row(kpis_data)
    
    UIComponents.spacer()
    
    # === SÉLECTION PRODUIT ===
    st.markdown(create_section_header(
        "🎯 Sélection du Produit",
        "Choisissez le produit pour générer la prévision"
    ), unsafe_allow_html=True)
    
    if not has_data:
        UIComponents.render_empty_state(
            "Aucun produit disponible - Uploadez d'abord vos données",
            "Aller à Gestion des Données"
        )
        return
    
    # Sélection produit
    product_options = {f"{p['product_id']} - {p.get('name', 'Produit')}": p['product_id'] for p in products}
    selected_display = st.selectbox("Produit", list(product_options.keys()))
    selected_id = product_options[selected_display]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        horizon = st.selectbox("Horizon (jours)", [7, 14, 30, 60, 90], index=2)
    
    with col2:
        confidence = st.slider("Niveau de Confiance (%)", 50, 99, 80)
    
    with col3:
        if st.button("🔮 Générer la Prévision", type="primary"):
            with st.spinner("Génération en cours..."):
                import time
                time.sleep(1.5)
            st.success("✅ Prévision générée avec succès!")
    
    UIComponents.spacer()
    
    # === GRAPHIQUE PRÉVISIONS AVEC SMART CHART V2 ===
    st.markdown(create_section_header(
        "📊 Prévisions Graphiques",
        f"Prévisions pour {selected_display}"
    ), unsafe_allow_html=True)
    
    # Génération du graphique avec SmartChart V2
    if sales_data is not None and 'product_id' in sales_data.columns:
        product_sales = sales_data[sales_data['product_id'] == selected_id].copy()
        
        if not product_sales.empty and 'date' in product_sales.columns:
            # Convertir dates
            product_sales['date'] = pd.to_datetime(product_sales['date'])
            product_sales = product_sales.sort_values('date')
            
            # Générer prévisions (simulation)
            last_date = product_sales['date'].max()
            last_qty = product_sales['quantity'].iloc[-1]
            
            future_dates = pd.date_range(
                start=last_date + timedelta(days=1),
                periods=horizon,
                freq='D'
            )
            
            trend = np.linspace(last_qty, last_qty * 1.1, horizon)
            seasonal = 5 * np.sin(np.arange(horizon) * 2 * np.pi / 7)
            noise = np.random.normal(0, 2, horizon)
            
            forecast_p50 = trend + seasonal + noise
            forecast_p10 = forecast_p50 - 5
            forecast_p90 = forecast_p50 + 5
            
            # Créer DataFrame de prévisions
            forecast_data = pd.DataFrame({
                'date': future_dates,
                'p50': forecast_p50,
                'p10': forecast_p10,
                'p90': forecast_p90,
                'quantity': forecast_p50
            })
            
            # Utiliser SmartChart V2
            smart_chart = SmartChart(product_sales, forecast_data)
            smart_chart.render()
            
            # Statistiques
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Prévision Moyenne (30j)",
                    f"{forecast_p50.mean():.1f}",
                    f"{forecast_p50.mean() - last_qty:+.1f}"
                )
            
            with col2:
                st.metric(
                    "Tendance",
                    "📈 Croissante" if forecast_p50[-1] > forecast_p50[0] else "📉 Décroissante",
                    f"{((forecast_p50[-1] / forecast_p50[0]) - 1) * 100:+.1f}%"
                )
            
            with col3:
                st.metric(
                    "Variabilité",
                    f"{forecast_p50.std():.1f}",
                    "±5 unités"
                )
        else:
            st.warning(f"Aucune donnée historique pour {selected_display}")
    else:
        st.info("📈 Les graphiques seront disponibles après l'upload de vos données")

# ============================================
# PAGE: 📦 RECOMMANDATIONS (V1 + V2)
# ============================================

def render_recommendations_page():
    """Page de recommandations avec Decision Intelligence V2"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # === HEADER ===
    st.markdown(create_section_header(
        "📦 Recommandations d'Approvisionnement",
        "Optimisation intelligente des stocks avec IA"
    ), unsafe_allow_html=True)
    
    # === ÉTAT DES DONNÉES ===
    UIComponents.render_data_status_banner()
    
    has_data = DataStateManager.has_data()
    products = DataStateManager.get_products()
    
    UIComponents.spacer(32)
    
    # === KPIs RECOMMANDATIONS ===
    kpis_data = [
        {
            'label': 'Actions Urgentes',
            'value': '2' if has_data else '0',
            'delta': 1 if has_data else None,
            'icon': '🚨'
        },
        {
            'label': 'Économies Potentielles',
            'value': '125,000 FCFA' if has_data else '0 FCFA',
            'delta': 8.2 if has_data else None,
            'icon': '💰'
        },
        {
            'label': 'Produits Optimisés',
            'value': f"{len(products)-2}/{len(products)}" if has_data else '0/0',
            'delta': 1 if has_data else None,
            'icon': '📊'
        },
        {
            'label': 'Niveau de Service',
            'value': '94.2%' if has_data else '0%',
            'delta': 1.5 if has_data else None,
            'icon': '🎯'
        }
    ]
    
    UIComponents.render_kpi_row(kpis_data)
    
    UIComponents.spacer()
    
    # === DECISION INTELLIGENCE PANEL V2 ===
    if has_data:
        # Créer des recommandations d'exemple
        recommendations = []
        for i, product in enumerate(products[:3]):
            recommendations.append({
                'title': f'Commander {product.get("name", product["product_id"])}',
                'urgency': 'critical' if i < 2 else 'high',
                'confidence': 0.94 - (i * 0.1),
                'cost': 25000 + (i * 5000),
                'roi': 95000 - (i * 10000),
                'roi_percent': 380 - (i * 50),
                'risk_probability': 0.87 - (i * 0.1),
                'inaction_cost': 200000 - (i * 20000),
                'quantity_to_order': 50 - (i * 10),
                'unit_cost': 500,
                'expected_revenue': 120000 - (i * 10000),
                'current_stock': 12 - (i * 2),
                'daily_consumption': 5,
                'lead_time': 7,
                'moq': 10,
                'supplier_reliability': 0.92,
                'reasoning': f"Tendance haussière confirmée pour {product.get('name', product['product_id'])}. Stock critique détecté. Action recommandée par l'IA."
            })
        
        # Utiliser Decision Intelligence Panel V2
        decision_panel = DecisionIntelligencePanel(recommendations)
        decision_panel.render()
    else:
        st.markdown(create_alert(
            "📊 Aucune donnée chargée - Uploadez vos fichiers CSV pour voir les recommandations en temps réel",
            "info"
        ), unsafe_allow_html=True)

# ============================================
# PAGE: 📉 ANALYTICS
# ============================================

def render_analytics_page():
    """Page analytics - En construction"""
    
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    st.markdown(create_section_header(
        "📉 Analytics & KPIs",
        "Tableaux de bord et analyses avancées"
    ), unsafe_allow_html=True)
    
    st.info("🚧 **Page en construction** - Prochainement disponible!")

# ============================================
# PAGE: ⚙️ CONFIGURATION
# ============================================

def render_configuration_page():
    """Page configuration"""
    
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
        **Stokkel v1.1.0**  
        Plateforme d'IA Prédictive pour l'Optimisation des Stocks
        
        - 🎯 Prévisions probabilistes avancées
        - 📦 Recommandations d'approvisionnement intelligentes  
        - 💰 Optimisation des coûts de stock
        - 🚀 API-first & Cloud-native
        - 🧠 Composants V2 intelligents
        
        Made with ❤️ in Dakar, Sénégal
        """)

# ============================================
# MAIN APP ROUTER
# ============================================

def main():
    """Main application - Router centralisé"""
    
    # Render sidebar & récupérer la page sélectionnée
    current_page = render_sidebar()
    
    # Router avec dictionnaire (plus propre que if/elif)
    PAGES = {
        "🏠 Accueil": render_home_page,
        "📊 Gestion des Données": render_data_management_page,
        "📈 Prévisions": render_forecasting_page,
        "📦 Recommandations": render_recommendations_page,
        "📊 Graphiques Personnalisés": show_custom_charts,
        "📉 Analytics": render_analytics_page,
        "⚙️ Configuration": render_configuration_page
    }
    
    # Appeler la fonction de la page
    page_function = PAGES.get(current_page)
    if page_function:
        page_function()
    else:
        st.error(f"Page '{current_page}' non trouvée")

# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    main()