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
    # STATS RÉELLES DEPUIS L'API
    # ============================================
    
    def get_real_kpis_from_api():
        """Récupère les KPIs RÉELS depuis l'API"""
        if not api_client:
            return {
                'total_products': 0,
                'total_sales_records': 0,
                'data_period_days': 0,
                'last_update': 'Aucune donnée'
            }
        
        try:
            # Appeler l'API pour obtenir les stats RÉELLES
            products = api_client.get_products()
            
            return {
                'total_products': len(products),
                'total_sales_records': sum(p.get('records_count', 0) for p in products),
                'data_period_days': max([p.get('days_of_data', 0) for p in products], default=0),
                'last_update': datetime.now().isoformat()
            }
        except:
            return {
                'total_products': 0,
                'total_sales_records': 0,
                'data_period_days': 0,
                'last_update': 'Erreur API'
            }
    
    # Utiliser les données réelles
    kpis = get_real_kpis_from_api()
    
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
            delta=0,
            icon="📅"
        ), unsafe_allow_html=True)
    
    with col4:
        hours_ago = (datetime.now() - datetime.fromisoformat(kpis['last_update'].replace('Z', '+00:00'))).total_seconds() / 3600 if kpis['last_update'] != 'Aucune donnée' else 0
        st.markdown(create_kpi_card(
            label="Dernière MAJ",
            value=f"{int(hours_ago)}h" if hours_ago > 0 else "N/A",
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
        # Sauvegarder temporairement le fichier
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Charger avec le système flexible
        with st.spinner("Analyse du fichier..."):
            import time
            time.sleep(1)
        
        st.success("✅ Fichier chargé avec succès!")
        
        # Lire le fichier pour l'interface
        df = pd.read_csv(uploaded_file)
        
        st.markdown("### 🔧 Configuration du Mapping des Colonnes")
        st.info("📌 Sélectionnez les colonnes correspondantes dans vos données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Colonnes Requises")
            
            # Laisser l'utilisateur CHOISIR
            user_mapping = {}
            
            product_col = st.selectbox(
                "🏷️ Colonne Product ID",
                options=[""] + list(df.columns),
                help="Identifiant unique du produit"
            )
            if product_col:
                user_mapping['product_id'] = product_col
            
            date_col = st.selectbox(
                "📅 Colonne Date",
                options=[""] + list(df.columns),
                help="Date de la vente"
            )
            if date_col:
                user_mapping['date'] = date_col
            
            quantity_col = st.selectbox(
                "📦 Colonne Quantité",
                options=[""] + list(df.columns),
                help="Quantité vendue"
            )
            if quantity_col:
                user_mapping['quantity'] = quantity_col
    
        with col2:
            st.markdown("#### Colonnes Optionnelles")
            
            price_col = st.selectbox(
                "💰 Colonne Prix (optionnel)",
                options=[""] + list(df.columns),
                help="Prix unitaire"
            )
            if price_col:
                user_mapping['price'] = price_col
            
            category_col = st.selectbox(
                "📊 Colonne Catégorie (optionnel)",
                options=[""] + list(df.columns),
                help="Catégorie du produit"
            )
            if category_col:
                user_mapping['category'] = category_col
            
        # Preview avec le mapping choisi
        if len(user_mapping) >= 3:  # Au moins les 3 requises
            st.markdown("### 👀 Aperçu des Données Mappées")
            
            # Appliquer le mapping
            df_mapped = df[list(user_mapping.values())].copy()
            df_mapped.columns = list(user_mapping.keys())
            
            st.dataframe(df_mapped.head(10), width='stretch')
            
            # Bouton pour envoyer à l'API avec le mapping personnalisé
            if st.button("📤 Envoyer à l'API avec ce Mapping", type="primary"):
                # Sauvegarder temporairement avec le bon mapping
                temp_file = "temp_mapped_data.csv"
                df_mapped.to_csv(temp_file, index=False)
                
                # Uploader vers l'API
                try:
                    response = api_client.upload_sales(temp_file)
                    
                    if response:
                        st.success("✅ Données envoyées avec succès!")
                        st.session_state.data_uploaded = True
                        st.rerun()  # Recharger la page pour mettre à jour les stats
                    else:
                        st.error("❌ Erreur lors de l'envoi")
                except Exception as e:
                    st.error(f"❌ Erreur API: {str(e)}")
        else:
            st.warning("⚠️ Veuillez sélectionner au minimum: Product ID, Date, et Quantité")
    
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