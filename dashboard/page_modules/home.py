"""
Page d'accueil - Vue d'ensemble de Stokkel
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from components.styles import render_page_header, render_metric_card


def render(api_client):
    """Render la page d'accueil"""
    
    # Hero section moderne
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 4rem 2rem;
            border-radius: 2rem;
            text-align: center;
            color: white;
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
        ">
            <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: float 8s ease-in-out infinite;"></div>
            <div style="position: relative; z-index: 2;">
                <h1 style="font-size: 3.5rem; font-weight: 800; margin: 0 0 1rem 0; font-family: 'Poppins', sans-serif; text-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                    Stokkel
                </h1>
                <p style="font-size: 1.3rem; margin: 0 0 2rem 0; opacity: 0.95; font-weight: 400; max-width: 600px; margin-left: auto; margin-right: auto;">
                    L'IA qui révolutionne la gestion des stocks pour les entreprises africaines
                </p>
                <div style="display: inline-flex; align-items: center; background: rgba(255,255,255,0.2); padding: 0.8rem 2rem; border-radius: 50px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3);">
                    <span style="margin-right: 0.5rem;">🚀</span>
                    <span style="font-weight: 600;">MVP Version 1.0</span>
                </div>
            </div>
        </div>
        <style>
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(180deg); }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Section hero avec cards ultra-modernes
    st.markdown("""
        <div style="margin-bottom: 3rem;">
            <p style="
                text-align: center;
                font-size: 1.125rem;
                color: #6b7280;
                max-width: 700px;
                margin: 0 auto 2rem auto;
                line-height: 1.8;
                animation: fadeInUp 0.6s ease-out 0.2s backwards;
            ">
                Transformez votre gestion des stocks avec l'intelligence artificielle.
                <strong style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Prévisions précises, décisions intelligentes.
                </strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card" style="animation: fadeInUp 0.6s ease-out 0.3s backwards;">
            <div class="feature-icon">🎯</div>
            <h3 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 0.75rem 0; font-family: 'Poppins', sans-serif; font-weight: 700;">Prévisions IA</h3>
            <p style="color: #6b7280; margin: 0; line-height: 1.7; font-weight: 500;">Anticipez la demande avec des prévisions probabilistes (P10/P50/P90) générées par l'intelligence artificielle Prophet</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card" style="animation: fadeInUp 0.6s ease-out 0.4s backwards;">
            <div class="feature-icon">📊</div>
            <h3 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 0.75rem 0; font-family: 'Poppins', sans-serif; font-weight: 700;">Optimisation</h3>
            <p style="color: #6b7280; margin: 0; line-height: 1.7; font-weight: 500;">Recevez des recommandations automatiques pour vos réapprovisionnements et niveaux de stock optimaux</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card" style="animation: fadeInUp 0.6s ease-out 0.5s backwards;">
            <div class="feature-icon">💡</div>
            <h3 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 0.75rem 0; font-family: 'Poppins', sans-serif; font-weight: 700;">Simple & Rapide</h3>
            <p style="color: #6b7280; margin: 0; line-height: 1.7; font-weight: 500;">Interface intuitive conçue pour les PME africaines, résultats en quelques secondes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Guide de démarrage
    st.markdown("## 🚀 Guide de Démarrage Rapide")
    
    steps = [
        {
            "number": "1",
            "icon": "📊",
            "title": "Importez vos données",
            "description": "Uploadez votre historique de ventes au format CSV ou Excel",
            "action": "Aller à Gestion des Données"
        },
        {
            "number": "2",
            "icon": "🔄",
            "title": "Configurez le mapping",
            "description": "Mappez vos colonnes avec le format Stokkel (produit, date, quantité)",
            "action": None
        },
        {
            "number": "3",
            "icon": "📈",
            "title": "Générez des prévisions",
            "description": "Consultez les prévisions de ventes pour vos produits avec intervalles de confiance",
            "action": "Aller aux Prévisions"
        },
        {
            "number": "4",
            "icon": "📦",
            "title": "Obtenez des recommandations",
            "description": "Recevez des conseils d'approvisionnement optimisés basés sur l'IA",
            "action": "Aller aux Recommandations"
        },
        {
            "number": "5",
            "icon": "🎯",
            "title": "Suivez vos KPIs",
            "description": "Surveillez vos indicateurs clés de performance en temps réel",
            "action": "Aller au Tableau de Bord"
        }
    ]
    
    for i, step in enumerate(steps):
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                    color: white;
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.5rem;
                    font-weight: 700;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    {step['number']}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="padding: 0.5rem 0;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{step['icon']}</span>
                        <h3 style="margin: 0; color: #374151;">{step['title']}</h3>
                    </div>
                    <p style="color: #6b7280; margin: 0 0 0.5rem 0;">{step['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if step['action']:
                if st.button(step['action'], key=f"step_{i}"):
                    target_page = step['action'].replace("Aller à ", "").replace("Aller aux ", "")
                    page_mapping = {
                        "Gestion des Données": "📊 Gestion des Données",
                        "Prévisions": "📈 Prévisions",
                        "Recommandations": "📦 Recommandations",
                        "Tableau de Bord": "🎯 Tableau de Bord"
                    }
                    st.session_state.current_page = page_mapping.get(target_page, "🏠 Accueil")
                    # Forcer le rechargement complet
                    st.rerun()
        
        if i < len(steps) - 1:
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistiques et bénéfices
    st.markdown("## 📈 Impact Attendu")
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="metric-card" style="text-align: center; animation: scaleIn 0.6s ease-out 0.6s backwards;">
                <div style="
                    font-size: 3rem;
                    margin-bottom: 0.75rem;
                    font-weight: 800;
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">-30%</div>
                <div style="color: #6b7280; font-size: 0.9375rem; font-weight: 600;">Ruptures de stock</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card" style="text-align: center; animation: scaleIn 0.6s ease-out 0.7s backwards;">
                <div style="
                    font-size: 3rem;
                    margin-bottom: 0.75rem;
                    font-weight: 800;
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">+25%</div>
                <div style="color: #6b7280; font-size: 0.9375rem; font-weight: 600;">Rotation des stocks</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card" style="text-align: center; animation: scaleIn 0.6s ease-out 0.8s backwards;">
                <div style="
                    font-size: 3rem;
                    margin-bottom: 0.75rem;
                    font-weight: 800;
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">-20%</div>
                <div style="color: #6b7280; font-size: 0.9375rem; font-weight: 600;">Stock immobilisé</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-card" style="text-align: center; animation: scaleIn 0.6s ease-out 0.9s backwards;">
                <div style="
                    font-size: 3rem;
                    margin-bottom: 0.75rem;
                    font-weight: 800;
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">95%</div>
                <div style="color: #6b7280; font-size: 0.9375rem; font-weight: 600;">Niveau de service</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Témoignages / Citations
    st.markdown("## 💬 Pourquoi Stokkel ?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background: #eff6ff; padding: 1.5rem; border-radius: 0.75rem; border-left: 4px solid #3b82f6;">
                <p style="font-style: italic; color: #1e40af; margin: 0 0 1rem 0;">
                    "Les PME africaines perdent en moyenne 4-7% de leur chiffre d'affaires à cause des ruptures de stock. 
                    72% de ces ruptures sont évitables avec de meilleurs outils de prévision."
                </p>
                <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">
                    <strong>Sources:</strong> Slimstock (2025), Netstock (2024)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: #f0fdf4; padding: 1.5rem; border-radius: 0.75rem; border-left: 4px solid #10b981;">
                <p style="font-style: italic; color: #065f46; margin: 0 0 1rem 0;">
                    "90% des entreprises africaines sont des PME, mais seulement 23% utilisent l'IA pour optimiser 
                    leur supply chain. Stokkel démocratise cet accès."
                </p>
                <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">
                    <strong>Sources:</strong> MIT Sloan (2024), DFS Lab (2024)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA Final ultra-moderne
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 1.5rem;
            text-align: center;
            color: white;
            box-shadow: 0 20px 60px -15px rgba(102, 126, 234, 0.5);
            position: relative;
            overflow: hidden;
            animation: scaleIn 0.6s ease-out 1s backwards;
        ">
            <div style="position: absolute; top: -50%; right: -10%; width: 300px; height: 300px; background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%); border-radius: 50%;"></div>
            <div style="position: absolute; bottom: -50%; left: -10%; width: 300px; height: 300px; background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%); border-radius: 50%;"></div>
            <h2 style="color: white; margin: 0 0 1rem 0; font-size: 2.25rem; font-weight: 800; font-family: 'Poppins', sans-serif; text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); position: relative;">
                Prêt à Optimiser Votre Gestion des Stocks ?
            </h2>
            <p style="font-size: 1.25rem; margin: 0 0 2rem 0; opacity: 0.95; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.7; position: relative;">
                Commencez dès maintenant et transformez votre supply chain avec l'intelligence artificielle
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='margin-top: -1.5rem; position: relative; z-index: 10;'>", unsafe_allow_html=True)
        if st.button("🚀 Commencer Maintenant", use_container_width=True, type="primary"):
            st.session_state.current_page = "📊 Gestion des Données"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)