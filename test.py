#!/usr/bin/env python3
"""
Stokkel - Tests Automatisés CORRIGÉS
✅ CORRECTION 2: Imports propres, cohérence 100%
"""

import sys
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
import io

# ===============================
# ✅ CORRECTION 2: Imports corrects sans sys.path.insert
# ===============================

from app.forecast_engine import SalesForecaster, StockOptimizer
from app.data_utils import validate_sales_data, prepare_forecast_data, generate_sample_data


class Colors:
    """Couleurs pour l'affichage des résultats"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class TestDataUtils(unittest.TestCase):
    """✅ NOUVEAU: Tests des utilitaires de données"""
    
    @classmethod
    def setUpClass(cls):
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}   TEST 0: Utilitaires de Données{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
    
    def test_01_generate_sample_data(self):
        """Test de génération de données synthétiques"""
        print(f"  {Colors.YELLOW}→ Test génération données...{Colors.ENDC}")
        
        df = generate_sample_data(num_products=2, num_days=30)
        
        self.assertEqual(len(df), 60)  # 2 produits × 30 jours
        self.assertIn('product_id', df.columns)
        self.assertIn('date', df.columns)
        self.assertIn('quantity', df.columns)
        
        print(f"  {Colors.GREEN}✓ {len(df)} lignes générées{Colors.ENDC}")
    
    def test_02_validate_sales_data_valid(self):
        """Test validation données valides"""
        print(f"  {Colors.YELLOW}→ Test validation données valides...{Colors.ENDC}")
        
        df = generate_sample_data(num_products=1, num_days=20)
        is_valid, errors = validate_sales_data(df)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        print(f"  {Colors.GREEN}✓ Données valides détectées{Colors.ENDC}")
    
    def test_03_validate_sales_data_invalid(self):
        """Test validation données invalides"""
        print(f"  {Colors.YELLOW}→ Test validation données invalides...{Colors.ENDC}")
        
        # DataFrame avec colonne manquante
        df = pd.DataFrame({
            'product_id': ['A', 'B'],
            'date': ['2024-01-01', '2024-01-02']
            # 'quantity' manquant
        })
        
        is_valid, errors = validate_sales_data(df)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        print(f"  {Colors.GREEN}✓ Données invalides détectées ({len(errors)} erreurs){Colors.ENDC}")
    
    def test_04_prepare_forecast_data(self):
        """Test préparation données pour Prophet"""
        print(f"  {Colors.YELLOW}→ Test préparation données forecast...{Colors.ENDC}")
        
        df = generate_sample_data(num_products=1, num_days=30)
        prepared = prepare_forecast_data(df, 'PROD_001')
        
        self.assertIn('ds', prepared.columns)
        self.assertIn('y', prepared.columns)
        self.assertEqual(len(prepared.columns), 2)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(prepared['ds']))
        
        print(f"  {Colors.GREEN}✓ Données préparées: {len(prepared)} jours{Colors.ENDC}")


class TestSalesForecaster(unittest.TestCase):
    """Tests du moteur de prévision"""
    
    @classmethod
    def setUpClass(cls):
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}   TEST 1: Moteur de Prévision IA{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
        
        # Utiliser generate_sample_data au lieu de créer manuellement
        cls.test_data = generate_sample_data(num_products=1, num_days=90)
        cls.test_data['product_id'] = 'TEST_PROD_001'  # Renommer pour le test
        cls.forecaster = SalesForecaster()
    
    def test_01_data_preparation(self):
        """Test de préparation des données"""
        print(f"  {Colors.YELLOW}→ Test préparation données...{Colors.ENDC}")
        
        prepared = self.forecaster.prepare_data(self.test_data, 'TEST_PROD_001')
        
        self.assertIn('ds', prepared.columns)
        self.assertIn('y', prepared.columns)
        self.assertEqual(len(prepared), 90)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(prepared['ds']))
        
        print(f"  {Colors.GREEN}✓ Données préparées correctement{Colors.ENDC}")
    
    def test_02_model_training(self):
        """Test d'entraînement du modèle"""
        print(f"  {Colors.YELLOW}→ Test entraînement Prophet...{Colors.ENDC}")
        
        self.forecaster.train_model(self.test_data, 'TEST_PROD_001')
        
        self.assertIn('TEST_PROD_001', self.forecaster.models)
        self.assertIn('TEST_PROD_001', self.forecaster.trained_products)
        
        print(f"  {Colors.GREEN}✓ Modèle entraîné avec succès{Colors.ENDC}")
    
    def test_03_forecast_generation(self):
        """Test de génération de prévisions"""
        print(f"  {Colors.YELLOW}→ Test génération prévisions P10/P50/P90...{Colors.ENDC}")
        
        forecast = self.forecaster.generate_forecast('TEST_PROD_001', horizon_days=30)
        
        self.assertIn('date', forecast)
        self.assertIn('P10', forecast)
        self.assertIn('P50', forecast)
        self.assertIn('P90', forecast)
        
        self.assertEqual(len(forecast['date']), 30)
        self.assertEqual(len(forecast['P50']), 30)
        
        # Vérifier cohérence P10 < P50 < P90
        for i in range(30):
            self.assertLessEqual(forecast['P10'][i], forecast['P50'][i])
            self.assertLessEqual(forecast['P50'][i], forecast['P90'][i])
        
        print(f"  {Colors.GREEN}✓ Prévisions générées correctement{Colors.ENDC}")
        print(f"    • P50 moyen: {np.mean(forecast['P50']):.2f} unités/jour")
    
    def test_04_uncertainty_calculation(self):
        """Test du calcul d'incertitude"""
        print(f"  {Colors.YELLOW}→ Test calcul incertitude...{Colors.ENDC}")
        
        uncertainty = self.forecaster.calculate_forecast_uncertainty('TEST_PROD_001', lead_time_days=7)
        
        self.assertGreater(uncertainty, 0)
        self.assertLess(uncertainty, 100)
        
        print(f"  {Colors.GREEN}✓ Incertitude: {uncertainty:.2f}{Colors.ENDC}")


class TestStockOptimizer(unittest.TestCase):
    """Tests de l'optimiseur de stocks"""
    
    @classmethod
    def setUpClass(cls):
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}   TEST 2: Optimiseur de Stocks{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
        
        cls.test_data = generate_sample_data(num_products=1, num_days=90)
        cls.test_data['product_id'] = 'TEST_PROD_002'
        
        cls.forecaster = SalesForecaster()
        cls.forecaster.train_model(cls.test_data, 'TEST_PROD_002')
        cls.optimizer = StockOptimizer(cls.forecaster)
    
    def test_01_safety_stock_calculation(self):
        """Test du calcul du stock de sécurité"""
        print(f"  {Colors.YELLOW}→ Test stock de sécurité...{Colors.ENDC}")
        
        safety_stock = self.optimizer.calculate_safety_stock(
            product_id='TEST_PROD_002',
            lead_time_days=7,
            service_level_percent=95.0
        )
        
        self.assertGreater(safety_stock, 0)
        self.assertIsInstance(safety_stock, (int, float))
        
        # Test avec différents niveaux
        ss_90 = self.optimizer.calculate_safety_stock('TEST_PROD_002', 7, 90.0)
        ss_99 = self.optimizer.calculate_safety_stock('TEST_PROD_002', 7, 99.0)
        
        self.assertLess(ss_90, safety_stock)
        self.assertGreater(ss_99, safety_stock)
        
        print(f"  {Colors.GREEN}✓ Stock sécurité: {safety_stock:.2f} unités{Colors.ENDC}")
        print(f"    • 90%: {ss_90:.2f}, 99%: {ss_99:.2f}")
    
    def test_02_reorder_point_calculation(self):
        """Test du calcul du point de commande"""
        print(f"  {Colors.YELLOW}→ Test point de commande...{Colors.ENDC}")
        
        reorder_point, safety_stock = self.optimizer.calculate_reorder_point(
            product_id='TEST_PROD_002',
            lead_time_days=7,
            service_level_percent=95.0
        )
        
        self.assertGreater(reorder_point, 0)
        self.assertGreater(reorder_point, safety_stock)
        
        print(f"  {Colors.GREEN}✓ Point commande: {reorder_point:.2f}{Colors.ENDC}")
        print(f"    • Stock sécurité: {safety_stock:.2f}")
    
    def test_03_recommendation_generation(self):
        """Test de génération de recommandation"""
        print(f"  {Colors.YELLOW}→ Test recommandations...{Colors.ENDC}")
        
        # Scénario 1: Stock suffisant
        rec1 = self.optimizer.generate_recommendation(
            product_id='TEST_PROD_002',
            current_stock=500,
            lead_time_days=7,
            service_level_percent=95.0
        )
        
        self.assertEqual(rec1['recommendation_action'], "Stock suffisant")
        self.assertEqual(rec1['quantity_to_order'], 0)
        
        # Scénario 2: Stock bas
        rec2 = self.optimizer.generate_recommendation(
            product_id='TEST_PROD_002',
            current_stock=50,
            lead_time_days=7,
            service_level_percent=95.0
        )
        
        self.assertEqual(rec2['recommendation_action'], "Commander maintenant")
        self.assertGreater(rec2['quantity_to_order'], 0)
        self.assertIn(rec2['urgency'], ['critical', 'high', 'medium', 'low'])
        
        print(f"  {Colors.GREEN}✓ Recommandations générées{Colors.ENDC}")
        print(f"    • Stock élevé: {rec1['recommendation_action']}")
        print(f"    • Stock bas: {rec2['recommendation_action']} - {rec2['quantity_to_order']:.0f} unités")


class TestAPIIntegration(unittest.TestCase):
    """Tests d'intégration de l'API"""
    
    @classmethod
    def setUpClass(cls):
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}   TEST 3: API Integration{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
        
        cls.api_url = "http://localhost:8000"
        cls.api_available = False
        
        try:
            response = requests.get(f"{cls.api_url}/health", timeout=2)
            if response.status_code == 200:
                cls.api_available = True
                print(f"  {Colors.GREEN}✓ API disponible{Colors.ENDC}")
        except:
            print(f"  {Colors.YELLOW}⚠️  API non disponible - tests ignorés{Colors.ENDC}")
    
    def test_01_health_endpoint(self):
        """Test du endpoint /health"""
        if not self.api_available:
            self.skipTest("API non disponible")
        
        print(f"  {Colors.YELLOW}→ Test /health...{Colors.ENDC}")
        
        response = requests.get(f"{self.api_url}/health")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
        
        print(f"  {Colors.GREEN}✓ Endpoint /health OK{Colors.ENDC}")
    
    def test_02_upload_endpoint(self):
        """Test du endpoint /upload_sales"""
        if not self.api_available:
            self.skipTest("API non disponible")
        
        print(f"  {Colors.YELLOW}→ Test /upload_sales...{Colors.ENDC}")
        
        # Générer CSV de test
        df_test = generate_sample_data(num_products=1, num_days=20)
        csv_buffer = io.StringIO()
        df_test.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        
        files = {'file': ('test.csv', io.StringIO(csv_content), 'text/csv')}
        response = requests.post(f"{self.api_url}/upload_sales", files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['status'], 'success')
        self.assertGreater(len(data.get('trained_products', [])), 0)
        
        print(f"  {Colors.GREEN}✓ Endpoint /upload_sales OK{Colors.ENDC}")
    
    def test_03_forecast_endpoint(self):
        """Test du endpoint /forecast"""
        if not self.api_available:
            self.skipTest("API non disponible")
        
        print(f"  {Colors.YELLOW}→ Test /forecast...{Colors.ENDC}")
        
        # Upload données d'abord
        df_test = generate_sample_data(num_products=1, num_days=30)
        df_test['product_id'] = 'TEST_API_FORECAST'
        csv_buffer = io.StringIO()
        df_test.to_csv(csv_buffer, index=False)
        
        files = {'file': ('test_forecast.csv', io.StringIO(csv_buffer.getvalue()), 'text/csv')}
        requests.post(f"{self.api_url}/upload_sales", files=files)
        
        # Tester forecast
        response = requests.get(f"{self.api_url}/forecast/TEST_API_FORECAST?horizon_days=7")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('forecast', data)
        self.assertIn('P10', data['forecast'])
        self.assertIn('P50', data['forecast'])
        self.assertIn('P90', data['forecast'])
        
        print(f"  {Colors.GREEN}✓ Endpoint /forecast OK{Colors.ENDC}")


def run_tests():
    """Exécute tous les tests"""
    print(f"\n{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}║         STOKKEL - SUITE DE TESTS (VERSION CORRIGÉE)          ║{Colors.ENDC}")
    print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ordre d'exécution
    suite.addTests(loader.loadTestsFromTestCase(TestDataUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestSalesForecaster))
    suite.addTests(loader.loadTestsFromTestCase(TestStockOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}   RÉSUMÉ DES TESTS{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")
    
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success = total - failures - errors
    
    print(f"\n  Tests exécutés:  {total}")
    print(f"  {Colors.GREEN}✓ Réussis:       {success}{Colors.ENDC}")
    
    if failures > 0:
        print(f"  {Colors.RED}✗ Échecs:        {failures}{Colors.ENDC}")
    if errors > 0:
        print(f"  {Colors.RED}✗ Erreurs:       {errors}{Colors.ENDC}")
    
    success_rate = (success / total) * 100 if total > 0 else 0
    print(f"\n  Taux de réussite: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}🎉 TOUS LES TESTS SONT PASSÉS ! 🎉{Colors.ENDC}")
    elif success_rate >= 80:
        print(f"\n  {Colors.YELLOW}{Colors.BOLD}⚠️  Certains tests ont échoué{Colors.ENDC}")
    else:
        print(f"\n  {Colors.RED}{Colors.BOLD}❌ Échec critique des tests{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)