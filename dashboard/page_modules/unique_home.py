"""
🎨 STOKKEL DASHBOARD - Page d'Accueil Unique
==============================================

Design inspiré de Lokad + Vekia + Meilleures startups B2B 2024
- Data-first (pas de marketing fluff)
- Minimaliste fonctionnel
- Identité visuelle unique
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from components.unique_design_system import apply_stokkel_design, create_kpi_card, create_alert, create_section_header

def render(api_client):
    """
    Page d'accueil Dashboard Stokkel - Design Unique
    """
    
    # Appliquer le design system
    st.markdown(apply_stokkel_design(), unsafe_allow_html=True)
    
    # ============================================
    # HEADER HERO (Minimaliste & Impactant)
    # ============================================
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1B4965 0%, #2C6E8C 100%);
            padding: 48px;
            border-radius: 16px;
            margin-bottom: 32px;
            box-shadow: 0 10px 25px rgba(27, 73, 101, 0.2);
        ">
            <div style="display: flex; align-items: center; gap: 24px;">
                <div style="
                    background: white;
                    padding: 20px;
                    border-radius: 16px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                ">
                    <img src="https://api.dicebear.com/7.x/shapes/svg?seed=stokkel&backgroundColor=D2691E,F4A261" 
                         width="64" height="64" style="display: block;">
                </div>
                <div style="flex: 1;">
                    <h1 style="
                        color: white;
                        font-size: 42px;
                        font-weight: 700;
                        margin: 0 0 8px 0;
                        border: none;
                        padding: 0;
                    ">Stokkel</h1>
                    <p style="
                        color: rgba(255,255,255,0.9);
                        font-size: 18px;
                        margin: 0;
                        font-weight: 400;
                    ">
                        IA Prédictive pour l'Optimisation des Stocks
                    </p>
                </div>
                <div style="
                    text-align: right;
                    color: white;
                ">
                    <div style="font-size: 14px; opacity: 0.8; margin-bottom: 4px;">
                        {datetime.now().strftime("%d %B %Y")}
                    </div>
                    <div style="font-size: 12px; opacity: 0.7;">
                        📍 Dakar, Sénégal
                    </div>
                </div>
            </div>
        </div>
    """.format(datetime=datetime), unsafe_allow_html=True)
    
    # ============================================
    # QUICK STATS (KPIs en 4 colonnes)
    # ============================================
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            label="Produits Suivis",
            value="127",
            delta=12,
            icon="📦"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            label="Précision Moyenne",
            value="91.2%",
            delta=3.5,
            icon="🎯"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            label="Économies (30j)",
            value="284K €",
            delta=18,
            icon="💰"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            label="Ruptures Évitées",
            value="43",
            delta=-22,
            icon="✅"
        ), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # ============================================
    # ALERTES CRITIQUES (Style Vekia)
    # ============================================
    
    st.markdown(create_section_header(
        "🚨 Alertes & Actions Prioritaires",
        "Décisions à prendre dans les 24h"
    ), unsafe_allow_html=True)
    
    # Simuler quelques alertes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(create_alert(
            "5 produits en stock critique - Commander maintenant",
            "critical"
        ), unsafe_allow_html=True)
        
        st.markdown(create_alert(
            "12 articles avec demande inhabituelle cette semaine",
            "warning"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_alert(
            "Nouvelle intégration ERP disponible",
            "info"
        ), unsafe_allow_html=True)
        
        st.markdown(create_alert(
            "Prévisions mises à jour pour 87 produits",
            "success"
        ), unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # ============================================
    # TOP PRODUITS À RISQUE (Data Table)
    # ============================================
    
    st.markdown(create_section_header(
        "⚠️ Produits Nécessitant une Attention",
        "Liste prioritaire par impact financier"
    ), unsafe_allow_html=True)
    
    # Simuler données
    data_risque = pd.DataFrame({
        "Produit ID": ["PROD-A127", "PROD-B089", "PROD-C456", "PROD-D234", "PROD-E991"],
        "Nom": [
            "Câble HDMI 2m",
            "Adaptateur USB-C",
            "Souris Sans Fil",
            "Clavier Mécanique",
            "Webcam HD"
        ],
        "Stock Actuel": [12, 28, 8, 45, 3],
        "Point Commande": [50, 80, 35, 60, 25],
        "Prévision 7j": [67, 142, 58, 89, 47],
        "Urgence": ["🔴 Critique", "🔴 Critique", "🟡 Élevée", "🟢 Normale", "🔴 Critique"],
        "Action": ["Commander 120", "Commander 200", "Commander 80", "Surveiller", "Commander 60"],
        "Impact €": ["4,280 €", "6,840 €", "2,150 €", "890 €", "3,940 €"],
    })
    
    # Styled Dataframe
    st.markdown("""
        <style>
        .styled-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .styled-table thead tr {
            background: #1B4965;
            color: white;
        }
        .styled-table th {
            padding: 16px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .styled-table td {
            padding: 14px 16px;
            border-top: 1px solid #E8E8E8;
            font-size: 14px;
        }
        .styled-table tbody tr:hover {
            background: #F4E4D7;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        data_risque,
        use_container_width=True,
        hide_index=True,
    )
    
    # Action rapide
    if st.button("📋 Générer Bons de Commande", type="primary"):
        st.success("✅ 3 bons de commande générés et prêts à être envoyés aux fournisseurs")
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # ============================================
    # PERFORMANCE GLOBALE (Charts Side by Side)
    # ============================================
    
    st.markdown(create_section_header(
        "📊 Performance Globale",
        "Vue d'ensemble des 30 derniers jours"
    ), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mini chart - Taux de service
        st.markdown("""
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
                ">97.8%</div>
                <div style="
                    color: #2A9D8F;
                    font-size: 14px;
                    font-weight: 500;
                ">↑ +2.3% vs. mois dernier</div>
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
        # Mini chart - Taux de rupture
        st.markdown("""
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
                ">2.8%</div>
                <div style="
                    color: #2A9D8F;
                    font-size: 14px;
                    font-weight: 500;
                ">↓ -1.9% vs. mois dernier</div>
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
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # ============================================
    # QUICK ACTIONS (Style Cards)
    # ============================================
    
    st.markdown(create_section_header(
        "⚡ Actions Rapides",
        "Accès direct aux fonctionnalités principales"
    ), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #D2691E 0%, #E8944A 100%);
                padding: 32px 24px;
                border-radius: 12px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(210, 105, 30, 0.2);
            " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 20px rgba(210, 105, 30, 0.3)';" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(210, 105, 30, 0.2)';">
                <div style="font-size: 48px; margin-bottom: 12px;">📊</div>
                <div style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                    Nouvelle Prévision
                </div>
                <div style="color: rgba(255,255,255,0.9); font-size: 13px;">
                    Générer prévisions pour produit
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1B4965 0%, #2C6E8C 100%);
                padding: 32px 24px;
                border-radius: 12px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(27, 73, 101, 0.2);
            " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 20px rgba(27, 73, 101, 0.3)';" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(27, 73, 101, 0.2)';">
                <div style="font-size: 48px; margin-bottom: 12px;">📦</div>
                <div style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                    Recommandations
                </div>
                <div style="color: rgba(255,255,255,0.9); font-size: 13px;">
                    Optimiser approvisionnements
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #F4A261 0%, #E76F51 100%);
                padding: 32px 24px;
                border-radius: 12px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(244, 162, 97, 0.2);
            " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 20px rgba(244, 162, 97, 0.3)';" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(244, 162, 97, 0.2)';">
                <div style="font-size: 48px; margin-bottom: 12px;">📈</div>
                <div style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                    Analytics
                </div>
                <div style="color: rgba(255,255,255,0.9); font-size: 13px;">
                    Tableaux de bord KPIs
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 48px 0;'></div>", unsafe_allow_html=True)
    
    # ============================================
    # FOOTER INFO
    # ============================================
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #F4E4D7 0%, #FFFFFF 100%);
            padding: 32px;
            border-radius: 12px;
            border: 2px solid #E8E8E8;
            text-align: center;
            margin-top: 32px;
        ">
            <div style="color: #1B4965; font-size: 16px; font-weight: 600; margin-bottom: 8px;">
                🚀 Optimisez votre Supply Chain avec l'IA
            </div>
            <div style="color: #6B6B6B; font-size: 14px; margin-bottom: 16px;">
                Stokkel combine prévision probabiliste et optimisation automatique pour maximiser votre rentabilité
            </div>
            <div style="display: flex; justify-content: center; gap: 24px; font-size: 13px; color: #8C8C8C;">
                <span>✨ 127 produits suivis</span>
                <span>|</span>
                <span>📊 91.2% de précision</span>
                <span>|</span>
                <span>💰 284K€ économisés (30j)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # WATERMARK (Subtle)
    # ============================================
    
    st.markdown("""
        <div style="
            text-align: center;
            padding: 24px;
            color: #ADADAD;
            font-size: 12px;
        ">
            Stokkel v1.0.0 | Made with ❤️ in Dakar, Sénégal
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_home_page()