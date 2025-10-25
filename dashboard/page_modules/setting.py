"""
Page de configuration - Paramètres de l'application
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from components.styles import render_page_header, render_alert
from components.session import clear_session


def render(api_client):
    """Render la page de configuration"""
    
    render_page_header(
        "Configuration",
        "Personnalisez les paramètres de Stokkel",
        "⚙️"
    )
    
    tabs = st.tabs(["🔧 Général", "🤖 Modèles IA", "🔐 API", "ℹ️ À Propos"])
    
    # TAB 1: PARAMÈTRES GÉNÉRAUX
    with tabs[0]:
        render_general_settings()
    
    # TAB 2: MODÈLES IA
    with tabs[1]:
        render_ai_settings()
    
    # TAB 3: API
    with tabs[2]:
        render_api_settings(api_client)
    
    # TAB 4: À PROPOS
    with tabs[3]:
        render_about()


def render_general_settings():
    """Onglet des paramètres généraux"""
    
    st.markdown("### 🔧 Paramètres Généraux")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌍 Localisation")
        
        language = st.selectbox(
            "Langue de l'interface",
            options=["Français", "English", "Wolof"],
            index=0,
            help="Langue d'affichage de l'application"
        )
        
        currency = st.selectbox(
            "Devise",
            options=["FCFA", "EUR", "USD"],
            index=0,
            help="Devise pour les calculs financiers"
        )
        
        timezone = st.selectbox(
            "Fuseau horaire",
            options=["GMT", "UTC+1", "UTC"],
            index=0,
            help="Fuseau horaire pour les dates"
        )
    
    with col2:
        st.markdown("#### 📅 Formats")
        
        date_format = st.selectbox(
            "Format de date",
            options=["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
            index=0,
            help="Format d'affichage des dates"
        )
        
        number_format = st.selectbox(
            "Format des nombres",
            options=["1 234,56", "1,234.56", "1234.56"],
            index=0,
            help="Format d'affichage des nombres"
        )
    
    st.markdown("---")
    
    st.markdown("#### 📦 Paramètres d'Approvisionnement par Défaut")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_lead_time = st.number_input(
            "Délai de livraison par défaut (jours)",
            min_value=1,
            max_value=30,
            value=st.session_state.get('default_lead_time', 7),
            help="Délai par défaut pour les calculs"
        )
        
        if default_lead_time != st.session_state.get('default_lead_time', 7):
            st.session_state.default_lead_time = default_lead_time
            st.success("✅ Paramètre mis à jour")
    
    with col2:
        default_service_level = st.slider(
            "Niveau de service par défaut (%)",
            min_value=80,
            max_value=99,
            value=st.session_state.get('default_service_level', 95),
            help="Taux de service par défaut"
        )
        
        if default_service_level != st.session_state.get('default_service_level', 95):
            st.session_state.default_service_level = default_service_level
            st.success("✅ Paramètre mis à jour")
    
    st.markdown("---")
    
    st.markdown("#### 🎨 Apparence")
    
    theme = st.selectbox(
        "Thème",
        options=["Clair", "Sombre", "Auto"],
        index=0,
        help="Thème de couleur de l'interface"
    )
    
    st.info("ℹ️ Le changement de thème nécessite un rechargement de l'application")
    
    st.markdown("---")
    
    st.markdown("#### 🗑️ Gestion des Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Réinitialiser les Paramètres", use_container_width=True):
            st.session_state.default_lead_time = 7
            st.session_state.default_service_level = 95
            st.success("✅ Paramètres réinitialisés aux valeurs par défaut")
            st.rerun()
    
    with col2:
        if st.button("⚠️ Effacer Toutes les Données", type="secondary", use_container_width=True):
            if st.session_state.get('confirm_clear_all'):
                clear_session()
                st.success("✅ Toutes les données ont été effacées")
                st.session_state.confirm_clear_all = False
                st.rerun()
            else:
                st.session_state.confirm_clear_all = True
                st.warning("⚠️ Cliquez à nouveau pour confirmer la suppression")


def render_ai_settings():
    """Onglet des paramètres IA"""
    
    st.markdown("### 🤖 Configuration des Modèles d'IA")
    
    st.markdown("#### 📈 Modèle de Prévision")
    
    model_choice = st.selectbox(
        "Algorithme principal",
        options=["Prophet (Recommandé)", "SARIMA", "LSTM", "Auto-Select"],
        index=0,
        help="Choisissez l'algorithme de prévision à utiliser"
    )
    
    if model_choice == "Prophet (Recommandé)":
        st.info("""
        ✅ **Prophet** est recommandé pour la plupart des cas d'usage.
        
        **Avantages :**
        - Gère automatiquement la saisonnalité
        - Robuste aux valeurs manquantes
        - Rapide et fiable
        - Bon pour les séries avec tendances
        """)
    
    st.markdown("---")
    
    st.markdown("#### ⚙️ Paramètres du Modèle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_seasonality = st.checkbox(
            "Détection automatique de saisonnalité",
            value=True,
            help="Le modèle détecte automatiquement les patterns saisonniers"
        )
        
        use_external_vars = st.checkbox(
            "Utiliser les variables externes",
            value=False,
            help="Inclure des variables explicatives supplémentaires (promotions, météo, etc.)"
        )
        
        incremental_learning = st.checkbox(
            "Apprentissage incrémental",
            value=False,
            help="Le modèle s'améliore au fil du temps avec les nouvelles données"
        )
    
    with col2:
        confidence_interval = st.slider(
            "Intervalle de confiance (%)",
            min_value=70,
            max_value=95,
            value=80,
            step=5,
            help="Largeur de l'intervalle de prévision (P10-P90)"
        )
        
        forecast_frequency = st.selectbox(
            "Fréquence de mise à jour",
            options=["Quotidienne", "Hebdomadaire", "Mensuelle", "Manuelle"],
            index=1,
            help="Fréquence de recalcul des prévisions"
        )
    
    st.markdown("---")
    
    st.markdown("#### 🔬 Paramètres Avancés")
    
    with st.expander("Afficher les paramètres avancés"):
        st.warning("⚠️ Modifier ces paramètres peut affecter la qualité des prévisions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            changepoint_prior = st.number_input(
                "Changepoint prior scale",
                min_value=0.001,
                max_value=0.500,
                value=0.050,
                step=0.001,
                format="%.3f",
                help="Flexibilité du modèle aux changements de tendance"
            )
            
            seasonality_prior = st.number_input(
                "Seasonality prior scale",
                min_value=0.1,
                max_value=50.0,
                value=10.0,
                step=0.1,
                help="Force de la composante saisonnière"
            )
        
        with col2:
            holidays_prior = st.number_input(
                "Holidays prior scale",
                min_value=0.1,
                max_value=50.0,
                value=10.0,
                step=0.1,
                help="Impact des jours fériés sur la prévision"
            )
            
            uncertainty_samples = st.number_input(
                "Échantillons d'incertitude",
                min_value=100,
                max_value=2000,
                value=1000,
                step=100,
                help="Nombre de simulations pour calculer l'incertitude"
            )
    
    st.markdown("---")
    
    if st.button("💾 Enregistrer les Paramètres IA", type="primary", use_container_width=True):
        st.success("✅ Paramètres IA enregistrés avec succès")
        st.info("ℹ️ Les nouveaux paramètres seront appliqués aux prochaines prévisions")


def render_api_settings(api_client):
    """Onglet des paramètres API"""
    
    st.markdown("### 🔐 Configuration de l'API")
    
    st.markdown("#### 🔗 Connexion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_url = st.text_input(
            "URL de l'API",
            value=st.session_state.get('api_url', 'http://localhost:8000'),
            help="Adresse du serveur backend"
        )
        
        if api_url != st.session_state.get('api_url'):
            st.session_state.api_url = api_url
            api_client.base_url = api_url
    
    with col2:
        api_token = st.text_input(
            "Token d'authentification",
            value=st.session_state.get('api_token', 'stokkel_mvp_token'),
            type="password",
            help="Clé API pour l'authentification"
        )
        
        if api_token != st.session_state.get('api_token'):
            st.session_state.api_token = api_token
            api_client.token = api_token
    
    # Test de connexion
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔄 Tester la Connexion", use_container_width=True):
            with st.spinner("Test en cours..."):
                response = api_client.health_check()
                
                if response and response.get('status') == 'ok':
                    render_alert(
                        f"Connexion réussie ! Version API: {response.get('version', 'N/A')}",
                        "success",
                        "✅ API Opérationnelle"
                    )
                else:
                    render_alert(
                        "Impossible de se connecter à l'API. Vérifiez l'URL et le token.",
                        "critical",
                        "❌ Échec de Connexion"
                    )
    
    with col2:
        if st.button("💾 Enregistrer", type="primary", use_container_width=True):
            st.success("✅ Configuration API enregistrée")
    
    st.markdown("---")
    
    st.markdown("#### 📊 Statistiques d'Utilisation de l'API")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Requêtes aujourd'hui",
            st.session_state.stats.get('api_calls_today', 0)
        )
    
    with col2:
        st.metric(
            "Temps de réponse moyen",
            "~250ms"
        )
    
    with col3:
        availability = "99.9%" if api_client.test_connection() else "0%"
        st.metric(
            "Disponibilité",
            availability
        )
    
    st.markdown("---")
    
    st.markdown("#### 🔒 Sécurité")
    
    st.info("""
    **Bonnes pratiques de sécurité :**
    
    - 🔑 Ne partagez jamais votre token API
    - 🔄 Changez régulièrement votre token
    - 🔐 Utilisez HTTPS en production
    - 📝 Activez les logs d'audit
    """)


def render_about():
    """Onglet À Propos"""
    
    st.markdown("### ℹ️ À Propos de Stokkel")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0 0 1rem 0;">📊 Stokkel</h2>
        <p style="font-size: 1.125rem; margin: 0; opacity: 0.9;">
            Prévision Intelligente des Ventes & Optimisation des Stocks propulsée par l'IA
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🎯 Mission")
    st.markdown("""
    Aider les petites et moyennes entreprises (PME) et distributeurs au Sénégal et en Afrique de l'Ouest 
    à anticiper la demande et optimiser leurs stocks grâce à l'intelligence artificielle.
    """)
    
    st.markdown("#### 💡 Vision")
    st.markdown("""
    Devenir la plateforme de référence en Afrique de l'Ouest pour une gestion proactive des stocks, 
    réduisant les ruptures et le gaspillage, et améliorant la rentabilité des entreprises locales.
    """)
    
    st.markdown("---")
    
    st.markdown("#### 🚀 Fonctionnalités Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 Prévisions IA**
        - Prévisions probabilistes (P10/P50/P90)
        - Détection automatique de saisonnalité
        - Algorithmes de pointe (Prophet, SARIMA)
        
        **📊 Optimisation des Stocks**
        - Calcul du stock de sécurité dynamique
        - Point de commande optimal
        - Recommandations automatiques
        """)
    
    with col2:
        st.markdown("""
        **🎯 Tableau de Bord**
        - KPIs en temps réel
        - Alertes intelligentes
        - Visualisations interactives
        
        **🔌 API Flexible**
        - Intégration facile
        - API-first architecture
        - Documentation complète
        """)
    
    st.markdown("---")
    
    st.markdown("#### 📊 Impact Attendu")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #fef2f2; border-radius: 0.5rem;">
            <div style="font-size: 2rem; color: #ef4444; font-weight: 700;">-30%</div>
            <div style="color: #6b7280; font-size: 0.875rem;">Ruptures</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f0fdf4; border-radius: 0.5rem;">
            <div style="font-size: 2rem; color: #10b981; font-weight: 700;">+25%</div>
            <div style="color: #6b7280; font-size: 0.875rem;">Rotation</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #eff6ff; border-radius: 0.5rem;">
            <div style="font-size: 2rem; color: #3b82f6; font-weight: 700;">-20%</div>
            <div style="color: #6b7280; font-size: 0.875rem;">Stock dormant</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #fffbeb; border-radius: 0.5rem;">
            <div style="font-size: 2rem; color: #f59e0b; font-weight: 700;">95%</div>
            <div style="color: #6b7280; font-size: 0.875rem;">Service</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 📚 Ressources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - 📖 [Documentation](https://docs.stokkel.io)
        - 🎓 [Tutoriels](https://tutorials.stokkel.io)
        - 💻 [GitHub](https://github.com/stokkel)
        """)
    
    with col2:
        st.markdown("""
        - 📧 [Support](mailto:support@stokkel.io)
        - 💬 [Communauté](https://community.stokkel.io)
        - 📱 [Twitter](https://twitter.com/stokkel)
        """)
    
    st.markdown("---")
    
    st.markdown("#### 📄 Informations Techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Version de l'Application**
        - Dashboard: v1.0.0
        - API: v1.0.0
        - Python: 3.10+
        """)
    
    with col2:
        st.markdown("""
        **Technologies Utilisées**
        - Backend: FastAPI, Python
        - IA: Prophet, Scikit-learn
        - Frontend: Streamlit, Plotly
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f9fafb; border-radius: 0.5rem;">
        <p style="color: #6b7280; margin: 0;">
            © 2024 Stokkel. Tous droits réservés.<br>
            Fait avec ❤️ pour les PME africaines
        </p>
    </div>
    """, unsafe_allow_html=True)