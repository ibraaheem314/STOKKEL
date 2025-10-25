"""
Page de prévisions - Génération et visualisation des prévisions de ventes
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from components.styles import render_page_header, render_alert
from components.api_client import with_loading
from components.session import update_stats


@with_loading("Génération de la prévision en cours...")
def generate_forecast(api_client, product_id, horizon_days):
    """Génère une prévision pour un produit"""
    forecast_data = api_client.get_forecast(product_id, horizon_days)
    if forecast_data:
        update_stats('total_forecasts')
        # Mettre en cache
        cache_key = f"{product_id}_{horizon_days}"
        st.session_state.forecasts_cache[cache_key] = forecast_data
        st.session_state.last_forecast = forecast_data
    return forecast_data


def render(api_client):
    """Render la page de prévisions"""
    
    render_page_header("Prévisions de Ventes", "Anticipez la demande avec l'IA probabiliste", "📈")
    
    if not st.session_state.get('products', []):
        render_alert(
            "Aucun produit disponible. Veuillez d'abord uploader vos données dans la page 'Gestion des Données'.",
            "warning",
            "Aucune Donnée"
        )
        
        # Contenu d'aide quand pas de données
        st.markdown("## 📋 Comment commencer ?")
        st.markdown("""
        1. **Allez à la page 'Gestion des Données'** dans le sidebar
        2. **Uploadez votre fichier CSV** avec vos données de ventes
        3. **Configurez le mapping** des colonnes
        4. **Revenez ici** pour générer des prévisions
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 Aller à la Gestion des Données", use_container_width=True, type="primary"):
                st.session_state.current_page = "📊 Gestion des Données"
                st.rerun()
        
        return
    
    # Configuration de la prévision
    st.markdown("### ⚙️ Configuration de la Prévision")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        selected_product = st.selectbox(
            "📦 Sélectionner un produit",
            options=st.session_state.products,
            help="Choisissez le produit pour lequel générer la prévision"
        )
    
    with col2:
        horizon = st.slider(
            "🔭 Horizon (jours)",
            min_value=7,
            max_value=90,
            value=30,
            step=7,
            help="Nombre de jours à prévoir"
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔮 Générer la Prévision", type="primary", use_container_width=True):
            st.session_state.trigger_forecast = True
    
    # Génération de la prévision
    if st.session_state.get('trigger_forecast', False):
        st.session_state.trigger_forecast = False
        
        forecast_data = generate_forecast(api_client, selected_product, horizon)
        
        if forecast_data:
            render_forecast_results(forecast_data, selected_product, horizon)
    
    # Affichage de la dernière prévision en cache
    elif st.session_state.last_forecast:
        st.info("ℹ️ Affichage de la dernière prévision générée")
        render_forecast_results(
            st.session_state.last_forecast,
            st.session_state.last_forecast.get('product_id', 'N/A'),
            len(st.session_state.last_forecast.get('forecasts', []))
        )


def render_forecast_results(forecast_data, product_id, horizon):
    """Affiche les résultats de la prévision"""
    
    st.markdown("---")
    st.markdown("### 📊 Résultats de la Prévision")
    
    forecasts = forecast_data['forecasts']
    metadata = forecast_data['metadata']
    
    # Préparation des données
    dates = [f['date'] for f in forecasts]
    p10 = [f['p10'] for f in forecasts]
    p50 = [f['p50'] for f in forecasts]
    p90 = [f['p90'] for f in forecasts]
    
    # Graphique principal
    fig = go.Figure()
    
    # Zone d'incertitude (P10-P90)
    fig.add_trace(go.Scatter(
        x=dates + dates[::-1],
        y=p90 + p10[::-1],
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.15)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Intervalle de confiance 80%'
    ))
    
    # P10 (Pessimiste)
    fig.add_trace(go.Scatter(
        x=dates,
        y=p10,
        mode='lines',
        name='P10 (Scénario pessimiste)',
        line=dict(color='#ef4444', dash='dash', width=2),
        hovertemplate='<b>P10:</b> %{y:.1f}<extra></extra>'
    ))
    
    # P50 (Médiane)
    fig.add_trace(go.Scatter(
        x=dates,
        y=p50,
        mode='lines+markers',
        name='P50 (Scénario médian)',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=6, color='#3b82f6'),
        hovertemplate='<b>P50:</b> %{y:.1f}<extra></extra>'
    ))
    
    # P90 (Optimiste)
    fig.add_trace(go.Scatter(
        x=dates,
        y=p90,
        mode='lines',
        name='P90 (Scénario optimiste)',
        line=dict(color='#10b981', dash='dash', width=2),
        hovertemplate='<b>P90:</b> %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Prévision des ventes - {product_id} ({horizon} jours)",
        xaxis_title="Date",
        yaxis_title="Quantité prévue",
        hovermode='x unified',
        height=500,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métriques clés
    st.markdown("### 📊 Métriques Clés")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Vente médiane prévue",
            f"{np.mean(p50):.1f} unités/jour",
            help="Moyenne des prévisions P50"
        )
    
    with col2:
        st.metric(
            "Total prévu (P50)",
            f"{np.sum(p50):.0f} unités",
            help="Somme des ventes prévues sur la période"
        )
    
    with col3:
        st.metric(
            "Modèle utilisé",
            metadata['model_used'],
            help="Algorithme de prévision"
        )
    
    with col4:
        confidence = metadata.get('confidence_level', 'N/A')
        st.metric(
            "Niveau de confiance",
            confidence,
            help="Fiabilité de la prévision"
        )
    
    # Analyse de la variabilité
    st.markdown("### 📉 Analyse de la Variabilité")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Coefficient de variation
        cv = (np.std(p50) / np.mean(p50)) * 100 if np.mean(p50) > 0 else 0
        st.metric(
            "Coefficient de variation",
            f"{cv:.1f}%",
            help="Mesure de la variabilité relative de la demande"
        )
        
        if cv < 20:
            st.success("✅ Demande stable - prévisions fiables")
        elif cv < 40:
            st.info("ℹ️ Demande modérément variable")
        else:
            st.warning("⚠️ Demande très variable - prudence recommandée")
    
    with col2:
        # Largeur de l'intervalle
        avg_interval_width = np.mean([p90[i] - p10[i] for i in range(len(p90))])
        interval_pct = (avg_interval_width / np.mean(p50)) * 100 if np.mean(p50) > 0 else 0
        
        st.metric(
            "Largeur intervalle P10-P90",
            f"{avg_interval_width:.1f} unités",
            f"{interval_pct:.0f}% de P50"
        )
        
        if interval_pct < 30:
            st.success("✅ Faible incertitude")
        elif interval_pct < 60:
            st.info("ℹ️ Incertitude modérée")
        else:
            st.warning("⚠️ Forte incertitude")
    
    # Détails de la prévision
    with st.expander("📋 Tableau détaillé des prévisions"):
        df_forecast = pd.DataFrame(forecasts)
        df_forecast['date'] = pd.to_datetime(df_forecast['date']).dt.strftime('%Y-%m-%d')
        df_forecast['p10'] = df_forecast['p10'].round(1)
        df_forecast['p50'] = df_forecast['p50'].round(1)
        df_forecast['p90'] = df_forecast['p90'].round(1)
        
        st.dataframe(
            df_forecast,
            use_container_width=True,
            column_config={
                "date": "Date",
                "p10": st.column_config.NumberColumn("P10 (Pessimiste)", format="%.1f"),
                "p50": st.column_config.NumberColumn("P50 (Médian)", format="%.1f"),
                "p90": st.column_config.NumberColumn("P90 (Optimiste)", format="%.1f")
            }
        )
        
        # Bouton de téléchargement
        csv = df_forecast.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les prévisions (CSV)",
            data=csv,
            file_name=f"forecast_{product_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Insights et recommandations
    st.markdown("### 💡 Insights")
    
    # Détection de tendance
    if len(p50) >= 7:
        first_week = np.mean(p50[:7])
        last_week = np.mean(p50[-7:])
        trend_pct = ((last_week - first_week) / first_week) * 100 if first_week > 0 else 0
        
        if abs(trend_pct) > 10:
            if trend_pct > 0:
                render_alert(
                    f"Tendance haussière détectée : +{trend_pct:.1f}% entre la première et la dernière semaine. Anticipez une augmentation de la demande.",
                    "info",
                    "📈 Tendance"
                )
            else:
                render_alert(
                    f"Tendance baissière détectée : {trend_pct:.1f}% entre la première et la dernière semaine. La demande pourrait diminuer.",
                    "info",
                    "📉 Tendance"
                )
    
    # Détection de pics
    max_p50 = max(p50)
    avg_p50 = np.mean(p50)
    if max_p50 > avg_p50 * 1.5:
        max_idx = p50.index(max_p50)
        peak_date = dates[max_idx]
        render_alert(
            f"Pic de demande prévu le {peak_date} avec {max_p50:.0f} unités (50% au-dessus de la moyenne). Préparez des stocks suffisants.",
            "warning",
            "⚠️ Pic de Demande"
        )
    
    # Recommandation pour le planning
    total_forecast = sum(p50)
    render_alert(
        f"Pour les {horizon} prochains jours, prévoyez un stock minimum de {total_forecast:.0f} unités (scénario médian). Pour un niveau de service élevé (90%), prévoyez {sum(p90):.0f} unités.",
        "success",
        "✅ Recommandation de Stock"
    )