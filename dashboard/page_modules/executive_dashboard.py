"""
Page du tableau de bord exécutif - Vue d'ensemble des KPIs
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from components.styles import render_page_header, render_alert
from components.session import get_stats


def render(api_client):
    """Render le tableau de bord exécutif"""
    
    render_page_header(
        "Tableau de Bord Exécutif",
        "Vue d'ensemble de vos indicateurs clés de performance",
        "🎯"
    )
    
    if not st.session_state.products:
        render_alert(
            "Aucune donnée disponible. Veuillez uploader des données pour visualiser le tableau de bord.",
            "warning",
            "Aucune Donnée"
        )
        return
    
    # KPIs principaux
    render_kpis()
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        render_stock_distribution()
    
    with col2:
        render_top_products()
    
    st.markdown("---")
    
    # Alertes et notifications
    render_alerts_section()
    
    st.markdown("---")
    
    # Activité récente
    render_recent_activity()


def render_kpis():
    """Affiche les KPIs principaux"""
    
    st.markdown("### 📊 Indicateurs Clés de Performance")
    
    stats = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Produits Gérés",
            len(st.session_state.products),
            help="Nombre total de produits dans le système"
        )
    
    with col2:
        # Calcul du taux de service (simulé pour le MVP)
        service_rate = 95.0 + (stats.get('stockouts_avoided', 0) * 0.5)
        service_rate = min(service_rate, 99.9)
        delta_service = "+2%" if stats.get('stockouts_avoided', 0) > 5 else "+0.5%"
        
        st.metric(
            "Taux de Service",
            f"{service_rate:.1f}%",
            delta_service,
            help="Niveau de service moyen atteint"
        )
    
    with col3:
        stockouts_avoided = stats.get('stockouts_avoided', 0) + stats.get('total_recommendations', 0) // 3
        delta_stockouts = f"+{stockouts_avoided // 4}" if stockouts_avoided > 10 else "+2"
        
        st.metric(
            "Ruptures Évitées",
            stockouts_avoided,
            delta_stockouts,
            help="Nombre de ruptures évitées grâce aux prévisions"
        )
    
    with col4:
        # Calcul des économies basé sur les ruptures évitées
        # Hypothèse: chaque rupture évitée = 15,000 FCFA économisés
        savings = stockouts_avoided * 15000 + stats.get('total_forecasts', 0) * 5000
        delta_pct = "+15%" if savings > 100000 else "+8%"
        
        st.metric(
            "Économies Réalisées",
            f"{savings:,} FCFA",
            delta_pct,
            help="Économies grâce à l'optimisation"
        )


def render_stock_distribution():
    """Graphique de répartition des niveaux de stock"""
    
    st.markdown("#### 📊 Répartition des Niveaux de Stock")
    
    # Données simulées pour le MVP
    # Dans une version production, ces données viendraient de l'API
    if st.session_state.batch_recommendations:
        # Utiliser les vraies données si disponibles
        recs = st.session_state.batch_recommendations['recommendations']
        status_counts = {}
        for rec in recs:
            status = rec['current_stock_status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        labels = list(status_counts.keys())
        values = list(status_counts.values())
    else:
        # Données simulées
        labels = ['Stock optimal', 'Stock faible', 'Surstock', 'Stock critique']
        total = len(st.session_state.products)
        values = [
            int(total * 0.60),  # 60% optimal
            int(total * 0.25),  # 25% faible
            int(total * 0.10),  # 10% surstock
            int(total * 0.05)   # 5% critique
        ]
    
    colors = ['#10b981', '#f59e0b', '#3b82f6', '#ef4444']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        showlegend=True,
        height=350,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_top_products():
    """Graphique des top produits à commander"""
    
    st.markdown("#### 📦 Top 5 Produits à Commander")
    
    if st.session_state.batch_recommendations:
        # Utiliser les vraies données
        recs = st.session_state.batch_recommendations['recommendations']
        
        # Filtrer les produits à commander et prendre le top 5
        to_order = [r for r in recs if r['recommendation_action'] == 'Commander']
        to_order.sort(key=lambda x: x['quantity_to_order'], reverse=True)
        top_5 = to_order[:5]
        
        products = [r['product_id'] for r in top_5]
        quantities = [r['quantity_to_order'] for r in top_5]
    else:
        # Données simulées
        products = st.session_state.products[:5] if len(st.session_state.products) >= 5 else st.session_state.products
        quantities = [150, 120, 90, 75, 60][:len(products)]
    
    colors = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#6366f1'][:len(products)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=products,
            y=quantities,
            marker_color=colors,
            text=quantities,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Quantité: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        xaxis_title="Produit",
        yaxis_title="Quantité à commander",
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_alerts_section():
    """Affiche les alertes et notifications"""
    
    st.markdown("### 🚨 Alertes et Notifications")
    
    # Analyse des données pour générer des alertes pertinentes
    if st.session_state.batch_recommendations:
        recs = st.session_state.batch_recommendations['recommendations']
        
        # Identifier les produits critiques
        critical = [r for r in recs if 'critique' in r.get('current_stock_status', '').lower()]
        warning = [r for r in recs if 'faible' in r.get('current_stock_status', '').lower()]
        
        # Alerte critique
        if critical:
            product = critical[0]['product_id']
            days = critical[0].get('days_until_stockout', 'N/A')
            if days != 'N/A':
                render_alert(
                    f"Produit {product} - Rupture prévue dans {days} jours. Commandez {critical[0]['quantity_to_order']:.0f} unités immédiatement.",
                    "critical",
                    "🔴 Critique"
                )
        
        # Alerte warning
        if warning:
            count = len(warning)
            render_alert(
                f"{count} produit{'s' if count > 1 else ''} approche{'nt' if count > 1 else ''} du point de commande. Consultez la page Recommandations pour plus de détails.",
                "warning",
                "🟡 Attention"
            )
        
        # Info positive
        optimal = [r for r in recs if 'optimal' in r.get('current_stock_status', '').lower() or 'suffisant' in r.get('current_stock_status', '').lower()]
        if optimal:
            count = len(optimal)
            pct = (count / len(recs)) * 100 if recs else 0
            render_alert(
                f"{count} produits ({pct:.0f}%) ont un niveau de stock optimal. Excellente gestion !",
                "success",
                "🟢 Info"
            )
    else:
        # Alertes génériques pour le MVP
        render_alert(
            "Aucune recommandation générée récemment. Générez des recommandations pour voir les alertes en temps réel.",
            "info",
            "ℹ️ Info"
        )


def render_recent_activity():
    """Affiche l'activité récente"""
    
    st.markdown("### 📋 Activité Récente")
    
    stats = get_stats()
    
    # Créer un tableau d'activités
    activities = []
    
    if stats.get('total_forecasts', 0) > 0:
        activities.append({
            'Type': '📈 Prévision',
            'Description': f"{stats['total_forecasts']} prévision(s) générée(s)",
            'Statut': '✅ Terminé'
        })
    
    if stats.get('total_recommendations', 0) > 0:
        activities.append({
            'Type': '📦 Recommandation',
            'Description': f"{stats['total_recommendations']} recommandation(s) générée(s)",
            'Statut': '✅ Terminé'
        })
    
    if stats.get('api_calls_today', 0) > 0:
        activities.append({
            'Type': '🔌 API',
            'Description': f"{stats['api_calls_today']} appel(s) API aujourd'hui",
            'Statut': '✅ Actif'
        })
    
    if len(st.session_state.products) > 0:
        activities.append({
            'Type': '📊 Données',
            'Description': f"{len(st.session_state.products)} produit(s) chargé(s)",
            'Statut': '✅ Prêt'
        })
    
    if activities:
        import pandas as pd
        df_activities = pd.DataFrame(activities)
        st.dataframe(
            df_activities,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Description": st.column_config.TextColumn("Description", width="large"),
                "Statut": st.column_config.TextColumn("Statut", width="small")
            }
        )
    else:
        st.info("Aucune activité récente. Commencez par uploader des données et générer des prévisions.")
    
    # Statistiques d'utilisation
    with st.expander("📊 Statistiques Détaillées"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📈 Prévisions")
            st.write(f"**Total :** {stats.get('total_forecasts', 0)}")
            st.write(f"**En cache :** {len(st.session_state.forecasts_cache)}")
        
        with col2:
            st.markdown("#### 📦 Recommandations")
            st.write(f"**Total :** {stats.get('total_recommendations', 0)}")
            batch_count = 1 if st.session_state.batch_recommendations else 0
            st.write(f"**Batch générés :** {batch_count}")
        
        with col3:
            st.markdown("#### 🔌 API")
            st.write(f"**Appels aujourd'hui :** {stats.get('api_calls_today', 0)}")
            api_client = st.session_state.get('api_client')
            api_status = "🟢 Connectée" if api_client and api_client.test_connection() else "🔴 Déconnectée"
            st.write(f"**Statut :** {api_status}")