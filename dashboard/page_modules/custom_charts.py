"""
dashboard/page_modules/custom_charts.py
========================================
Graphiques 100% Personnalisables - L'utilisateur contrôle TOUT
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

def show_custom_charts():
    """
    Page de création de graphiques personnalisables
    Aucune valeur statique - tout est choisi par l'utilisateur
    """
    
    st.markdown("# 📊 Créateur de Graphiques Personnalisés")
    st.markdown("✨ Créez vos propres visualisations en choisissant librement vos variables")
    
    # Vérifier l'état - utiliser les données du session state
    has_data = st.session_state.get('data_uploaded', False)
    products = st.session_state.get('uploaded_products', [])
    sales_data = st.session_state.get('uploaded_sales_data', None)
    
    if not has_data or not products or sales_data is None:
        st.warning("⚠️ Veuillez d'abord uploader des données dans 'Gestion des Données'")
        
        if st.button("📊 Aller à Gestion des Données"):
            st.session_state.selected_page = "📊 Gestion des Données"
            st.rerun()
        
        return
    
    try:
        # Utiliser les produits du session state
        product_ids = [p['product_id'] for p in products]
        
        # ========================================
        # SECTION 1: Sélection des Données
        # ========================================
        st.markdown("## 1️⃣ Sélection des Données")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_product = st.selectbox(
                "🏷️ Produit à Analyser",
                options=product_ids,
                help="Sélectionnez le produit dont vous voulez visualiser les données"
            )
        
        with col2:
            # Bouton pour charger les données
            if st.button("📥 Charger les Données", type="primary"):
                with st.spinner("Chargement des données..."):
                    # Filtrer les données du produit sélectionné
                    if sales_data is not None and 'product_id' in sales_data.columns:
                        product_data = sales_data[sales_data['product_id'] == selected_product]
                        
                        if not product_data.empty:
                            st.session_state.chart_data = product_data.copy()
                            st.session_state.chart_product_id = selected_product
                            st.success(f"✅ {len(st.session_state.chart_data)} lignes chargées")
                        else:
                            st.error("❌ Aucune donnée trouvée pour ce produit")
                    else:
                        st.error("❌ Aucune donnée disponible")
        
        # Vérifier si des données sont chargées
        if 'chart_data' not in st.session_state or st.session_state.chart_data is None:
            st.info("👆 Cliquez sur 'Charger les Données' pour commencer")
            return
        
        df = st.session_state.chart_data.copy()
        
        # Convertir les dates si nécessaire
        for col in df.columns:
            if 'date' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
        
        # Afficher un aperçu
        with st.expander("👀 Aperçu des Données"):
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"📊 Total: {len(df)} lignes | Colonnes disponibles: {', '.join(df.columns)}")
        
        st.markdown("---")
        
        # ========================================
        # SECTION 2: Configuration du Graphique
        # ========================================
        st.markdown("## 2️⃣ Configuration du Graphique")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chart_type = st.selectbox(
                "📈 Type de Graphique",
                options=[
                    "Ligne (Line)",
                    "Barres (Bar)",
                    "Nuage de Points (Scatter)",
                    "Aires (Area)",
                    "Boîte à Moustaches (Box)",
                    "Histogramme (Histogram)",
                    "Camembert (Pie)"
                ],
                help="Choisissez le type de visualisation"
            )
            chart_type_code = chart_type.split("(")[1].rstrip(")")
        
        with col2:
            x_column = st.selectbox(
                "🔹 Axe X",
                options=df.columns.tolist(),
                help="Variable pour l'axe horizontal"
            )
        
        with col3:
            # Pour Pie chart, on ne demande pas Y
            if chart_type_code != "Pie":
                available_y = [col for col in df.columns if col != x_column]
                y_column = st.selectbox(
                    "🔹 Axe Y",
                    options=available_y,
                    help="Variable pour l'axe vertical"
                )
            else:
                y_column = st.selectbox(
                    "🔹 Valeur",
                    options=[col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])],
                    help="Variable numérique pour les parts"
                )
        
        # Options avancées
        with st.expander("⚙️ Options Avancées"):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                color_by = st.selectbox(
                    "🎨 Couleur par",
                    options=["Aucune"] + df.columns.tolist(),
                    help="Grouper par couleur (catégories)"
                )
            
            with col_b:
                if chart_type_code not in ["Pie", "Histogram", "Box"]:
                    aggregation = st.selectbox(
                        "📊 Agrégation",
                        options=["Aucune", "Somme (Sum)", "Moyenne (Mean)", "Médiane (Median)", "Compte (Count)"],
                        help="Comment agréger les données groupées"
                    )
                else:
                    aggregation = "Aucune"
            
            with col_c:
                show_grid = st.checkbox("🔲 Afficher la Grille", value=True)
        
        # Titre personnalisé
        title = st.text_input(
            "📝 Titre du Graphique",
            value=f"Analyse de {y_column} par {x_column}" if chart_type_code != "Pie" else f"Distribution de {y_column}",
            help="Personnalisez le titre de votre graphique"
        )
        
        st.markdown("---")
        
        # ========================================
        # SECTION 3: Génération du Graphique
        # ========================================
        st.markdown("## 3️⃣ Votre Graphique")
        
        try:
            df_plot = df.copy()
            
            # Appliquer l'agrégation si nécessaire
            if aggregation != "Aucune" and chart_type_code not in ["Pie", "Histogram", "Box"]:
                agg_function = {
                    "Somme (Sum)": 'sum',
                    "Moyenne (Mean)": 'mean',
                    "Médiane (Median)": 'median',
                    "Compte (Count)": 'count'
                }.get(aggregation, 'sum')
                
                group_cols = [x_column]
                if color_by != "Aucune":
                    group_cols.append(color_by)
                
                df_plot = df_plot.groupby(group_cols)[y_column].agg(agg_function).reset_index()
            
            # Créer le graphique selon le type
            color_col = color_by if color_by != "Aucune" else None
            
            if chart_type_code == "Line":
                fig = px.line(
                    df_plot,
                    x=x_column,
                    y=y_column,
                    color=color_col,
                    title=title,
                    markers=True
                )
            
            elif chart_type_code == "Bar":
                fig = px.bar(
                    df_plot,
                    x=x_column,
                    y=y_column,
                    color=color_col,
                    title=title,
                    text_auto=True
                )
            
            elif chart_type_code == "Scatter":
                fig = px.scatter(
                    df_plot,
                    x=x_column,
                    y=y_column,
                    color=color_col,
                    title=title,
                    size=y_column if pd.api.types.is_numeric_dtype(df_plot[y_column]) else None
                )
            
            elif chart_type_code == "Area":
                fig = px.area(
                    df_plot,
                    x=x_column,
                    y=y_column,
                    color=color_col,
                    title=title
                )
            
            elif chart_type_code == "Box":
                fig = px.box(
                    df_plot,
                    x=x_column,
                    y=y_column,
                    color=color_col,
                    title=title
                )
            
            elif chart_type_code == "Histogram":
                fig = px.histogram(
                    df_plot,
                    x=x_column,
                    color=color_col,
                    title=title,
                    marginal="box"
                )
            
            elif chart_type_code == "Pie":
                # Pour Pie, aggréger d'abord
                if color_col:
                    df_pie = df_plot.groupby(color_col)[y_column].sum().reset_index()
                    names_col = color_col
                else:
                    df_pie = df_plot.groupby(x_column)[y_column].sum().reset_index()
                    names_col = x_column
                
                fig = px.pie(
                    df_pie,
                    values=y_column,
                    names=names_col,
                    title=title,
                    hole=0.3  # Donut style
                )
            
            else:
                st.error(f"Type de graphique non supporté: {chart_type_code}")
                return
            
            # Appliquer le style
            fig.update_layout(
                height=600,
                template='plotly_white',
                showlegend=True,
                hovermode='closest',
                font=dict(size=12)
            )
            
            if show_grid and chart_type_code not in ["Pie"]:
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            # Afficher le graphique
            st.plotly_chart(fig, use_container_width=True, key="main_chart")
            
            # ========================================
            # SECTION 4: Actions
            # ========================================
            st.markdown("## 4️⃣ Actions")
            
            col_action1, col_action2, col_action3 = st.columns(3)
            
            with col_action1:
                if st.button("💾 Sauvegarder cette Configuration", use_container_width=True):
                    # Initialiser la liste si nécessaire
                    if 'saved_charts' not in st.session_state:
                        st.session_state.saved_charts = []
                    
                    # Créer la configuration
                    config = {
                        'id': len(st.session_state.saved_charts) + 1,
                        'product_id': st.session_state.chart_product_id,
                        'type': chart_type_code,
                        'x': x_column,
                        'y': y_column,
                        'color': color_by,
                        'aggregation': aggregation,
                        'title': title,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    st.session_state.saved_charts.append(config)
                    st.success(f"✅ Configuration #{config['id']} sauvegardée!")
            
            with col_action2:
                # Export HTML
                html_buffer = fig.to_html()
                st.download_button(
                    label="📥 Télécharger (HTML)",
                    data=html_buffer,
                    file_name=f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            with col_action3:
                # Export PNG (nécessite kaleido)
                try:
                    img_bytes = fig.to_image(format="png", width=1200, height=600)
                    st.download_button(
                        label="📸 Télécharger (PNG)",
                        data=img_bytes,
                        file_name=f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                except:
                    st.caption("⚠️ Export PNG nécessite: pip install kaleido")
            
            # Afficher les configurations sauvegardées
            if 'saved_charts' in st.session_state and st.session_state.saved_charts:
                st.markdown("---")
                st.markdown("### 📚 Configurations Sauvegardées")
                
                for config in st.session_state.saved_charts:
                    with st.expander(f"#{config['id']} - {config['title']}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.json(config, expanded=False)
                        
                        with col2:
                            if st.button(f"🔄 Charger", key=f"load_{config['id']}"):
                                st.info("Chargement de la configuration...")
                                # Recharger les données et la config
                                # (à implémenter)
        
        except Exception as e:
            st.error(f"❌ Erreur lors de la création du graphique:")
            st.exception(e)
    
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
        st.exception(e)


# Helper function pour nettoyer les types
def clean_chart_data(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie et prépare les données pour le graphique"""
    df_clean = df.copy()
    
    # Convertir les dates
    for col in df_clean.columns:
        if 'date' in col.lower():
            try:
                df_clean[col] = pd.to_datetime(df_clean[col])
            except:
                pass
    
    return df_clean