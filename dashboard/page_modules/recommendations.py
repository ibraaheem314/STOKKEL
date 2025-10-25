"""
Page de recommandations - Génération de recommandations d'approvisionnement
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from components.styles import render_page_header, render_alert, render_status_badge
from components.api_client import with_loading
from components.session import update_stats


@with_loading("Calcul de la recommandation en cours...")
def generate_recommendation(api_client, product_id, current_stock, lead_time, service_level):
    """Génère une recommandation pour un produit"""
    rec = api_client.get_recommendation(product_id, current_stock, lead_time, service_level)
    if rec:
        update_stats('total_recommendations')
    return rec


@with_loading("Génération des recommandations batch en cours...")
def generate_batch_recommendations(api_client, lead_time, service_level):
    """Génère des recommandations pour tous les produits"""
    batch_rec = api_client.get_batch_recommendations(lead_time, service_level)
    if batch_rec:
        st.session_state.batch_recommendations = batch_rec
    return batch_rec


def render(api_client):
    """Render la page de recommandations"""
    
    render_page_header(
        "Recommandations d'Approvisionnement",
        "Optimisez vos commandes avec l'IA",
        "📦"
    )
    
    if not st.session_state.products:
        render_alert(
            "Aucun produit disponible. Veuillez d'abord uploader vos données dans la page 'Gestion des Données'.",
            "warning",
            "Aucune Donnée"
        )
        return
    
    tabs = st.tabs(["🎯 Produit Unique", "📊 Analyse Batch"])
    
    # TAB 1: PRODUIT UNIQUE
    with tabs[0]:
        render_single_product_tab(api_client)
    
    # TAB 2: ANALYSE BATCH
    with tabs[1]:
        render_batch_tab(api_client)


def render_single_product_tab(api_client):
    """Onglet d'analyse d'un produit unique"""
    
    st.markdown("### 🎯 Recommandation pour un Produit")
    
    # Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📦 Sélection du Produit")
        selected_product = st.selectbox(
            "Produit",
            options=st.session_state.products,
            key="rec_product",
            help="Choisissez le produit à analyser"
        )
        
        current_stock = st.number_input(
            "Stock actuel (unités)",
            min_value=0,
            value=100,
            step=10,
            help="Quantité actuellement en stock"
        )
    
    with col2:
        st.markdown("#### ⚙️ Paramètres d'Approvisionnement")
        lead_time = st.slider(
            "Délai de livraison (jours)",
            min_value=1,
            max_value=30,
            value=st.session_state.get('default_lead_time', 7),
            help="Temps entre la commande et la réception"
        )
        
        service_level = st.slider(
            "Niveau de service cible (%)",
            min_value=80,
            max_value=99,
            value=st.session_state.get('default_service_level', 95),
            help="Probabilité de ne pas tomber en rupture"
        )
    
    # Bouton de génération
    if st.button("💡 Générer la Recommandation", type="primary", use_container_width=True):
        recommendation = generate_recommendation(
            api_client, selected_product, current_stock, lead_time, service_level
        )
        
        if recommendation:
            render_single_recommendation(recommendation, selected_product)


def render_single_recommendation(recommendation, product_id):
    """Affiche une recommandation unique"""
    
    st.markdown("---")
    st.markdown("### 📋 Recommandation Détaillée")
    
    # Alerte principale
    action = recommendation['recommendation_action']
    status = recommendation['current_stock_status']
    
    if action == "Commander":
        qty = recommendation['quantity_to_order']
        render_alert(
            f"**Quantité à commander :** {qty:.0f} unités\n\n**Statut actuel :** {status}",
            "warning",
            f"⚠️ ACTION REQUISE : {action.upper()}"
        )
    else:
        render_alert(
            f"**Statut actuel :** {status}\n\nVotre stock est suffisant pour couvrir la période",
            "success",
            "✅ STOCK SUFFISANT"
        )
    
    # Métriques clés
    st.markdown("### 📊 Métriques d'Optimisation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        reorder = recommendation['reorder_point']
        st.metric(
            "Point de Commande",
            f"{reorder:.0f} unités",
            help="Niveau de stock déclencheur pour passer commande"
        )
        
        st.markdown(f"""
            <div style="padding: 0.5rem; background: #eff6ff; border-radius: 0.5rem; margin-top: 0.5rem;">
                <small style="color: #1e40af;">
                    <strong>Explication :</strong> Commandez dès que le stock atteint {reorder:.0f} unités
                </small>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        safety = recommendation['dynamic_safety_stock']
        st.metric(
            "Stock de Sécurité",
            f"{safety:.0f} unités",
            help="Stock tampon pour absorber les variations de demande"
        )
        
        st.markdown(f"""
            <div style="padding: 0.5rem; background: #f0fdf4; border-radius: 0.5rem; margin-top: 0.5rem;">
                <small style="color: #065f46;">
                    <strong>Rôle :</strong> Protège contre les variations imprévues de la demande
                </small>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        days_until_stockout = recommendation.get('days_until_stockout')
        if days_until_stockout and days_until_stockout > 0:
            st.metric(
                "Jours avant rupture",
                days_until_stockout,
                help="Estimation basée sur la demande prévue"
            )
            
            if days_until_stockout <= 7:
                urgency_color = "#fef2f2"
                urgency_text_color = "#991b1b"
                urgency_msg = "⚠️ URGENT : Rupture imminente"
            elif days_until_stockout <= 14:
                urgency_color = "#fffbeb"
                urgency_text_color = "#92400e"
                urgency_msg = "⚠️ Attention : Commandez bientôt"
            else:
                urgency_color = "#f0fdf4"
                urgency_text_color = "#065f46"
                urgency_msg = "✅ Situation confortable"
            
            st.markdown(f"""
                <div style="padding: 0.5rem; background: {urgency_color}; border-radius: 0.5rem; margin-top: 0.5rem;">
                    <small style="color: {urgency_text_color};">
                        <strong>{urgency_msg}</strong>
                    </small>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.metric("Jours avant rupture", "N/A")
    
    # Détails supplémentaires
    with st.expander("📈 Détails de l'Analyse"):
        metadata = recommendation['metadata']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Demande")
            st.write(f"**Moyenne quotidienne :** {metadata['average_daily_demand']:.2f} unités/jour")
            st.write(f"**Variabilité :** {metadata['demand_variability']:.2f}")
            
            # Interprétation de la variabilité
            var = metadata['demand_variability']
            if var < 0.2:
                st.success("✅ Demande très stable")
            elif var < 0.5:
                st.info("ℹ️ Demande modérément variable")
            else:
                st.warning("⚠️ Demande très variable - stock de sécurité élevé recommandé")
        
        with col2:
            st.markdown("#### ⚙️ Paramètres")
            st.write(f"**Délai de livraison :** {metadata['lead_time']} jours")
            st.write(f"**Niveau de service :** {metadata['service_level']}%")
            st.write(f"**Stock actuel :** {metadata['current_stock']} unités")
    
    # Simulation de scénarios
    with st.expander("🎲 Simulation de Scénarios"):
        st.markdown("#### Que se passe-t-il si...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_lead_time = st.number_input(
                "Nouveau délai de livraison (jours)",
                min_value=1,
                max_value=30,
                value=int(metadata['lead_time']),
                key="sim_lead_time"
            )
        
        with col2:
            new_service = st.slider(
                "Nouveau niveau de service (%)",
                min_value=80,
                max_value=99,
                value=int(metadata['service_level'].replace('%', '')),
                key="sim_service"
            )
        
        if st.button("🔄 Recalculer", key="sim_button"):
            api_client = st.session_state.get('api_client')
            selected_product = st.session_state.get('rec_product', st.session_state.products[0] if st.session_state.products else None)
            new_rec = generate_recommendation(
                api_client, selected_product, 
                metadata['current_stock'], new_lead_time, new_service
            )
            
            if new_rec:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Nouveau Point de Commande", f"{new_rec['reorder_point']:.0f}")
                with col2:
                    st.metric("Nouveau Stock de Sécurité", f"{new_rec['dynamic_safety_stock']:.0f}")
                with col3:
                    st.metric("Nouvelle Quantité", f"{new_rec['quantity_to_order']:.0f}")


def render_batch_tab(api_client):
    """Onglet d'analyse batch"""
    
    st.markdown("### 📊 Recommandations pour Tous les Produits")
    
    st.info("""
    ℹ️ **Analyse globale :** Générez des recommandations pour l'ensemble de votre catalogue 
    avec les mêmes paramètres d'approvisionnement.
    """)
    
    # Configuration globale
    col1, col2 = st.columns(2)
    
    with col1:
        batch_lead_time = st.slider(
            "Délai de livraison global (jours)",
            min_value=1,
            max_value=30,
            value=st.session_state.get('default_lead_time', 7),
            key="batch_lead"
        )
    
    with col2:
        batch_service_level = st.slider(
            "Niveau de service global (%)",
            min_value=80,
            max_value=99,
            value=st.session_state.get('default_service_level', 95),
            key="batch_service"
        )
    
    # Génération
    if st.button("🚀 Générer Toutes les Recommandations", type="primary", use_container_width=True):
        batch_data = generate_batch_recommendations(api_client, batch_lead_time, batch_service_level)
        
        if batch_data:
            render_batch_results(batch_data)
    
    # Affichage des résultats en cache
    elif st.session_state.batch_recommendations:
        st.info("ℹ️ Affichage des dernières recommandations batch générées")
        render_batch_results(st.session_state.batch_recommendations)


def render_batch_results(batch_data):
    """Affiche les résultats batch"""
    
    st.markdown("---")
    st.markdown("### 📋 Résultats Globaux")
    
    recommendations = batch_data['recommendations']
    df_rec = pd.DataFrame(recommendations)
    
    # Statistiques globales
    products_to_order = df_rec[df_rec['recommendation_action'] == 'Commander']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Produits analysés",
            len(df_rec),
            help="Nombre total de produits"
        )
    
    with col2:
        st.metric(
            "Produits à commander",
            len(products_to_order),
            help="Produits nécessitant un réapprovisionnement"
        )
    
    with col3:
        total_qty = products_to_order['quantity_to_order'].sum()
        st.metric(
            "Quantité totale",
            f"{total_qty:,.0f}",
            help="Total des unités à commander"
        )
    
    with col4:
        avg_safety = df_rec['dynamic_safety_stock'].mean()
        st.metric(
            "Stock de sécurité moyen",
            f"{avg_safety:.0f}",
            help="Moyenne des stocks de sécurité"
        )
    
    # Filtres
    st.markdown("### 🔍 Filtrer les Résultats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        action_filter = st.multiselect(
            "Action recommandée",
            options=df_rec['recommendation_action'].unique().tolist(),
            default=df_rec['recommendation_action'].unique().tolist()
        )
    
    with col2:
        status_filter = st.multiselect(
            "Statut du stock",
            options=df_rec['current_stock_status'].unique().tolist(),
            default=df_rec['current_stock_status'].unique().tolist()
        )
    
    # Filtrage
    df_filtered = df_rec[
        df_rec['recommendation_action'].isin(action_filter) &
        df_rec['current_stock_status'].isin(status_filter)
    ]
    
    # Tableau des recommandations
    st.markdown(f"### 📊 Tableau des Recommandations ({len(df_filtered)} produits)")
    
    # Préparation du tableau d'affichage
    display_cols = [
        'product_id',
        'recommendation_action',
        'quantity_to_order',
        'reorder_point',
        'dynamic_safety_stock',
        'current_stock_status'
    ]
    
    df_display = df_filtered[display_cols].copy()
    df_display['quantity_to_order'] = df_display['quantity_to_order'].round(0).astype(int)
    df_display['reorder_point'] = df_display['reorder_point'].round(0).astype(int)
    df_display['dynamic_safety_stock'] = df_display['dynamic_safety_stock'].round(0).astype(int)
    
    # Tri par quantité à commander (décroissant)
    df_display = df_display.sort_values('quantity_to_order', ascending=False)
    
    st.dataframe(
        df_display,
        use_container_width=True,
        column_config={
            "product_id": st.column_config.TextColumn("Produit", width="medium"),
            "recommendation_action": st.column_config.TextColumn("Action", width="small"),
            "quantity_to_order": st.column_config.NumberColumn(
                "Qté à Commander",
                format="%d unités"
            ),
            "reorder_point": st.column_config.NumberColumn(
                "Point de Commande",
                format="%d"
            ),
            "dynamic_safety_stock": st.column_config.NumberColumn(
                "Stock de Sécurité",
                format="%d"
            ),
            "current_stock_status": st.column_config.TextColumn("Statut", width="medium")
        },
        hide_index=True
    )
    
    # Export
    st.markdown("### 📥 Export")
    
    csv = df_display.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger les recommandations (CSV)",
        data=csv,
        file_name=f"recommendations_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Résumé par catégorie de statut
    with st.expander("📊 Analyse par Statut"):
        status_counts = df_rec['current_stock_status'].value_counts()
        
        import plotly.express as px
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Répartition par Statut de Stock"
        )
        st.plotly_chart(fig, use_container_width=True)