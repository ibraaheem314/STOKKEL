"""
🚀 STOKKEL DASHBOARD V2 - COMPOSANTS INTELLIGENTS
===================================================

Composants V2 pour intégration progressive dans V1:
1. Smart KPIs avec contexte et insights
2. Decision Intelligence Panel
3. Auto-Annotated Charts
4. Business Context enrichi

USAGE:
from components.v2_components import (
    SmartKPI,
    DecisionIntelligencePanel,
    SmartChart,
    BusinessContextKPI
)
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# ============================================
# DATA MODELS
# ============================================

class TrendDirection(Enum):
    """Direction de tendance"""
    UP = "📈"
    DOWN = "📉"
    STABLE = "➡️"

class UrgencyLevel(Enum):
    """Niveau d'urgence"""
    CRITICAL = "🔴"
    HIGH = "🟠"
    MEDIUM = "🟡"
    LOW = "🟢"

@dataclass
class Insight:
    """Un insight automatique"""
    text: str
    confidence: float  # 0-1
    supporting_data: Dict
    actions: List[str]

@dataclass
class Scenario:
    """Un scénario de décision"""
    name: str
    cost: float
    roi: float
    risk_probability: float
    expected_outcome: float
    pros: List[str]
    cons: List[str]

# ============================================
# 1. SMART KPI - KPI INTELLIGENT
# ============================================

class SmartKPI:
    """
    KPI Intelligent avec contexte, benchmarks et insights automatiques
    
    Example:
        kpi = SmartKPI(
            label="Précision Prévisions",
            value=87.3,
            target=90,
            previous=85.2,
            benchmark=82
        )
        kpi.render()
    """
    
    def __init__(
        self,
        label: str,
        value: float,
        target: Optional[float] = None,
        previous: Optional[float] = None,
        benchmark: Optional[float] = None,
        unit: str = "%",
        icon: str = "📊",
        trend_data: Optional[List[float]] = None
    ):
        self.label = label
        self.value = value
        self.target = target
        self.previous = previous
        self.benchmark = benchmark
        self.unit = unit
        self.icon = icon
        self.trend_data = trend_data or []
    
    def calculate_gap_to_target(self) -> Tuple[float, str]:
        """Calcule l'écart à l'objectif"""
        if self.target is None:
            return 0, ""
        
        gap = self.value - self.target
        if abs(gap) < 0.5:
            status = "🎯 Objectif atteint"
        elif gap > 0:
            status = f"✅ Au-dessus de {abs(gap):.1f}{self.unit}"
        else:
            status = f"⚠️ En dessous de {abs(gap):.1f}{self.unit}"
        
        return gap, status
    
    def calculate_mom_change(self) -> Tuple[float, TrendDirection]:
        """Calcule changement vs mois précédent"""
        if self.previous is None:
            return 0, TrendDirection.STABLE
        
        change = self.value - self.previous
        pct_change = (change / self.previous) * 100
        
        if abs(pct_change) < 2:
            direction = TrendDirection.STABLE
        elif pct_change > 0:
            direction = TrendDirection.UP
        else:
            direction = TrendDirection.DOWN
        
        return pct_change, direction
    
    def compare_to_benchmark(self) -> Tuple[float, str]:
        """Compare au benchmark secteur"""
        if self.benchmark is None:
            return 0, ""
        
        diff = self.value - self.benchmark
        if abs(diff) < 1:
            status = "≈ Équivalent secteur"
        elif diff > 0:
            status = f"🏆 {abs(diff):.1f}{self.unit} au-dessus secteur"
        else:
            status = f"⚠️ {abs(diff):.1f}{self.unit} en dessous secteur"
        
        return diff, status
    
    def generate_auto_insight(self) -> Insight:
        """Génère insight automatique basé sur les données"""
        
        gap, _ = self.calculate_gap_to_target()
        mom_change, direction = self.calculate_mom_change()
        bench_diff, _ = self.compare_to_benchmark()
        
        # Logique d'insight intelligente
        if gap >= 0 and mom_change > 0 and bench_diff > 0:
            text = f"Excellente performance ! {direction.value} progression continue. Maintenir cette trajectoire."
            confidence = 0.9
            actions = ["Documenter les bonnes pratiques", "Partager avec l'équipe"]
        
        elif gap < 0 and mom_change > 0:
            text = f"En progression {direction.value} (+{abs(mom_change):.1f}%). Objectif atteignable sous {abs(gap / mom_change):.0f} mois."
            confidence = 0.85
            actions = ["Continuer les efforts actuels", "Monitorer hebdomadairement"]
        
        elif gap >= 0 and mom_change < 0:
            text = f"⚠️ Dégradation détectée {direction.value} (-{abs(mom_change):.1f}%). Investigate causes."
            confidence = 0.8
            actions = ["Analyser causes de la baisse", "Mettre en place actions correctives"]
        
        else:
            text = f"Performance {direction.value} stable. Monitoring requis."
            confidence = 0.75
            actions = ["Suivre l'évolution", "Réévaluer objectif si nécessaire"]
        
        return Insight(
            text=text,
            confidence=confidence,
            supporting_data={
                'gap': gap,
                'mom_change': mom_change,
                'benchmark_diff': bench_diff
            },
            actions=actions
        )
    
    def render(self):
        """Rend le KPI intelligent avec composants Streamlit natifs"""
        
        gap, gap_status = self.calculate_gap_to_target()
        mom_change, direction = self.calculate_mom_change()
        bench_diff, bench_status = self.compare_to_benchmark()
        insight = self.generate_auto_insight()
        
        # Utiliser les composants Streamlit natifs - plus fiable
        with st.container():
            # Titre du KPI
            st.markdown(f"**{self.icon} {self.label}**")
            
            # Valeur principale avec st.metric
            if self.target:
                delta_value = f"{self.value - self.target:+.1f}{self.unit}" if self.value != self.target else None
                st.metric(
                    label="",
                    value=f"{self.value:.1f}{self.unit}",
                    delta=delta_value
                )
            else:
                st.metric(
                    label="",
                    value=f"{self.value:.1f}{self.unit}",
                    delta=None
                )
            
            # Informations supplémentaires
            if self.target:
                st.caption(f"Objectif: {self.target:.1f}{self.unit}")
            
            if self.previous:
                st.caption(f"vs Mois dernier: {self.previous:.1f}{self.unit} ({direction.value} {mom_change:+.1f}%)")
            
            if self.benchmark:
                st.caption(f"Benchmark: {self.benchmark:.1f}{self.unit}")
        
        # Contexte détaillé dans expander
        with st.expander("📊 Contexte & Insights", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📍 Contexte**")
                
                if self.target:
                    st.markdown(f"🎯 **Objectif:** {self.target:.1f}{self.unit}")
                    st.markdown(f"└─ {gap_status}")
                
                if self.previous:
                    st.markdown(f"📈 **vs Mois dernier:** {self.previous:.1f}{self.unit}")
                    st.markdown(f"└─ {direction.value} {mom_change:+.1f}%")
                
                if self.benchmark:
                    st.markdown(f"🏆 **Benchmark secteur:** {self.benchmark:.1f}{self.unit}")
                    st.markdown(f"└─ {bench_status}")
            
            with col2:
                st.markdown(f"**💡 Insight (Confiance: {insight.confidence*100:.0f}%)**")
                st.info(insight.text)
                
                if insight.actions:
                    st.markdown("**⚡ Actions Suggérées:**")
                    for i, action in enumerate(insight.actions, 1):
                        st.markdown(f"{i}. {action}")
            
            # Mini sparkline si données de tendance
            if self.trend_data:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=self.trend_data,
                    mode='lines',
                    fill='tozeroy',
                    line=dict(color='#D2691E', width=2),
                    fillcolor='rgba(210, 105, 30, 0.1)'
                ))
                fig.update_layout(
                    height=100,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=False, showticklabels=False)
                )
                st.plotly_chart(fig, use_container_width=True)


# ============================================
# 2. DECISION INTELLIGENCE PANEL
# ============================================

class DecisionIntelligencePanel:
    """
    Panneau d'aide à la décision avec priorisation et simulation
    
    Example:
        panel = DecisionIntelligencePanel(recommendations)
        panel.render()
    """
    
    def __init__(self, recommendations: List[Dict]):
        self.recommendations = recommendations
    
    def calculate_priority_score(self, recommendation: Dict) -> float:
        """Calcule score de priorité (ROI × Urgence × Confiance)"""
        
        roi = recommendation.get('roi', 0)
        urgency = self._urgency_to_score(recommendation.get('urgency', 'low'))
        confidence = recommendation.get('confidence', 0.5)
        
        # Score pondéré
        score = (roi / 1000) * urgency * confidence
        
        return score
    
    def _urgency_to_score(self, urgency: str) -> float:
        """Convertit urgence en score"""
        mapping = {
            'critical': 1.0,
            'high': 0.75,
            'medium': 0.5,
            'low': 0.25
        }
        return mapping.get(urgency.lower(), 0.5)
    
    def prioritize_recommendations(self) -> List[Dict]:
        """Trie recommandations par priorité"""
        
        scored = []
        for rec in self.recommendations:
            score = self.calculate_priority_score(rec)
            scored.append({**rec, 'priority_score': score})
        
        return sorted(scored, key=lambda x: x['priority_score'], reverse=True)
    
    def create_scenarios(self, recommendation: Dict) -> List[Scenario]:
        """Crée scénarios de décision"""
        
        base_qty = recommendation.get('quantity_to_order', 50)
        unit_cost = recommendation.get('unit_cost', 500)
        expected_revenue = recommendation.get('expected_revenue', 120000)
        
        scenarios = []
        
        # Scénario A: Recommandation IA
        scenarios.append(Scenario(
            name="Scénario A: Recommandation IA",
            cost=base_qty * unit_cost,
            roi=(expected_revenue - (base_qty * unit_cost)) / (base_qty * unit_cost) * 100,
            risk_probability=0.02,
            expected_outcome=expected_revenue,
            pros=[
                "ROI maximal",
                "Risque minimal de rupture (2%)",
                "Optimisé par IA"
            ],
            cons=[
                "Investissement plus élevé"
            ]
        ))
        
        # Scénario B: Quantité réduite
        reduced_qty = int(base_qty * 0.6)
        reduced_revenue = expected_revenue * 0.7
        scenarios.append(Scenario(
            name="Scénario B: Quantité Réduite",
            cost=reduced_qty * unit_cost,
            roi=(reduced_revenue - (reduced_qty * unit_cost)) / (reduced_qty * unit_cost) * 100,
            risk_probability=0.15,
            expected_outcome=reduced_revenue,
            pros=[
                "Investissement réduit",
                "ROI% plus élevé"
            ],
            cons=[
                "Risque rupture (15%)",
                "CA potentiel réduit"
            ]
        ))
        
        # Scénario C: Ne rien faire
        scenarios.append(Scenario(
            name="Scénario C: Ne Rien Faire",
            cost=0,
            roi=-100,
            risk_probability=0.87,
            expected_outcome=-recommendation.get('stockout_cost', 200000),
            pros=[
                "Aucun coût immédiat"
            ],
            cons=[
                "Rupture quasi-certaine (87%)",
                "Perte CA importante",
                "Insatisfaction clients"
            ]
        ))
        
        return scenarios
    
    def render(self):
        """Rend le panneau de décision"""
        
        st.markdown("## 🎯 Decision Intelligence Center")
        st.markdown("*Actions prioritaires triées par ROI et impact*")
        
        # Prioriser
        prioritized = self.prioritize_recommendations()
        
        # Top 3 actions
        st.markdown("### 🔥 TOP 3 ACTIONS À FORT IMPACT")
        
        for i, rec in enumerate(prioritized[:3], 1):
            urgency_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(rec.get('urgency', 'medium').lower(), '🟡')
            
            with st.container():
                st.markdown(f"""
                    <div style="
                        background: white;
                        border: 3px solid {'#E53E3E' if rec.get('urgency') == 'critical' else '#E8E8E8'};
                        border-radius: 12px;
                        padding: 24px;
                        margin-bottom: 24px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    ">
                        <div style="font-size: 20px; font-weight: 700; color: #1B4965; margin-bottom: 8px;">
                            #{i} {rec.get('title', 'Action')}
                        </div>
                        <div style="font-size: 14px; color: #6B6B6B; margin-bottom: 16px;">
                            Priorité: {urgency_emoji} {rec.get('urgency', 'MEDIUM').upper()} | 
                            Confiance: {rec.get('confidence', 0.8)*100:.0f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Tabs: Impact / Simulation / Détails
                tab1, tab2, tab3 = st.tabs(["💰 Impact", "🎲 Simulation", "🔍 Détails"])
                
                with tab1:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Investissement",
                            f"{rec.get('cost', 25000):,.0f} FCFA",
                            help="Coût de l'action"
                        )
                    
                    with col2:
                        st.metric(
                            "ROI Attendu",
                            f"+{rec.get('roi', 95000):,.0f} FCFA",
                            f"{rec.get('roi_percent', 380):.0f}%",
                            help="Retour sur investissement"
                        )
                    
                    with col3:
                        st.metric(
                            "Risque Inaction",
                            f"{rec.get('risk_probability', 0.87)*100:.0f}%",
                            f"-{rec.get('inaction_cost', 200000):,.0f} FCFA",
                            delta_color="inverse",
                            help="Risque si action non prise"
                        )
                
                with tab2:
                    st.markdown("**🎲 Comparaison de Scénarios**")
                    
                    scenarios = self.create_scenarios(rec)
                    
                    scenario_data = []
                    for scenario in scenarios:
                        scenario_data.append({
                            'Scénario': scenario.name,
                            'Coût': f"{scenario.cost:,.0f} FCFA",
                            'ROI': f"{scenario.roi:.0f}%",
                            'Risque': f"{scenario.risk_probability*100:.0f}%",
                            'Résultat': f"{scenario.expected_outcome:,.0f} FCFA"
                        })
                    
                    df_scenarios = pd.DataFrame(scenario_data)
                    st.dataframe(df_scenarios, width='stretch', hide_index=True)
                    
                    # Recommandation
                    st.success(f"💡 **Recommandation:** {scenarios[0].name} - ROI maximal avec risque minimal")
                    
                    # Slider interactif
                    st.markdown("**Ajuster la quantité:**")
                    qty = st.slider(
                        "Quantité à commander",
                        min_value=10,
                        max_value=100,
                        value=rec.get('quantity_to_order', 50),
                        step=5,
                        key=f"qty_slider_{i}"
                    )
                    
                    # Calcul dynamique
                    dynamic_cost = qty * rec.get('unit_cost', 500)
                    dynamic_roi = (rec.get('expected_revenue', 120000) - dynamic_cost) / dynamic_cost * 100
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Coût Simulé", f"{dynamic_cost:,.0f} FCFA")
                    with col2:
                        st.metric("ROI Simulé", f"{dynamic_roi:.0f}%")
                
                with tab3:
                    st.markdown("**📊 Contexte Opérationnel**")
                    
                    context_data = {
                        'Stock Actuel': rec.get('current_stock', 25),
                        'Consommation/jour': rec.get('daily_consumption', 5),
                        'Autonomie Actuelle': f"{rec.get('current_stock', 25) / rec.get('daily_consumption', 5):.0f} jours",
                        'Délai Réappro': f"{rec.get('lead_time', 7)} jours",
                        'MOQ Fournisseur': rec.get('moq', 10),
                        'Fiabilité Fournisseur': f"{rec.get('supplier_reliability', 0.92)*100:.0f}%"
                    }
                    
                    for key, value in context_data.items():
                        st.markdown(f"**{key}:** {value}")
                    
                    st.markdown("---")
                    st.markdown("**💡 Pourquoi Maintenant?**")
                    st.info(rec.get('reasoning', "Action recommandée par l'IA basée sur l'analyse des données historiques et des tendances actuelles."))
                
                # Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"✅ Approuver", key=f"approve_{i}", type="primary"):
                        st.success("✅ Action approuvée et ajoutée à la file d'exécution")
                
                with col2:
                    if st.button(f"📋 Créer Bon Commande", key=f"order_{i}"):
                        st.info("📋 Bon de commande généré - À télécharger")
                
                with col3:
                    if st.button(f"⏰ Reporter (+24h)", key=f"snooze_{i}"):
                        st.warning("⏰ Action reportée de 24h - Rappel créé")


# ============================================
# 3. SMART CHART - GRAPHIQUE INTELLIGENT
# ============================================

class SmartChart:
    """
    Graphique intelligent avec annotations automatiques
    
    Example:
        chart = SmartChart(sales_data, forecast_data)
        chart.render()
    """
    
    def __init__(
        self,
        historical_data: pd.DataFrame,
        forecast_data: Optional[pd.DataFrame] = None
    ):
        self.historical = historical_data
        self.forecast = forecast_data
    
    def detect_significant_events(self) -> List[Dict]:
        """Détecte événements significatifs (pics, creux)"""
        
        if 'quantity' not in self.historical.columns:
            return []
        
        quantities = self.historical['quantity'].values
        mean = quantities.mean()
        std = quantities.std()
        
        events = []
        
        for idx, row in self.historical.iterrows():
            qty = row['quantity']
            z_score = (qty - mean) / std
            
            if abs(z_score) > 2:  # Événement significatif
                event_type = "Pic" if z_score > 0 else "Creux"
                magnitude = abs((qty - mean) / mean * 100)
                
                events.append({
                    'date': row.get('date', idx),
                    'type': event_type,
                    'value': qty,
                    'magnitude': magnitude,
                    'label': f"{event_type} +{magnitude:.0f}%" if z_score > 0 else f"{event_type} -{magnitude:.0f}%"
                })
        
        return events
    
    def detect_anomalies(self) -> List[Dict]:
        """Détecte anomalies dans les données"""
        
        # Méthode IQR simple
        Q1 = self.historical['quantity'].quantile(0.25)
        Q3 = self.historical['quantity'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomalies = []
        
        for idx, row in self.historical.iterrows():
            qty = row['quantity']
            
            if qty < lower_bound or qty > upper_bound:
                anomalies.append({
                    'date': row.get('date', idx),
                    'value': qty,
                    'type': 'high' if qty > upper_bound else 'low'
                })
        
        return anomalies
    
    def detect_patterns(self) -> Dict:
        """Détecte patterns (tendance, saisonnalité)"""
        
        quantities = self.historical['quantity'].values
        
        # Tendance simple (régression linéaire)
        x = np.arange(len(quantities))
        slope = np.polyfit(x, quantities, 1)[0]
        
        if abs(slope) < 0.1:
            trend = "Stable"
            trend_emoji = "➡️"
        elif slope > 0:
            trend = "Croissante"
            trend_emoji = "📈"
        else:
            trend = "Décroissante"
            trend_emoji = "📉"
        
        # Variabilité
        cv = (quantities.std() / quantities.mean()) * 100
        
        if cv < 10:
            variability = "Faible"
        elif cv < 25:
            variability = "Modérée"
        else:
            variability = "Élevée"
        
        return {
            'trend': trend,
            'trend_emoji': trend_emoji,
            'trend_slope': slope,
            'variability': variability,
            'coefficient_variation': cv
        }
    
    def render(self):
        """Rend le graphique intelligent"""
        
        fig = go.Figure()
        
        # Historique
        fig.add_trace(go.Scatter(
            x=self.historical.get('date', self.historical.index),
            y=self.historical['quantity'],
            name='Ventes Historiques',
            line=dict(color='#1B4965', width=2),
            mode='lines+markers',
            marker=dict(size=6)
        ))
        
        # Prévisions si disponibles
        if self.forecast is not None:
            fig.add_trace(go.Scatter(
                x=self.forecast.get('date', self.forecast.index),
                y=self.forecast.get('p50', self.forecast['quantity']),
                name='Prévision (P50)',
                line=dict(color='#D2691E', width=2, dash='dash')
            ))
            
            # Bandes de confiance
            if 'p10' in self.forecast.columns and 'p90' in self.forecast.columns:
                fig.add_trace(go.Scatter(
                    x=self.forecast.get('date', self.forecast.index),
                    y=self.forecast['p90'],
                    fill=None,
                    mode='lines',
                    line=dict(color='rgba(210, 105, 30, 0)'),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=self.forecast.get('date', self.forecast.index),
                    y=self.forecast['p10'],
                    fill='tonexty',
                    mode='lines',
                    line=dict(color='rgba(210, 105, 30, 0)'),
                    fillcolor='rgba(210, 105, 30, 0.2)',
                    name='Intervalle Confiance (P10-P90)'
                ))
        
        # Annotations automatiques
        events = self.detect_significant_events()
        for event in events[:5]:  # Max 5 annotations
            fig.add_annotation(
                x=event['date'],
                y=event['value'],
                text=event['label'],
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='#D2691E',
                bgcolor='white',
                bordercolor='#D2691E',
                borderwidth=2
            )
        
        # Layout
        fig.update_layout(
            title="Ventes Historiques et Prévisions avec Événements Clés",
            xaxis_title="Date",
            yaxis_title="Quantité",
            height=500,
            template='plotly_white',
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights automatiques
        patterns = self.detect_patterns()
        anomalies = self.detect_anomalies()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Tendance Détectée",
                patterns['trend'],
                patterns['trend_emoji']
            )
        
        with col2:
            st.metric(
                "Variabilité",
                patterns['variability'],
                f"{patterns['coefficient_variation']:.1f}%"
            )
        
        with col3:
            st.metric(
                "Anomalies",
                len(anomalies),
                "À investiguer" if len(anomalies) > 0 else "Aucune"
            )
        
        # Insights textuels
        with st.expander("💡 Insights Automatiques", expanded=True):
            st.markdown("**📊 Analyse des Patterns:**")
            st.info(f"""
            - **Tendance:** {patterns['trend_emoji']} {patterns['trend']} (pente: {patterns['trend_slope']:.2f})
            - **Variabilité:** {patterns['variability']} (CV: {patterns['coefficient_variation']:.1f}%)
            - **Événements détectés:** {len(events)} pics/creux significatifs
            - **Anomalies:** {len(anomalies)} valeurs atypiques détectées
            """)
            
            if events:
                st.markdown("**🔥 Événements Majeurs:**")
                for event in events[:3]:
                    st.markdown(f"- {event['date']}: {event['label']}")


# ============================================
# 4. BUSINESS CONTEXT KPI
# ============================================

class BusinessContextKPI:
    """
    KPI avec contexte métier enrichi (coûts, délais, ROI)
    
    Example:
        kpi = BusinessContextKPI(
            metric="Stock Actuel",
            value=25,
            context={
                "cost_per_unit": 500,
                "holding_cost_rate": 0.15,
                "lead_time_days": 7
            }
        )
        kpi.render()
    """
    
    def __init__(
        self,
        metric: str,
        value: float,
        context: Dict,
        unit: str = "unités",
        icon: str = "📦"
    ):
        self.metric = metric
        self.value = value
        self.context = context
        self.unit = unit
        self.icon = icon
    
    def calculate_financial_impact(self) -> Dict:
        """Calcule l'impact financier"""
        
        cost_per_unit = self.context.get('cost_per_unit', 0)
        holding_cost_rate = self.context.get('holding_cost_rate', 0.15)
        
        total_value = self.value * cost_per_unit
        monthly_holding_cost = total_value * (holding_cost_rate / 12)
        
        return {
            'total_value': total_value,
            'monthly_holding_cost': monthly_holding_cost,
            'annual_holding_cost': total_value * holding_cost_rate
        }
    
    def calculate_time_constraints(self) -> Dict:
        """Calcule les contraintes temporelles"""
        
        lead_time = self.context.get('lead_time_days', 7)
        daily_consumption = self.context.get('daily_consumption', 1)
        
        autonomy_days = self.value / daily_consumption if daily_consumption > 0 else 0
        reorder_point_days = lead_time + 2  # +2 jours de sécurité
        
        return {
            'autonomy_days': autonomy_days,
            'reorder_point_days': reorder_point_days,
            'lead_time_days': lead_time,
            'is_critical': autonomy_days <= reorder_point_days
        }
    
    def generate_business_insight(self) -> str:
        """Génère insight métier"""
        
        financial = self.calculate_financial_impact()
        time_constraints = self.calculate_time_constraints()
        
        if time_constraints['is_critical']:
            return f"🚨 **CRITIQUE** - Stock insuffisant ({time_constraints['autonomy_days']:.0f}j) pour couvrir délai réappro ({time_constraints['lead_time_days']}j). Commander immédiatement."
        elif time_constraints['autonomy_days'] < time_constraints['reorder_point_days'] + 3:
            return f"⚠️ **ATTENTION** - Stock faible ({time_constraints['autonomy_days']:.0f}j). Planifier commande sous 2-3 jours."
        else:
            return f"✅ **OPTIMAL** - Stock suffisant ({time_constraints['autonomy_days']:.0f}j). Surveillance normale."
    
    def render(self):
        """Rend le KPI avec contexte métier"""
        
        financial = self.calculate_financial_impact()
        time_constraints = self.calculate_time_constraints()
        insight = self.generate_business_insight()
        
        # Container principal
        st.markdown(f"""
            <div style="
                background: white;
                border: 2px solid {'#E53E3E' if time_constraints['is_critical'] else '#E8E8E8'};
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div>
                        <div style="font-size: 14px; color: #6B6B6B; text-transform: uppercase; letter-spacing: 0.05em;">
                            {self.icon} {self.metric}
                        </div>
                    </div>
                    <div style="
                        background: linear-gradient(135deg, #D2691E, #F4A261);
                        width: 40px;
                        height: 40px;
                        border-radius: 8px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                    ">{self.icon}</div>
                </div>
                
                <div style="font-size: 42px; font-weight: 700; color: #1B4965; margin: 16px 0;">
                    {self.value:.0f} {self.unit}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Contexte métier détaillé
        with st.expander("💼 Contexte Métier", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💰 Impact Financier**")
                st.metric("Valeur Stock", f"{financial['total_value']:,.0f} FCFA")
                st.metric("Coût Portage/mois", f"{financial['monthly_holding_cost']:,.0f} FCFA")
                st.metric("Coût Portage/an", f"{financial['annual_holding_cost']:,.0f} FCFA")
            
            with col2:
                st.markdown("**⏱️ Contraintes Temporelles**")
                st.metric("Autonomie", f"{time_constraints['autonomy_days']:.0f} jours")
                st.metric("Délai Réappro", f"{time_constraints['lead_time_days']} jours")
                st.metric("Point Commande", f"{time_constraints['reorder_point_days']} jours")
            
            st.markdown("---")
            st.markdown("**💡 Insight Métier**")
            st.info(insight)
