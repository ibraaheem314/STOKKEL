"""
Page de gestion des données avec mapping flexible des colonnes
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from components.styles import render_page_header, render_alert
from components.api_client import with_loading


def render(api_client):
    """Render la page de gestion des données"""
    
    render_page_header("Gestion des Données", "Importez et configurez vos données de ventes", "📊")
    
    tabs = st.tabs(["📤 Import", "🔄 Mapping", "👁️ Visualisation", "🎯 Validation & Upload"])
    
    # TAB 1: IMPORT
    with tabs[0]:
        render_import_tab()
    
    # TAB 2: MAPPING
    with tabs[1]:
        render_mapping_tab()
    
    # TAB 3: VISUALISATION
    with tabs[2]:
        render_visualization_tab()
    
    # TAB 4: VALIDATION & UPLOAD
    with tabs[3]:
        render_validation_tab(api_client)


def render_import_tab():
    """Onglet d'import des données"""
    st.markdown("### 📤 Importer votre historique de ventes")
    
    st.info("""
    **Format attendu :** Fichier CSV ou Excel contenant votre historique de ventes
    
    **Données minimales requises :**
    - Identifiant produit (SKU, code article, nom...)
    - Date de la vente
    - Quantité vendue
    """)
    
    uploaded_file = st.file_uploader(
        "Choisir un fichier",
        type=['csv', 'xlsx', 'xls'],
        help="Uploadez votre fichier de ventes (CSV ou Excel)"
    )
    
    if uploaded_file is not None:
        try:
            # Lecture du fichier
            with st.spinner("Lecture du fichier..."):
                if uploaded_file.name.endswith('.csv'):
                    # Essayer différents encodings
                    try:
                        df = pd.read_csv(uploaded_file)
                    except UnicodeDecodeError:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding='latin-1')
                else:
                    df = pd.read_excel(uploaded_file)
            
            st.session_state.uploaded_data = df
            st.session_state.data_uploaded = True
            
            st.success(f"✅ **Fichier chargé avec succès !**")
            
            # Métriques du fichier
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Lignes", f"{len(df):,}")
            with col2:
                st.metric("📋 Colonnes", len(df.columns))
            with col3:
                missing = df.isnull().sum().sum()
                st.metric("⚠️ Valeurs manquantes", f"{missing:,}")
            with col4:
                size_kb = df.memory_usage(deep=True).sum() / 1024
                st.metric("💾 Taille", f"{size_kb:.1f} KB")
            
            # Aperçu des données
            st.markdown("#### 📋 Aperçu des données (10 premières lignes)")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Informations sur les colonnes
            with st.expander("📊 Informations détaillées sur les colonnes"):
                col_info = pd.DataFrame({
                    'Colonne': df.columns,
                    'Type': df.dtypes.astype(str),
                    'Non-null': df.count(),
                    'Uniques': [df[col].nunique() for col in df.columns],
                    'Exemple': [str(df[col].iloc[0]) if len(df) > 0 else '' for col in df.columns]
                })
                st.dataframe(col_info, use_container_width=True)
            
            # Bouton pour passer à la configuration
            if st.button("➡️ Passer à la Configuration du Mapping", type="primary", use_container_width=True):
                st.info("👉 Passez à l'onglet 'Mapping' pour configurer vos colonnes")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
            st.info("💡 Vérifiez que votre fichier est au bon format et n'est pas corrompu")


def render_mapping_tab():
    """Onglet de mapping des colonnes"""
    st.markdown("### 🔄 Configuration du Mapping des Colonnes")
    
    if st.session_state.uploaded_data is None:
        st.warning("⚠️ Veuillez d'abord importer un fichier dans l'onglet 'Import'")
        return
    
    df = st.session_state.uploaded_data
    
    st.info("""
    📌 **Instructions :** Mappez les colonnes de votre fichier avec les champs requis par Stokkel.
    Les colonnes marquées d'une * sont **obligatoires**.
    """)
    
    # Section 1: Colonnes obligatoires
    st.markdown("#### 1️⃣ Colonnes Obligatoires")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product_col = st.selectbox(
            "🏷️ Produit (ID/Référence) *",
            options=[''] + list(df.columns),
            help="Colonne contenant l'identifiant unique du produit",
            key="map_product"
        )
    
    with col2:
        date_col = st.selectbox(
            "📅 Date *",
            options=[''] + list(df.columns),
            help="Colonne contenant la date de la transaction",
            key="map_date"
        )
    
    with col3:
        quantity_col = st.selectbox(
            "📦 Quantité *",
            options=[''] + list(df.columns),
            help="Colonne contenant la quantité vendue",
            key="map_quantity"
        )
    
    # Affichage d'aperçu si les 3 colonnes sont sélectionnées
    if all([product_col, date_col, quantity_col]):
        st.markdown("##### ✅ Aperçu du mapping obligatoire")
        preview_df = pd.DataFrame({
            'product_id': df[product_col].head(3),
            'date': df[date_col].head(3),
            'quantity': df[quantity_col].head(3)
        })
        st.dataframe(preview_df, use_container_width=True)
    
    # Section 2: Colonnes optionnelles
    st.markdown("#### 2️⃣ Colonnes Optionnelles")
    
    with st.expander("🔍 Ajouter des colonnes additionnelles (optionnel)"):
        col1, col2 = st.columns(2)
        
        with col1:
            price_col = st.selectbox(
                "💰 Prix unitaire",
                options=['Non utilisé'] + list(df.columns),
                help="Prix unitaire du produit",
                key="map_price"
            )
            
            category_col = st.selectbox(
                "📂 Catégorie",
                options=['Non utilisé'] + list(df.columns),
                help="Catégorie du produit",
                key="map_category"
            )
            
            stock_col = st.selectbox(
                "📊 Stock actuel",
                options=['Non utilisé'] + list(df.columns),
                help="Niveau de stock actuel",
                key="map_stock"
            )
        
        with col2:
            store_col = st.selectbox(
                "🏪 Magasin/Entrepôt",
                options=['Non utilisé'] + list(df.columns),
                help="Identifiant du point de vente",
                key="map_store"
            )
            
            supplier_col = st.selectbox(
                "🚚 Fournisseur",
                options=['Non utilisé'] + list(df.columns),
                help="Identifiant du fournisseur",
                key="map_supplier"
            )
            
            cost_col = st.selectbox(
                "💵 Coût d'achat",
                options=['Non utilisé'] + list(df.columns),
                help="Coût d'achat unitaire",
                key="map_cost"
            )
    
    # Bouton de validation
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if not all([product_col, date_col, quantity_col]):
            st.warning("⚠️ Veuillez sélectionner les 3 colonnes obligatoires avant de valider")
    
    with col2:
        if st.button("✅ Valider le Mapping", type="primary", use_container_width=True, disabled=not all([product_col, date_col, quantity_col])):
            # Sauvegarde du mapping
            st.session_state.column_mapping = {
                'product_id': product_col,
                'date': date_col,
                'quantity': quantity_col,
                'price': price_col if price_col != 'Non utilisé' else None,
                'category': category_col if category_col != 'Non utilisé' else None,
                'stock': stock_col if stock_col != 'Non utilisé' else None,
                'store': store_col if store_col != 'Non utilisé' else None,
                'supplier': supplier_col if supplier_col != 'Non utilisé' else None,
                'cost': cost_col if cost_col != 'Non utilisé' else None
            }
            
            # Création du dataframe mappé
            try:
                mapped_df = pd.DataFrame()
                mapped_df['product_id'] = df[product_col].astype(str)
                mapped_df['date'] = pd.to_datetime(df[date_col], errors='coerce')
                mapped_df['quantity'] = pd.to_numeric(df[quantity_col], errors='coerce')
                
                # Ajout des colonnes optionnelles
                for key, col in st.session_state.column_mapping.items():
                    if col and key not in ['product_id', 'date', 'quantity']:
                        mapped_df[key] = df[col]
                
                # Nettoyage: supprimer les lignes avec des valeurs manquantes critiques
                initial_len = len(mapped_df)
                mapped_df = mapped_df.dropna(subset=['product_id', 'date', 'quantity'])
                dropped = initial_len - len(mapped_df)
                
                st.session_state.mapped_data = mapped_df
                
                st.success(f"✅ **Mapping validé avec succès !**")
                if dropped > 0:
                    st.info(f"ℹ️ {dropped} lignes avec des valeurs manquantes ont été supprimées")
                
                # Résumé du mapping
                st.markdown("#### 📊 Résumé du Mapping")
                mapping_summary = []
                for key, value in st.session_state.column_mapping.items():
                    if value:
                        mapping_summary.append({'Champ Stokkel': key, 'Colonne source': value})
                
                st.dataframe(pd.DataFrame(mapping_summary), use_container_width=True)
                
                st.info("👉 Passez à l'onglet 'Visualisation' pour explorer vos données")
                
            except Exception as e:
                st.error(f"❌ Erreur lors du mapping : {str(e)}")


def render_visualization_tab():
    """Onglet de visualisation des données"""
    st.markdown("### 👁️ Visualisation des Données Mappées")
    
    if st.session_state.mapped_data is None:
        st.warning("⚠️ Veuillez d'abord configurer le mapping dans l'onglet 'Mapping'")
        return
    
    df = st.session_state.mapped_data
    
    # Statistiques globales
    st.markdown("#### 📊 Statistiques Globales")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Produits uniques", df['product_id'].nunique())
    with col2:
        st.metric("Total ventes", f"{df['quantity'].sum():,.0f}")
    with col3:
        date_range = (df['date'].max() - df['date'].min()).days
        st.metric("Période (jours)", date_range)
    with col4:
        st.metric("Vente moy/jour", f"{df['quantity'].sum() / max(date_range, 1):.1f}")
    
    st.markdown("---")
    
    # Sélection du produit
    st.markdown("#### 🔍 Analyse par Produit")
    
    products = sorted(df['product_id'].unique())
    selected_product = st.selectbox(
        "Sélectionner un produit à analyser",
        options=products,
        key="viz_product"
    )
    
    if selected_product:
        product_data = df[df['product_id'] == selected_product].sort_values('date')
        
        # Graphique des ventes historiques
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=product_data['date'],
            y=product_data['quantity'],
            mode='lines+markers',
            name='Ventes',
            line=dict(color='#3b82f6', width=2),
            marker=dict(size=6, color='#3b82f6'),
            hovertemplate='<b>Date:</b> %{x}<br><b>Quantité:</b> %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Historique des ventes - {selected_product}",
            xaxis_title="Date",
            yaxis_title="Quantité",
            hovermode='x unified',
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques du produit
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Vente moyenne", f"{product_data['quantity'].mean():.1f}")
        with col2:
            st.metric("Vente max", f"{product_data['quantity'].max():.0f}")
        with col3:
            st.metric("Écart-type", f"{product_data['quantity'].std():.1f}")
        with col4:
            st.metric("Total vendu", f"{product_data['quantity'].sum():.0f}")
        
        # Analyses supplémentaires
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution
            fig_hist = px.histogram(
                product_data,
                x='quantity',
                nbins=20,
                title="Distribution des ventes",
                labels={'quantity': 'Quantité', 'count': 'Fréquence'}
            )
            fig_hist.update_layout(showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot
            fig_box = px.box(
                product_data,
                y='quantity',
                title="Box plot des ventes",
                labels={'quantity': 'Quantité'}
            )
            st.plotly_chart(fig_box, use_container_width=True)


@with_loading("Upload des données en cours...")
def upload_data_to_api(api_client, df):
    """Upload les données vers l'API"""
    # Préparation du CSV
    csv_buffer = io.StringIO()
    df[['product_id', 'date', 'quantity']].to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    # Upload
    response = api_client.upload_sales(csv_data)
    return response


def render_validation_tab(api_client):
    """Onglet de validation et upload"""
    st.markdown("### 🎯 Validation et Upload vers l'API")
    
    if st.session_state.mapped_data is None:
        st.warning("⚠️ Veuillez d'abord configurer le mapping dans l'onglet 'Mapping'")
        return
    
    df = st.session_state.mapped_data
    
    # Contrôles de qualité
    st.markdown("#### ✅ Contrôles de Qualité")
    
    checks = []
    
    # Check 1: Valeurs manquantes critiques
    missing_critical = df[['product_id', 'date', 'quantity']].isnull().sum().sum()
    checks.append({
        'test': 'Valeurs manquantes (colonnes critiques)',
        'result': '✅ Aucune' if missing_critical == 0 else f'❌ {missing_critical}',
        'status': 'success' if missing_critical == 0 else 'error'
    })
    
    # Check 2: Quantités négatives
    negative_qty = (df['quantity'] < 0).sum()
    checks.append({
        'test': 'Quantités négatives',
        'result': '✅ Aucune' if negative_qty == 0 else f'⚠️ {negative_qty}',
        'status': 'success' if negative_qty == 0 else 'warning'
    })
    
    # Check 3: Dates futures
    future_dates = (df['date'] > pd.Timestamp.now()).sum()
    checks.append({
        'test': 'Dates futures',
        'result': '✅ Aucune' if future_dates == 0 else f'⚠️ {future_dates}',
        'status': 'success' if future_dates == 0 else 'warning'
    })
    
    # Check 4: Produits avec peu de données
    product_counts = df.groupby('product_id').size()
    low_data_products = (product_counts < 7).sum()
    checks.append({
        'test': 'Produits avec < 7 jours de données',
        'result': '✅ Aucun' if low_data_products == 0 else f'⚠️ {low_data_products}',
        'status': 'success' if low_data_products == 0 else 'warning'
    })
    
    # Check 5: Doublons
    duplicates = df.duplicated(subset=['product_id', 'date']).sum()
    checks.append({
        'test': 'Doublons (produit + date)',
        'result': '✅ Aucun' if duplicates == 0 else f'⚠️ {duplicates}',
        'status': 'success' if duplicates == 0 else 'warning'
    })
    
    # Affichage des checks
    for check in checks:
        if check['status'] == 'success':
            st.success(f"**{check['test']}:** {check['result']}")
        elif check['status'] == 'warning':
            st.warning(f"**{check['test']}:** {check['result']}")
        else:
            st.error(f"**{check['test']}:** {check['result']}")
    
    # Résumé
    st.markdown("#### 📊 Résumé des Données")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📦 Produits uniques", df['product_id'].nunique())
    with col2:
        period_str = f"{df['date'].min().strftime('%Y-%m-%d')} → {df['date'].max().strftime('%Y-%m-%d')}"
        st.metric("📅 Période", period_str)
    with col3:
        st.metric("📊 Lignes de données", f"{len(df):,}")
    
    # Upload
    st.markdown("---")
    
    can_upload = missing_critical == 0
    
    if not can_upload:
        st.error("❌ Impossible d'uploader : des valeurs critiques sont manquantes")
    
    if st.button(
        "🚀 Envoyer les Données vers l'API",
        type="primary",
        use_container_width=True,
        disabled=not can_upload
    ):
        response = upload_data_to_api(api_client, df)
        
        if response:
            st.success("✅ **Données uploadées avec succès !**")
            
            # Mise à jour de la liste des produits
            products_response = api_client.get_products()
            if products_response:
                products_data = products_response.get('products', [])
                st.session_state.products = [
                    p['product_id'] for p in products_data 
                    if isinstance(p, dict) and 'product_id' in p
                ]
                st.info(f"✅ {len(st.session_state.products)} produits chargés dans le système")
            
            # Affichage de la réponse
            with st.expander("📋 Détails de la réponse API"):
                st.json(response)
            
            st.markdown("---")
            st.info("👉 **Prochaines étapes :** Allez dans l'onglet 'Prévisions' pour générer vos premières prévisions")