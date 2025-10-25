#!/usr/bin/env python3
"""
Stokkel - Script de Vérification de l'Installation
===================================================
Vérifie que toutes les dépendances et fichiers sont correctement installés.

Usage:
    python check_installation.py
"""

import sys
import os
from pathlib import Path

# Couleurs pour la sortie
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Affiche un en-tête."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def check_mark(success):
    """Retourne une marque de succès ou d'échec."""
    if success:
        return f"{Colors.GREEN}✓{Colors.END}"
    else:
        return f"{Colors.RED}✗{Colors.END}"

def check_python_version():
    """Vérifie la version de Python."""
    print_header("Vérification de Python")
    
    version = sys.version_info
    print(f"Version Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print(f"{check_mark(True)} Python 3.10+ détecté")
        return True
    else:
        print(f"{check_mark(False)} Python 3.10+ requis (version actuelle: {version.major}.{version.minor})")
        return False

def check_dependencies():
    """Vérifie les dépendances Python."""
    print_header("Vérification des Dépendances")
    
    dependencies = {
        'fastapi': 'FastAPI (API)',
        'uvicorn': 'Uvicorn (Serveur)',
        'prophet': 'Prophet (IA Prévisions)',
        'pandas': 'Pandas (Data)',
        'numpy': 'NumPy (Calculs)',
        'streamlit': 'Streamlit (Dashboard)',
        'plotly': 'Plotly (Graphiques)',
        'pydantic': 'Pydantic (Validation)',
    }
    
    all_ok = True
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"{check_mark(True)} {description}")
        except ImportError:
            print(f"{check_mark(False)} {description} - MANQUANT")
            all_ok = False
    
    if not all_ok:
        print(f"\n{Colors.YELLOW}⚠ Installation requise:{Colors.END}")
        print(f"  pip install -r requirements.txt --break-system-packages")
    
    return all_ok

def check_file_structure():
    """Vérifie la structure des fichiers."""
    print_header("Vérification de la Structure")
    
    required_files = [
        'app/main.py',
        'app/forecasting.py',
        'app/optimization.py',
        'app/data_utils.py',
        'app/schemas.py',
        'app/__init__.py',
        'dashboard/app.py',
        'dashboard/components/styles.py',
        'dashboard/components/session.py',
        'dashboard/components/api_client.py',
        'dashboard/pages/home.py',
        'dashboard/pages/data_management.py',
        'dashboard/pages/forecasting.py',
        'dashboard/pages/recommendations.py',
        'data/sample_sales.csv',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
    ]
    
    all_ok = True
    for filepath in required_files:
        exists = Path(filepath).exists()
        status = check_mark(exists)
        print(f"{status} {filepath}")
        if not exists:
            all_ok = False
    
    return all_ok

def check_data_files():
    """Vérifie les fichiers de données."""
    print_header("Vérification des Données")
    
    data_file = Path('data/sample_sales.csv')
    
    if not data_file.exists():
        print(f"{check_mark(False)} Fichier sample_sales.csv manquant")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv(data_file)
        
        # Normaliser les colonnes si nécessaire
        column_mapping = {
            'reference_article': 'product_id',
            'date_vente': 'date', 
            'quantite_vendue': 'quantity'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns and new_name not in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        required_cols = ['product_id', 'date', 'quantity']
        has_cols = all(col in df.columns for col in required_cols)
        
        print(f"{check_mark(has_cols)} Colonnes requises présentes")
        print(f"  - Lignes: {len(df)}")
        print(f"  - Produits: {df['product_id'].nunique()}")
        print(f"  - Période: {df['date'].min()} à {df['date'].max()}")
        
        return has_cols
    except Exception as e:
        print(f"{check_mark(False)} Erreur lecture CSV: {str(e)}")
        return False

def test_api_imports():
    """Test les imports de l'API."""
    print_header("Test des Imports API")
    
    all_ok = True
    
    try:
        from app import forecasting
        print(f"{check_mark(True)} forecasting.py")
    except Exception as e:
        print(f"{check_mark(False)} forecasting.py - {str(e)}")
        all_ok = False
    
    try:
        from app import optimization
        print(f"{check_mark(True)} optimization.py")
    except Exception as e:
        print(f"{check_mark(False)} optimization.py - {str(e)}")
        all_ok = False
    
    try:
        from app import data_utils
        print(f"{check_mark(True)} data_utils.py")
    except Exception as e:
        print(f"{check_mark(False)} data_utils.py - {str(e)}")
        all_ok = False
    
    try:
        from app import schemas
        print(f"{check_mark(True)} schemas.py")
    except Exception as e:
        print(f"{check_mark(False)} schemas.py - {str(e)}")
        all_ok = False
    
    return all_ok

def test_forecast_engine():
    """Test rapide du moteur de prévision."""
    print_header("Test du Moteur de Prévision")
    
    try:
        from app.forecasting import ForecastEngine
        from app.data_utils import generate_sample_data
        import pandas as pd
        
        # Générer données de test
        print("  📊 Génération de données de test...")
        df = generate_sample_data(num_products=1, num_days=90)
        
        # Créer le moteur
        engine = ForecastEngine()
        
        # Tester la prévision
        print("  🔮 Test de prévision...")
        # Préparer les données pour Prophet
        from app.data_utils import prepare_forecast_data
        prepared_data = prepare_forecast_data(df, 'PROD_001')
        # Générer la prévision
        forecast_points, metadata = engine.generate_forecast(
            product_id='PROD_001',
            historical_data=prepared_data,
            horizon_days=7
        )
        
        # Vérifier le résultat
        has_forecast = isinstance(forecast_points, list) and len(forecast_points) > 0
        has_p50 = len(forecast_points) > 0 and hasattr(forecast_points[0], 'p50')
        correct_length = len(forecast_points) == 7 if has_forecast else False
        
        print(f"{check_mark(has_forecast)} Prévision générée")
        print(f"{check_mark(has_p50 and correct_length)} Format correct (7 jours)")
        
        if has_forecast and has_p50:
            avg_p50 = sum(point.p50 for point in forecast_points) / len(forecast_points)
            uncertainty = sum((point.p90 - point.p10) / point.p50 for point in forecast_points) / len(forecast_points) * 100
            print(f"  - Demande P50 moyenne: {avg_p50:.1f} unités/jour")
            print(f"  - Incertitude: {uncertainty:.1f}%")
        
        return has_forecast and has_p50
        
    except Exception as e:
        print(f"{check_mark(False)} Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_optimization_engine():
    """Test rapide du moteur d'optimisation."""
    print_header("Test du Moteur d'Optimisation")
    
    try:
        from app.optimization import StockOptimizer
        import pandas as pd
        
        # Créer des données de prévision simulées
        forecast_df = pd.DataFrame({
            'date': pd.date_range('2025-01-01', periods=30, freq='D').strftime('%Y-%m-%d'),
            'p10': [90 + i for i in range(30)],
            'p50': [100 + i for i in range(30)],
            'p90': [110 + i for i in range(30)]
        })
        
        # Tester l'optimisation
        print("  📦 Test d'optimisation...")
        optimizer = StockOptimizer()
        rec = optimizer.generate_recommendation(
            product_id="PROD_001",
            forecast_data=forecast_df,
            current_stock=500,
            lead_time_days=7,
            service_level_percent=95
        )
        
        # Vérifier le résultat
        has_rec = hasattr(rec, 'recommendation_action')
        has_qty = hasattr(rec, 'quantity_to_order')
        has_metrics = hasattr(rec, 'metadata')
        
        print(f"{check_mark(has_rec)} Recommandation générée")
        print(f"{check_mark(has_qty)} Quantité calculée")
        print(f"{check_mark(has_metrics)} Métriques présentes")
        
        if all([has_rec, has_qty, has_metrics]):
            print(f"  - Action: {rec.recommendation_action}")
            print(f"  - Point de commande: {rec.reorder_point} unités")
            print(f"  - Stock de sécurité: {rec.dynamic_safety_stock} unités")
        
        return has_rec and has_qty and has_metrics
        
    except Exception as e:
        print(f"{check_mark(False)} Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def print_summary(results):
    """Affiche le résumé final."""
    print_header("Résumé de la Vérification")
    
    total = len(results)
    passed = sum(results.values())
    
    for test_name, success in results.items():
        status = check_mark(success)
        print(f"{status} {test_name}")
    
    print(f"\n{Colors.BOLD}Score: {passed}/{total}{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ TOUT EST PRÊT !{Colors.END}")
        print(f"\n{Colors.BOLD}Prochaines étapes:{Colors.END}")
        print(f"  1. Lancer l'API:      uvicorn app.main:app --reload")
        print(f"  2. Lancer le Dashboard: streamlit run dashboard/app.py")
        print(f"  3. Ouvrir: http://localhost:8501")
    else:
        print(f"\n{Colors.YELLOW}⚠ Certaines vérifications ont échoué{Colors.END}")
        print(f"Veuillez corriger les erreurs ci-dessus avant de continuer.")
        print(f"\n{Colors.BOLD}Aide:{Colors.END}")
        print(f"  - Installer les dépendances: pip install -r requirements.txt")
        print(f"  - Vérifier la structure des fichiers")
        print(f"  - Consulter README.md pour plus d'aide")

def main():
    """Fonction principale."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("   _____ _        _    _        _ ")
    print("  / ____| |      | |  | |      | |")
    print(" | (___ | |_ ___ | | _| | _____| |")
    print("  \\___ \\| __/ _ \\| |/ / |/ / _ \\ |")
    print("  ____) | || (_) |   <|   <  __/ |")
    print(" |_____/ \\__\\___/|_|\\_\\_|\\_\\___|_|")
    print(f"{Colors.END}")
    print(f"{Colors.BOLD}Vérification de l'Installation{Colors.END}\n")
    
    results = {}
    
    # Exécuter les vérifications
    results["Python 3.10+"] = check_python_version()
    results["Dépendances"] = check_dependencies()
    results["Structure Fichiers"] = check_file_structure()
    results["Fichiers Données"] = check_data_files()
    results["Imports API"] = test_api_imports()
    results["Moteur Prévision"] = test_forecast_engine()
    results["Moteur Optimisation"] = test_optimization_engine()
    
    # Résumé
    print_summary(results)
    
    # Code de sortie
    sys.exit(0 if all(results.values()) else 1)

if __name__ == "__main__":
    main()