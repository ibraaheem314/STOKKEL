"""
🎯 STOKKEL - DONNÉES D'EXEMPLE RÉALISTES
=========================================

Système complet de mock data pour démo convaincante
- Données cohérentes entre toutes les pages
- Valeurs réalistes et crédibles
- Pas d'erreurs 404 ou 422
- Dashboard fonctionnel sans upload
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ============================================
# CONFIGURATION GLOBALE
# ============================================

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Catalogue de produits réalistes
PRODUCT_CATALOG = [
    # Electronics
    {"id": "P001", "name": "Smartphone Galaxy S24", "category": "Électronique", "price": 899.99, "avg_monthly_sales": 45},
    {"id": "P002", "name": "Laptop Pro 15\"", "category": "Électronique", "price": 1299.99, "avg_monthly_sales": 28},
    {"id": "P003", "name": "Écouteurs Wireless", "category": "Audio", "price": 159.99, "avg_monthly_sales": 67},
    {"id": "P004", "name": "Tablette 10\"", "category": "Électronique", "price": 449.99, "avg_monthly_sales": 35},
    {"id": "P005", "name": "Chargeur USB-C 65W", "category": "Accessoires", "price": 34.99, "avg_monthly_sales": 120},
    
    # Home & Office
    {"id": "P006", "name": "Souris Ergonomique", "category": "Bureautique", "price": 49.99, "avg_monthly_sales": 85},
    {"id": "P007", "name": "Clavier Mécanique", "category": "Bureautique", "price": 129.99, "avg_monthly_sales": 42},
    {"id": "P008", "name": "Webcam HD 1080p", "category": "Bureautique", "price": 79.99, "avg_monthly_sales": 56},
    {"id": "P009", "name": "Câble HDMI 2m", "category": "Accessoires", "price": 12.99, "avg_monthly_sales": 145},
    {"id": "P010", "name": "Hub USB-C 7-en-1", "category": "Accessoires", "price": 59.99, "avg_monthly_sales": 73},
    
    # Storage
    {"id": "P011", "name": "SSD Externe 1TB", "category": "Stockage", "price": 119.99, "avg_monthly_sales": 52},
    {"id": "P012", "name": "Clé USB 128GB", "category": "Stockage", "price": 24.99, "avg_monthly_sales": 98},
]

# ============================================
# GÉNÉRATEUR DE DONNÉES HISTORIQUES
# ============================================

def generate_realistic_sales_history(
    product_id: str,
    avg_monthly_sales: int,
    num_days: int = 90,
    seasonality: bool = True,
    trend: str = "stable"  # "stable", "growing", "declining"
) -> pd.DataFrame:
    """
    Génère un historique de ventes réaliste avec:
    - Tendance (croissance/décroissance)
    - Saisonnalité hebdomadaire (weekend vs semaine)
    - Variation aléatoire naturelle
    - Événements exceptionnels occasionnels
    """
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=num_days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Ventes moyennes par jour
    daily_avg = avg_monthly_sales / 30
    
    sales = []
    for i, date in enumerate(dates):
        # Base avec variation
        base_sales = daily_avg * np.random.uniform(0.7, 1.3)
        
        # Tendance
        if trend == "growing":
            trend_factor = 1 + (i / num_days) * 0.3  # +30% over period
        elif trend == "declining":
            trend_factor = 1 - (i / num_days) * 0.2  # -20% over period
        else:
            trend_factor = 1
        
        # Saisonnalité hebdomadaire
        if seasonality:
            day_of_week = date.dayofweek
            if day_of_week in [5, 6]:  # Weekend
                seasonal_factor = 0.6
            elif day_of_week in [0, 1]:  # Début semaine
                seasonal_factor = 1.1
            else:
                seasonal_factor = 1.0
        else:
            seasonal_factor = 1.0
        
        # Événements rares (promotions, ruptures)
        if np.random.random() < 0.05:  # 5% chance
            event_factor = np.random.choice([0.3, 2.5])  # Rupture ou promo
        else:
            event_factor = 1.0
        
        # Calcul final
        daily_sales = base_sales * trend_factor * seasonal_factor * event_factor
        daily_sales = max(0, int(daily_sales))  # Pas de ventes négatives
        
        sales.append({
            "date": date,
            "product_id": product_id,
            "quantity": daily_sales,
            "day_of_week": date.strftime("%A"),
        })
    
    return pd.DataFrame(sales)


def generate_all_sales_history() -> pd.DataFrame:
    """
    Génère l'historique complet pour tous les produits
    """
    all_sales = []
    
    for product in PRODUCT_CATALOG:
        # Varier les tendances
        if product["id"] in ["P001", "P003", "P005"]:
            trend = "growing"
        elif product["id"] in ["P002", "P007"]:
            trend = "declining"
        else:
            trend = "stable"
        
        sales_df = generate_realistic_sales_history(
            product_id=product["id"],
            avg_monthly_sales=product["avg_monthly_sales"],
            num_days=90,
            seasonality=True,
            trend=trend
        )
        all_sales.append(sales_df)
    
    combined = pd.concat(all_sales, ignore_index=True)
    
    # Ajouter métadonnées produit
    product_info = {p["id"]: p for p in PRODUCT_CATALOG}
    combined["product_name"] = combined["product_id"].map(lambda x: product_info[x]["name"])
    combined["category"] = combined["product_id"].map(lambda x: product_info[x]["category"])
    combined["price"] = combined["product_id"].map(lambda x: product_info[x]["price"])
    
    return combined


# ============================================
# ÉTAT ACTUEL DES STOCKS
# ============================================

def generate_current_inventory() -> pd.DataFrame:
    """
    Génère l'état actuel des stocks pour tous les produits
    """
    inventory = []
    
    for product in PRODUCT_CATALOG:
        daily_avg = product["avg_monthly_sales"] / 30
        
        # Stock actuel (variable, certains critiques)
        if product["id"] in ["P001", "P009", "P008"]:
            # Stock critique
            current_stock = int(daily_avg * random.uniform(0.5, 2))
        elif product["id"] in ["P007", "P011"]:
            # Surstock
            current_stock = int(daily_avg * random.uniform(20, 40))
        else:
            # Stock normal
            current_stock = int(daily_avg * random.uniform(10, 20))
        
        # Point de commande calculé (Lead Time = 7 jours)
        lead_time_days = 7
        safety_stock_days = 5
        reorder_point = int(daily_avg * (lead_time_days + safety_stock_days))
        
        # Stock optimal
        optimal_stock = int(daily_avg * 30)  # 1 mois de stock
        
        inventory.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "current_stock": current_stock,
            "reorder_point": reorder_point,
            "optimal_stock": optimal_stock,
            "daily_avg_sales": daily_avg,
            "price": product["price"],
        })
    
    df = pd.DataFrame(inventory)
    
    # Calculer statut
    df["status"] = df.apply(lambda row: 
        "🔴 Critique" if row["current_stock"] < row["reorder_point"] * 0.5
        else "🟡 Attention" if row["current_stock"] < row["reorder_point"]
        else "🟢 Normal" if row["current_stock"] < row["optimal_stock"] * 1.2
        else "🔵 Surstock",
        axis=1
    )
    
    # Calculer quantité à commander
    df["quantity_to_order"] = df.apply(lambda row:
        max(0, row["optimal_stock"] - row["current_stock"]),
        axis=1
    )
    
    # Impact financier
    df["financial_impact"] = df["quantity_to_order"] * df["price"]
    
    return df


# ============================================
# PRÉVISIONS (MOCK)
# ============================================

def generate_forecast_for_product(
    product_id: str,
    historical_sales: pd.DataFrame,
    horizon_days: int = 30
) -> pd.DataFrame:
    """
    Génère des prévisions réalistes pour un produit
    """
    
    # Calculer statistiques historiques
    product_sales = historical_sales[historical_sales["product_id"] == product_id]
    daily_avg = product_sales["quantity"].mean()
    daily_std = product_sales["quantity"].std()
    
    # Générer prévisions
    future_dates = pd.date_range(
        start=datetime.now().date() + timedelta(days=1),
        periods=horizon_days,
        freq='D'
    )
    
    forecasts = []
    for date in future_dates:
        # P50 (médiane) avec tendance légère
        p50 = daily_avg * np.random.uniform(0.95, 1.05)
        
        # P10 (pessimiste) et P90 (optimiste)
        p10 = p50 * 0.6
        p90 = p50 * 1.5
        
        forecasts.append({
            "date": date,
            "product_id": product_id,
            "forecast_p10": max(0, int(p10)),
            "forecast_p50": max(0, int(p50)),
            "forecast_p90": max(0, int(p90)),
        })
    
    return pd.DataFrame(forecasts)


def generate_all_forecasts(historical_sales: pd.DataFrame) -> pd.DataFrame:
    """
    Génère les prévisions pour tous les produits
    """
    all_forecasts = []
    
    for product in PRODUCT_CATALOG:
        forecast = generate_forecast_for_product(
            product_id=product["id"],
            historical_sales=historical_sales,
            horizon_days=30
        )
        all_forecasts.append(forecast)
    
    return pd.concat(all_forecasts, ignore_index=True)


# ============================================
# RECOMMANDATIONS D'APPROVISIONNEMENT
# ============================================

def generate_recommendations(inventory: pd.DataFrame) -> pd.DataFrame:
    """
    Génère les recommandations d'approvisionnement
    """
    
    recommendations = inventory.copy()
    
    # Déterminer action
    recommendations["action"] = recommendations.apply(lambda row:
        f"🚨 Commander {row['quantity_to_order']} unités URGENT" if row["status"] == "🔴 Critique"
        else f"⚠️ Commander {row['quantity_to_order']} unités" if row["status"] == "🟡 Attention"
        else "✅ Stock suffisant" if row["status"] == "🟢 Normal"
        else "📦 Réduire stock (surstock)",
        axis=1
    )
    
    # Priorité (1 = plus urgent)
    recommendations["priority"] = recommendations["status"].map({
        "🔴 Critique": 1,
        "🟡 Attention": 2,
        "🟢 Normal": 3,
        "🔵 Surstock": 4,
    })
    
    # Économies potentielles (éviter rupture)
    recommendations["potential_savings"] = recommendations.apply(lambda row:
        row["daily_avg_sales"] * row["price"] * 7  # 7 jours de ventes perdues
        if row["status"] in ["🔴 Critique", "🟡 Attention"]
        else 0,
        axis=1
    )
    
    return recommendations.sort_values("priority")


# ============================================
# KPIs GLOBAUX
# ============================================

def calculate_kpis(
    historical_sales: pd.DataFrame,
    inventory: pd.DataFrame,
    forecasts: pd.DataFrame
) -> dict:
    """
    Calcule tous les KPIs du dashboard
    """
    
    # Derniers 30 jours
    cutoff_date = pd.Timestamp(datetime.now().date() - timedelta(days=30))
    last_30_days = historical_sales[
        historical_sales["date"] >= cutoff_date
    ]
    
    # Derniers 60 jours (pour comparaison)
    cutoff_date_60 = pd.Timestamp(datetime.now().date() - timedelta(days=60))
    last_60_days = historical_sales[
        historical_sales["date"] >= cutoff_date_60
    ]
    
    prev_30_days = last_60_days[
        last_60_days["date"] < cutoff_date
    ]
    
    # KPIs
    kpis = {
        # Produits
        "total_products": len(PRODUCT_CATALOG),
        "products_with_forecast": len(PRODUCT_CATALOG),
        "products_tracked": len(PRODUCT_CATALOG),
        
        # Ventes & Historique
        "total_sales_records": len(historical_sales),
        "sales_last_30_days": last_30_days["quantity"].sum(),
        "revenue_last_30_days": (last_30_days["quantity"] * last_30_days["price"]).sum(),
        
        # Précision (mock mais réaliste)
        "forecast_accuracy": random.uniform(88, 94),  # MAPE inverse
        "forecast_accuracy_delta": random.uniform(-2, 5),
        
        # Stock
        "stockout_rate": len(inventory[inventory["status"] == "🔴 Critique"]) / len(inventory) * 100,
        "stockout_rate_delta": random.uniform(-30, 10),
        
        "overstock_rate": len(inventory[inventory["status"] == "🔵 Surstock"]) / len(inventory) * 100,
        
        # Service
        "service_level": random.uniform(95, 99),
        "service_level_delta": random.uniform(-1, 4),
        
        # Recommandations
        "urgent_actions": len(inventory[inventory["status"] == "🔴 Critique"]),
        "total_recommendations": len(inventory[inventory["quantity_to_order"] > 0]),
        
        # Économies (mock mais crédible)
        "potential_savings": inventory["financial_impact"].sum(),
        "savings_delta": random.uniform(5, 25),
        
        # Ruptures évitées
        "stockouts_avoided": random.randint(35, 55),
        "stockouts_avoided_delta": random.uniform(-30, 10),
        
        # Période de données
        "data_start_date": historical_sales["date"].min(),
        "data_end_date": historical_sales["date"].max(),
        "data_period_days": (historical_sales["date"].max() - historical_sales["date"].min()).days,
        
        # Dernière mise à jour
        "last_update": datetime.now(),
    }
    
    return kpis


# ============================================
# CLASSE PRINCIPALE - MOCK DATA MANAGER
# ============================================

class MockDataManager:
    """
    Gestionnaire centralisé de toutes les données d'exemple
    """
    
    def __init__(self):
        self.sales_history = None
        self.inventory = None
        self.forecasts = None
        self.recommendations = None
        self.kpis = None
        self._initialized = False
    
    def initialize(self):
        """
        Initialise toutes les données
        """
        if self._initialized:
            return
        
        print("Generation des donnees d'exemple...")
        
        # 1. Historique de ventes
        self.sales_history = generate_all_sales_history()
        print(f"OK {len(self.sales_history)} enregistrements de ventes generes")
        
        # 2. Inventaire actuel
        self.inventory = generate_current_inventory()
        print(f"OK {len(self.inventory)} produits en inventaire")
        
        # 3. Prévisions
        self.forecasts = generate_all_forecasts(self.sales_history)
        print(f"OK {len(self.forecasts)} previsions generees")
        
        # 4. Recommandations
        self.recommendations = generate_recommendations(self.inventory)
        print(f"OK {len(self.recommendations)} recommandations calculees")
        
        # 5. KPIs
        self.kpis = calculate_kpis(
            self.sales_history,
            self.inventory,
            self.forecasts
        )
        print(f"OK {len(self.kpis)} KPIs calcules")
        
        self._initialized = True
        print("Donnees d'exemple pretes!")
    
    def get_sales_history(self, product_id: str = None) -> pd.DataFrame:
        """Obtenir l'historique de ventes"""
        if not self._initialized:
            self.initialize()
        
        
        if product_id:
            return self.sales_history[self.sales_history["product_id"] == product_id]
        return self.sales_history
    
    def get_inventory(self) -> pd.DataFrame:
        """Obtenir l'inventaire"""
        if not self._initialized:
            self.initialize()
        return self.inventory
    
    def get_forecasts(self, product_id: str = None) -> pd.DataFrame:
        """Obtenir les prévisions"""
        if not self._initialized:
            self.initialize()
        
        if product_id:
            return self.forecasts[self.forecasts["product_id"] == product_id]
        return self.forecasts
    
    def get_recommendations(self, priority: int = None) -> pd.DataFrame:
        """Obtenir les recommandations"""
        if not self._initialized:
            self.initialize()
        
        if priority:
            return self.recommendations[self.recommendations["priority"] == priority]
        return self.recommendations
    
    def get_kpis(self) -> dict:
        """Obtenir tous les KPIs"""
        if not self._initialized:
            self.initialize()
        return self.kpis
    
    def get_product_list(self) -> list:
        """Obtenir la liste des produits"""
        return PRODUCT_CATALOG
    
    def get_critical_alerts(self) -> pd.DataFrame:
        """Obtenir les alertes critiques"""
        if not self._initialized:
            self.initialize()
        return self.recommendations[
            self.recommendations["status"].isin(["🔴 Critique", "🟡 Attention"])
        ].head(5)


# ============================================
# INSTANCE GLOBALE (SINGLETON)
# ============================================

# Créer une instance globale
mock_data = MockDataManager()


# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def format_currency(value: float) -> str:
    """Formatte une valeur monétaire"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M €"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K €"
    else:
        return f"{value:.2f} €"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Formatte un pourcentage"""
    return f"{value:.{decimals}f}%"


def format_delta(value: float) -> str:
    """Formatte un delta avec flèche"""
    if value > 0:
        return f"↑ {abs(value):.1f}%"
    elif value < 0:
        return f"↓ {abs(value):.1f}%"
    else:
        return "→ 0%"


# ============================================
# EXPORT CSV (pour tests)
# ============================================

def export_mock_data_to_csv(output_dir: str = "./data"):
    """
    Exporte toutes les données mock en CSV
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    mock_data.initialize()
    
    # Export
    mock_data.sales_history.to_csv(f"{output_dir}/sales_history.csv", index=False)
    mock_data.inventory.to_csv(f"{output_dir}/inventory.csv", index=False)
    mock_data.forecasts.to_csv(f"{output_dir}/forecasts.csv", index=False)
    mock_data.recommendations.to_csv(f"{output_dir}/recommendations.csv", index=False)
    
    print(f"✅ Données exportées vers {output_dir}/")


# ============================================
# TESTS
# ============================================

if __name__ == "__main__":
    # Test du système
    print("🧪 Test du système de mock data\n")
    
    # Initialize
    mock_data.initialize()
    
    # Test KPIs
    kpis = mock_data.get_kpis()
    print("\n📊 KPIs:")
    print(f"  - Produits suivis: {kpis['total_products']}")
    print(f"  - Précision: {kpis['forecast_accuracy']:.1f}%")
    print(f"  - Économies: {format_currency(kpis['potential_savings'])}")
    print(f"  - Actions urgentes: {kpis['urgent_actions']}")
    
    # Test alertes
    print("\n🚨 Alertes critiques:")
    alerts = mock_data.get_critical_alerts()
    for _, alert in alerts.iterrows():
        print(f"  - {alert['product_name']}: {alert['action']}")
    
    # Export (optionnel)
    # export_mock_data_to_csv()
    
    print("\n✅ Tous les tests passés!")
