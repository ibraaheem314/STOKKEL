"""
🎯 STOKKEL MOCK DATA SYSTEM
===========================

Système de données réalistes pour démonstration
- 12 produits avec historique de 90 jours
- Prévisions probabilistes (P10, P50, P90)
- Recommandations calculées automatiquement
- KPIs cohérents sur toutes les pages
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

# ============================================
# CONFIGURATION DES DONNÉES
# ============================================

PRODUCT_CATALOG = [
    {"id": "P001", "name": "Smartphone Galaxy S24", "category": "Électronique", "price": 899.99, "avg_monthly_sales": 45},
    {"id": "P002", "name": "Laptop Pro 15\"", "category": "Électronique", "price": 1299.99, "avg_monthly_sales": 28},
    {"id": "P003", "name": "Écouteurs Wireless", "category": "Audio", "price": 199.99, "avg_monthly_sales": 67},
    {"id": "P004", "name": "Tablette iPad Air", "category": "Électronique", "price": 599.99, "avg_monthly_sales": 34},
    {"id": "P005", "name": "Smartwatch Series 9", "category": "Wearable", "price": 399.99, "avg_monthly_sales": 52},
    {"id": "P006", "name": "Câble USB-C 2m", "category": "Accessoires", "price": 29.99, "avg_monthly_sales": 89},
    {"id": "P007", "name": "Chargeur Sans Fil", "category": "Accessoires", "price": 79.99, "avg_monthly_sales": 43},
    {"id": "P008", "name": "Écran 27\" 4K", "category": "Électronique", "price": 399.99, "avg_monthly_sales": 23},
    {"id": "P009", "name": "Clavier Mécanique", "category": "Accessoires", "price": 149.99, "avg_monthly_sales": 38},
    {"id": "P010", "name": "Souris Gaming", "category": "Accessoires", "price": 89.99, "avg_monthly_sales": 56},
    {"id": "P011", "name": "Webcam HD 1080p", "category": "Électronique", "price": 129.99, "avg_monthly_sales": 41},
    {"id": "P012", "name": "Micro Casque Gaming", "category": "Audio", "price": 199.99, "avg_monthly_sales": 29}
]

class MockDataSystem:
    """Système de données mock pour Stokkel"""
    
    def __init__(self):
        self.initialized = False
        self.sales_history = None
        self.inventory = None
        self.forecasts = None
        self.recommendations = None
        self.kpis = None
        
    def initialize(self):
        """Initialise toutes les données mock"""
        if self.initialized:
            return
            
        # Générer l'historique des ventes
        self.sales_history = self._generate_sales_history()
        
        # Calculer l'inventaire actuel
        self.inventory = self._calculate_inventory()
        
        # Générer les prévisions
        self.forecasts = self._generate_forecasts()
        
        # Calculer les recommandations
        self.recommendations = self._calculate_recommendations()
        
        # Calculer les KPIs
        self.kpis = self._calculate_kpis()
        
        self.initialized = True
    
    def _generate_sales_history(self) -> pd.DataFrame:
        """Génère l'historique des ventes sur 90 jours"""
        start_date = datetime.now() - timedelta(days=90)
        dates = [start_date + timedelta(days=i) for i in range(90)]
        
        sales_data = []
        
        for product in PRODUCT_CATALOG:
            product_id = product["id"]
            avg_daily = product["avg_monthly_sales"] / 30
            
            for date in dates:
                # Base sales avec variation
                base_sales = avg_daily * (1 + np.random.normal(0, 0.3))
                
                # Effet weekend (moins de ventes)
                if date.weekday() >= 5:  # Weekend
                    base_sales *= 0.7
                
                # Saisonnalité (plus de ventes en fin de mois)
                if date.day > 20:
                    base_sales *= 1.2
                
                # Événements rares (promotions)
                if random.random() < 0.05:  # 5% chance
                    base_sales *= 2.5
                
                # Ruptures occasionnelles
                if random.random() < 0.02:  # 2% chance
                    base_sales = 0
                
                sales_data.append({
                    'product_id': product_id,
                    'date': date,
                    'quantity': max(0, int(base_sales))
                })
        
        return pd.DataFrame(sales_data)
    
    def _calculate_inventory(self) -> Dict[str, int]:
        """Calcule l'inventaire actuel basé sur les ventes"""
        inventory = {}
        
        for product in PRODUCT_CATALOG:
            product_id = product["id"]
            
            # Ventes des 7 derniers jours
            recent_sales = self.sales_history[
                (self.sales_history['product_id'] == product_id) &
                (self.sales_history['date'] >= datetime.now() - timedelta(days=7))
            ]['quantity'].sum()
            
            # Stock de sécurité (2 semaines de ventes)
            safety_stock = int(recent_sales * 2)
            
            # Stock actuel (aléatoire entre 0.5x et 2x le stock de sécurité)
            current_stock = int(safety_stock * random.uniform(0.5, 2.0))
            
            inventory[product_id] = current_stock
        
        return inventory
    
    def _generate_forecasts(self) -> Dict[str, Dict]:
        """Génère les prévisions pour chaque produit"""
        forecasts = {}
        
        for product in PRODUCT_CATALOG:
            product_id = product["id"]
            avg_daily = product["avg_monthly_sales"] / 30
            
            # Prévisions pour les 30 prochains jours
            forecast_data = []
            for day in range(30):
                date = datetime.now() + timedelta(days=day+1)
                
                # Base forecast
                base_forecast = avg_daily * (1 + np.random.normal(0, 0.2))
                
                # P10, P50, P90
                p10 = int(base_forecast * 0.7)
                p50 = int(base_forecast)
                p90 = int(base_forecast * 1.4)
                
                forecast_data.append({
                    'date': date,
                    'p10': p10,
                    'p50': p50,
                    'p90': p90
                })
            
            forecasts[product_id] = {
                'forecast_data': forecast_data,
                'accuracy': random.uniform(0.85, 0.95),
                'mape': random.uniform(5, 15)
            }
        
        return forecasts
    
    def _calculate_recommendations(self) -> List[Dict]:
        """Calcule les recommandations pour chaque produit"""
        recommendations = []
        
        for product in PRODUCT_CATALOG:
            product_id = product["id"]
            current_stock = self.inventory.get(product_id, 0)
            
            # Ventes moyennes des 7 derniers jours
            recent_sales = self.sales_history[
                (self.sales_history['product_id'] == product_id) &
                (self.sales_history['date'] >= datetime.now() - timedelta(days=7))
            ]['quantity'].mean()
            
            # Point de commande (2 semaines de ventes)
            reorder_point = int(recent_sales * 14)
            
            # Délai de livraison (3-7 jours)
            lead_time = random.randint(3, 7)
            
            # Niveau de service (90-99%)
            service_level = random.uniform(0.90, 0.99)
            
            # Calcul de la recommandation
            if current_stock < reorder_point:
                urgency = "high"
                action = f"Commander {reorder_point - current_stock + int(recent_sales * lead_time)}"
                impact_value = product["price"] * (reorder_point - current_stock)
            else:
                urgency = "normal"
                action = "Surveiller"
                impact_value = 0
            
            recommendations.append({
                'product_id': product_id,
                'product_name': product["name"],
                'current_stock': current_stock,
                'reorder_point': reorder_point,
                'forecast_7d': int(recent_sales * 7),
                'urgency': urgency,
                'action': action,
                'impact_value': impact_value,
                'lead_time_days': lead_time,
                'service_level_percent': int(service_level * 100)
            })
        
        return recommendations
    
    def _calculate_kpis(self) -> Dict[str, Any]:
        """Calcule les KPIs globaux"""
        total_products = len(PRODUCT_CATALOG)
        
        # Précision moyenne des prévisions
        avg_accuracy = np.mean([f['accuracy'] for f in self.forecasts.values()])
        
        # Économies estimées (basées sur les recommandations)
        total_savings = sum([r['impact_value'] for r in self.recommendations if r['urgency'] == 'high'])
        
        # Ruptures évitées (produits avec stock critique)
        critical_products = len([r for r in self.recommendations if r['urgency'] == 'high'])
        
        # Taux de service global
        service_level = np.mean([r['service_level_percent'] for r in self.recommendations])
        
        return {
            'total_products': total_products,
            'avg_accuracy': avg_accuracy,
            'forecast_accuracy': avg_accuracy * 100,  # Convertir en pourcentage
            'forecast_accuracy_delta': random.uniform(2.0, 5.0),  # Variation de précision
            'total_savings': total_savings,
            'potential_savings': total_savings,  # Alias pour potential_savings
            'savings_delta': random.uniform(10.0, 25.0),  # Variation des économies
            'critical_products': critical_products,
            'urgent_actions': critical_products,  # Alias pour urgent_actions
            'actions_delta': random.uniform(-5.0, 5.0),  # Variation des actions
            'service_level': service_level,
            'total_records': len(self.sales_history),
            'date_range': '90 jours',
            'products_delta': random.uniform(0.0, 3.0),  # Variation du nombre de produits
            'accuracy_delta': random.uniform(1.0, 4.0),  # Variation de précision
            'savings_percentage': (total_savings / 1000000) * 100,  # Pourcentage d'économies
            'ruptures_evitees': critical_products,  # Alias pour ruptures évitées
            'stockouts_avoided': critical_products,  # Alias pour stockouts_avoided
            'stockouts_avoided_delta': random.uniform(-5.0, 5.0),  # Variation des ruptures évitées
            'service_level_delta': random.uniform(1.0, 3.0),  # Variation du niveau de service
            'stockout_rate': random.uniform(2.0, 8.0),  # Taux de rupture
            'stockout_rate_delta': random.uniform(-2.0, 1.0),  # Variation du taux de rupture
            'total_sales_records': len(self.sales_history),  # Nombre total d'enregistrements
            'data_period_days': 90,  # Période des données
            'last_update': datetime.now().isoformat(),  # Dernière mise à jour
            'products_with_forecast': total_products,  # Produits avec prévisions
            'optimized_products': int(total_products * 0.8)  # Produits optimisés
        }
    
    # ============================================
    # MÉTHODES PUBLIQUES
    # ============================================
    
    def get_sales_history(self) -> pd.DataFrame:
        """Retourne l'historique des ventes"""
        if not self.initialized:
            self.initialize()
        return self.sales_history
    
    def get_inventory(self) -> Dict[str, int]:
        """Retourne l'inventaire actuel"""
        if not self.initialized:
            self.initialize()
        return self.inventory
    
    def get_forecasts(self) -> Dict[str, Dict]:
        """Retourne les prévisions"""
        if not self.initialized:
            self.initialize()
        return self.forecasts
    
    def get_recommendations(self) -> List[Dict]:
        """Retourne les recommandations"""
        if not self.initialized:
            self.initialize()
        return self.recommendations
    
    def get_kpis(self) -> Dict[str, Any]:
        """Retourne les KPIs"""
        if not self.initialized:
            self.initialize()
        return self.kpis
    
    def get_products(self) -> List[Dict]:
        """Retourne le catalogue des produits"""
        return PRODUCT_CATALOG
    
    def get_critical_alerts(self) -> List[Dict]:
        """Retourne les alertes critiques"""
        if not self.initialized:
            self.initialize()
        
        alerts = []
        for rec in self.recommendations:
            if rec['urgency'] == 'high':
                alerts.append({
                    'product_id': rec['product_id'],
                    'product_name': rec['product_name'],
                    'message': f"Stock critique: {rec['current_stock']} unités restantes",
                    'action': rec['action'],
                    'impact': rec['impact_value'],
                    'urgency': rec['urgency']
                })
        
        return alerts
    
    def get_product_list(self) -> List[Dict]:
        """Retourne la liste des produits pour sélection"""
        if not self.initialized:
            self.initialize()
        
        product_list = []
        for product in PRODUCT_CATALOG:
            product_list.append({
                'id': product['id'],
                'name': product['name'],
                'category': product['category']
            })
        
        return product_list
    
    def get_sales_history(self, product_id: str = None) -> pd.DataFrame:
        """Retourne l'historique des ventes pour un produit ou tous"""
        if not self.initialized:
            self.initialize()
        
        if product_id:
            return self.sales_history[self.sales_history['product_id'] == product_id]
        return self.sales_history
    
    def get_forecasts(self, product_id: str = None) -> Dict:
        """Retourne les prévisions pour un produit ou tous"""
        if not self.initialized:
            self.initialize()
        
        if product_id:
            # Retourner un dictionnaire avec forecast_data comme DataFrame
            if product_id in self.forecasts:
                forecast_dict = self.forecasts[product_id]
                # Convertir la liste en DataFrame
                import pandas as pd
                forecast_data = pd.DataFrame(forecast_dict['forecast_data'])
                return {
                    'forecast_data': forecast_data,
                    'accuracy': forecast_dict.get('accuracy', random.uniform(85.0, 95.0)),
                    'mape': forecast_dict.get('mape', random.uniform(5.0, 15.0))
                }
            return {}
        return self.forecasts

# ============================================
# INSTANCE GLOBALE
# ============================================

mock_data = MockDataSystem()

# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def format_currency(amount: float) -> str:
    """Formate un montant en devise"""
    return f"{amount:,.0f} €"

def format_percentage(value: float) -> str:
    """Formate un pourcentage"""
    return f"{value:.1f}%"

def format_delta(value: float) -> str:
    """Formate une variation"""
    if value > 0:
        return f"+{value:.1f}%"
    else:
        return f"{value:.1f}%"
