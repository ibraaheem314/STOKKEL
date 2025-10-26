"""
Sidebar avec navigation et informations système
"""

import streamlit as st
from datetime import datetime
from .session import get_stats


def render_sidebar() -> str:
    """Render la sidebar et retourne la page sélectionnée"""
    
    with st.sidebar:
        # Logo et titre ultra-moderne avec animation
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem 0 2.5rem 0; animation: fadeInDown 0.6s ease-out;">
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    width: 80px;
                    height: 80px;
                    border-radius: 20px;
                    margin: 0 auto 1rem auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 2.5rem;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                    animation: float 3s ease-in-out infinite;
                ">
                    📊
                </div>
                <h2 style="
                    color: white;
                    font-size: 2rem;
                    margin: 0;
                    font-weight: 800;
                    font-family: 'Poppins', sans-serif;
                    letter-spacing: -0.02em;
                    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                ">Stokkel</h2>
                <p style="
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 0.75rem;
                    margin: 0.5rem 0 0 0;
                    font-weight: 600;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                ">Version 1.0.0</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation principale
        st.markdown("### 🧭 Navigation")
        
        pages = [
            ("🏠", "Accueil"),
            ("📊", "Gestion des Données"),
            ("📈", "Prévisions"),
            ("📦", "Recommandations"),
            ("🎯", "Tableau de Bord"),
            ("⚙️", "Configuration")
        ]
        
        # Navigation avec boutons persistants
        current_page = st.session_state.get('current_page', "🏠 Accueil")
        
        for icon, page_name in pages:
            full_name = f"{icon} {page_name}"
            is_selected = current_page == full_name
            
            # Style du bouton selon l'état
            button_type = "primary" if is_selected else "secondary"
            
            if st.button(
                full_name,
                key=f"nav_{page_name}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.current_page = full_name
                st.rerun()
        
        # Retourner la page actuelle
        selected_page = st.session_state.get('current_page', "🏠 Accueil")
        
        st.markdown("---")
        
        # Statistiques rapides avec design moderne
        st.markdown("### 📊 Statistiques")
        stats = get_stats()

        st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 1.25rem;
                border-radius: 1rem;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            ">
                <div style="margin-bottom: 0.875rem; display: flex; align-items: center; justify-content: space-between;">
                    <span style="opacity: 0.9; font-size: 0.875rem;">Produits</span>
                    <span style="font-weight: 700; font-size: 1.25rem; font-family: 'Poppins', sans-serif;">{len(st.session_state.get('products', []))}</span>
                </div>
                <div style="margin-bottom: 0.875rem; display: flex; align-items: center; justify-content: space-between;">
                    <span style="opacity: 0.9; font-size: 0.875rem;">Prévisions</span>
                    <span style="font-weight: 700; font-size: 1.25rem; font-family: 'Poppins', sans-serif;">{stats.get('total_forecasts', 0)}</span>
                </div>
                <div style="margin-bottom: 0.875rem; display: flex; align-items: center; justify-content: space-between;">
                    <span style="opacity: 0.9; font-size: 0.875rem;">Ruptures évitées</span>
                    <span style="font-weight: 700; font-size: 1.25rem; font-family: 'Poppins', sans-serif; color: #10b981;">{stats.get('stockouts_avoided', 0)}</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span style="opacity: 0.9; font-size: 0.875rem;">API calls</span>
                    <span style="font-weight: 700; font-size: 1.25rem; font-family: 'Poppins', sans-serif;">{stats.get('api_calls_today', 0)}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # État de la connexion
        st.markdown("### 🔌 État Système")
        
        api_client = st.session_state.get('api_client')
        if api_client:
            if api_client.test_connection():
                st.success("✅ API connectée")
            else:
                st.error("❌ API déconnectée")
        else:
            st.warning("⚠️ Client API non initialisé")
        
        # Données uploadées
        if st.session_state.get('data_uploaded'):
            st.success("✅ Données chargées")
        else:
            st.info("ℹ️ Aucune donnée")
        
        st.markdown("---")
        
        # Raccourcis
        st.markdown("### ⚡ Raccourcis")
        
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
        
        if st.button("🗑️ Réinitialiser", use_container_width=True):
            if st.session_state.get('confirm_reset'):
                from components.session import clear_session
                clear_session()
                st.success("Session réinitialisée")
                st.session_state.confirm_reset = False
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("⚠️ Cliquez à nouveau pour confirmer")
        
        st.markdown("---")
        
        # Footer moderne avec gradient
        st.markdown(f"""
            <div style="
                text-align: center;
                padding: 1rem;
                margin-top: 1rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                animation: fadeIn 1s ease-out;
            ">
                <p style="
                    margin: 0 0 0.5rem 0;
                    font-weight: 600;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 0.8125rem;
                    letter-spacing: 0.05em;
                ">© 2024 Stokkel</p>
                <p style="
                    margin: 0;
                    color: rgba(255, 255, 255, 0.6);
                    font-size: 0.6875rem;
                    font-weight: 500;
                ">{datetime.now().strftime('%d/%m/%Y • %H:%M')}</p>
                <div style="
                    margin-top: 0.75rem;
                    display: flex;
                    gap: 0.5rem;
                    justify-content: center;
                    flex-wrap: wrap;
                ">
                    <span style="
                        background: rgba(16, 185, 129, 0.2);
                        color: #10b981;
                        padding: 0.25rem 0.75rem;
                        border-radius: 999px;
                        font-size: 0.625rem;
                        font-weight: 600;
                        letter-spacing: 0.05em;
                    ">AI-POWERED</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    return selected_page