"""
app/data_utils.py
Utilitaires pour validation et traitement des données
"""

import pandas as pd
from typing import Tuple, List, Dict
import numpy as np

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise les colonnes du DataFrame pour correspondre au format attendu
    """
    df_copy = df.copy()
    
    # Mapping des colonnes alternatives
    column_mapping = {
        'reference_article': 'product_id',
        'date_vente': 'date',
        'quantite_vendue': 'quantity',
        'sales_qty': 'quantity'
    }
    
    # Renommer les colonnes si nécessaire
    for old_name, new_name in column_mapping.items():
        if old_name in df_copy.columns and new_name not in df_copy.columns:
            df_copy = df_copy.rename(columns={old_name: new_name})
    
    return df_copy

def validate_sales_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valide le format du CSV de ventes
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    # Normalisation des colonnes
    df_normalized = normalize_columns(df)
    
    # Vérifier colonnes requises après normalisation
    required_cols = ['product_id', 'date', 'quantity']
    missing_cols = [col for col in required_cols if col not in df_normalized.columns]
    
    if missing_cols:
        errors.append(f"Colonnes manquantes: {', '.join(missing_cols)}")
        return False, errors
    
    # Vérifier types
    try:
        df_normalized['date'] = pd.to_datetime(df_normalized['date'])
    except Exception as e:
        errors.append(f"Erreur format date: {str(e)}")
    
    try:
        df_normalized['quantity'] = pd.to_numeric(df_normalized['quantity'])
    except Exception as e:
        errors.append(f"Erreur format quantity: {str(e)}")
    
    # Vérifier valeurs négatives
    if (df_normalized['quantity'] < 0).any():
        errors.append("Quantités négatives détectées")
    
    if errors:
        return False, errors
    
    return True, []


def prepare_forecast_data(df: pd.DataFrame, product_id: str) -> pd.DataFrame:
    """
    Prépare les données pour le forecasting
    
    Returns:
        DataFrame avec colonnes ds (date) et y (quantity)
    """
    # Normaliser les colonnes d'abord
    df_normalized = normalize_columns(df)
    product_data = df_normalized[df_normalized['product_id'] == product_id].copy()
    
    if len(product_data) < 14:
        raise ValueError(f"Données insuffisantes: {len(product_data)} jours (minimum: 14)")
    
    # Agrégation par date
    product_data = product_data.groupby('date')['quantity'].sum().reset_index()
    product_data.columns = ['ds', 'y']
    product_data['ds'] = pd.to_datetime(product_data['ds'])
    
    return product_data.sort_values('ds')


def load_sales_data(file_path: str) -> pd.DataFrame:
    """
    Charge les données de ventes depuis un fichier CSV
    
    Returns:
        DataFrame avec colonnes product_id, date, quantity
    """
    try:
        df = pd.read_csv(file_path)
        
        # Normalisation des colonnes
        if 'sales_qty' in df.columns:
            df['quantity'] = df['sales_qty']
        elif 'qty' in df.columns:
            df['quantity'] = df['qty']
        
        # Validation
        is_valid, errors = validate_sales_data(df)
        if not is_valid:
            raise ValueError(f"Données invalides: {'; '.join(errors)}")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement: {str(e)}")


def get_product_list(df: pd.DataFrame) -> List[str]:
    """
    Retourne la liste des produits uniques
    
    Returns:
        Liste des product_id
    """
    return df['product_id'].unique().tolist()


def get_date_range(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Retourne la plage de dates des données
    
    Returns:
        (date_min, date_max) au format string
    """
    date_min = df['date'].min().strftime('%Y-%m-%d')
    date_max = df['date'].max().strftime('%Y-%m-%d')
    return date_min, date_max


def get_data_statistics(df: pd.DataFrame) -> Dict:
    """
    Calcule les statistiques des données
    
    Returns:
        Dictionnaire avec statistiques
    """
    return {
        'num_products': df['product_id'].nunique(),
        'total_records': len(df),
        'date_range': (df['date'].min(), df['date'].max()),
        'total_quantity': df['quantity'].sum(),
        'avg_daily_sales': df.groupby('date')['quantity'].sum().mean()
    }


def detect_seasonality(df: pd.DataFrame, product_id: str) -> Dict:
    """
    Détecte la saisonnalité et la tendance d'un produit
    
    Returns:
        Dictionnaire avec métriques de saisonnalité
    """
    product_data = df[df['product_id'] == product_id].copy()
    
    if len(product_data) < 14:
        return {'trend': 'insufficient_data', 'coefficient_of_variation': 0}
    
    # Calcul du coefficient de variation
    daily_sales = product_data.groupby('date')['quantity'].sum()
    cv = daily_sales.std() / daily_sales.mean() if daily_sales.mean() > 0 else 0
    
    # Détection de tendance simple
    if len(daily_sales) >= 7:
        recent_avg = daily_sales.tail(7).mean()
        older_avg = daily_sales.head(7).mean()
        trend = 'increasing' if recent_avg > older_avg * 1.1 else 'decreasing' if recent_avg < older_avg * 0.9 else 'stable'
    else:
        trend = 'insufficient_data'
    
    return {
        'trend': trend,
        'coefficient_of_variation': cv,
        'daily_avg': daily_sales.mean(),
        'daily_std': daily_sales.std()
    }


def generate_sample_data(num_products: int = 2, num_days: int = 30) -> pd.DataFrame:
    """
    Génère des données synthétiques pour les tests
    
    Args:
        num_products: Nombre de produits à générer
        num_days: Nombre de jours de données
    
    Returns:
        DataFrame avec colonnes product_id, date, quantity
    """
    np.random.seed(42)  # Pour la reproductibilité
    
    data = []
    dates = pd.date_range('2024-01-01', periods=num_days, freq='D')
    
    for i in range(num_products):
        product_id = f'PROD_{i+1:03d}'
        
        # Génération de données avec tendance et saisonnalité
        base_demand = 50 + i * 10
        trend = np.linspace(0, 5, num_days)
        seasonality = 10 * np.sin(np.arange(num_days) * 2 * np.pi / 7)
        noise = np.random.normal(0, 5, num_days)
        
        quantities = base_demand + trend + seasonality + noise
        quantities = np.maximum(0, quantities)  # Pas de quantités négatives
        
        for j, date in enumerate(dates):
            data.append({
                'product_id': product_id,
                'date': date.strftime('%Y-%m-%d'),
                'quantity': int(quantities[j])
            })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Test des fonctions
    print("🧪 Test des utilitaires de données...")
    
    # Créer des données de test
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    df = pd.DataFrame({
        'product_id': ['PROD_001'] * 30,
        'date': dates,
        'quantity': np.random.poisson(50, 30)
    })
    
    print("\n🧪 Test de validate_sales_data...")
    is_valid, errors = validate_sales_data(df)
    print(f"✅ Validation: {is_valid}, Erreurs: {len(errors)}")
    
    print("\n🧪 Test de prepare_forecast_data...")
    prepared = prepare_forecast_data(df, 'PROD_001')
    print(f"✅ {len(prepared)} lignes préparées, Colonnes: {prepared.columns.tolist()}")
    
    print("\n🧪 Test de get_data_statistics...")
    stats = get_data_statistics(df)
    print(f"✅ Statistiques: {stats['num_products']} produits, {stats['total_records']} records")
    
    print("\n🧪 Test de detect_seasonality...")
    seasonality = detect_seasonality(df, 'PROD_001')
    print(f"✅ Tendance: {seasonality['trend']}, CV: {seasonality['coefficient_of_variation']:.2f}")
    
    print("\n✅ Tous les tests passés!")