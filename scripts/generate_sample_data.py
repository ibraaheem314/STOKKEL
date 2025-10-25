#!/usr/bin/env python3
"""
Stokkel - Générateur de Données d'Exemple
Crée des données synthétiques réalistes pour démonstrations et tests
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
from pathlib import Path


class SampleDataGenerator:
    """Générateur de données de ventes synthétiques"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.seed = seed
    
    def generate_product_sales(
        self, 
        product_id: str,
        start_date: str = '2024-01-01',
        num_days: int = 90,
        base_demand: float = 50.0,
        trend_slope: float = 0.1,
        seasonality_amplitude: float = 10.0,
        noise_std: float = 5.0,
        growth_rate: float = 0.0
    ) -> pd.DataFrame:
        """
        Génère des données de ventes pour un produit avec tendance et saisonnalité.
        
        Args:
            product_id: Identifiant du produit
            start_date: Date de début
            num_days: Nombre de jours de données
            base_demand: Demande de base quotidienne
            trend_slope: Pente de la tendance (croissance/jour)
            seasonality_amplitude: Amplitude de la saisonnalité hebdomadaire
            noise_std: Écart-type du bruit aléatoire
            growth_rate: Taux de croissance exponentielle (0 = linéaire)
        
        Returns:
            DataFrame avec colonnes product_id, date, quantity
        """
        dates = pd.date_range(start_date, periods=num_days, freq='D')
        
        # Tendance (linéaire ou exponentielle)
        if growth_rate > 0:
            trend = base_demand * np.exp(growth_rate * np.arange(num_days) / 365)
        else:
            trend = base_demand + trend_slope * np.arange(num_days)
        
        # Saisonnalité hebdomadaire (pics le week-end)
        weekly_pattern = seasonality_amplitude * np.sin(np.arange(num_days) * 2 * np.pi / 7)
        
        # Saisonnalité mensuelle (légère)
        monthly_pattern = seasonality_amplitude * 0.3 * np.sin(np.arange(num_days) * 2 * np.pi / 30)
        
        # Bruit aléatoire
        noise = np.random.normal(0, noise_std, num_days)
        
        # Combinaison
        quantities = trend + weekly_pattern + monthly_pattern + noise
        quantities = np.maximum(0, quantities)  # Pas de valeurs négatives
        
        return pd.DataFrame({
            'product_id': product_id,
            'date': dates,
            'quantity': quantities.round(2)
        })
    
    def generate_retail_scenario(self, output_path: str = 'data/sample_sales.csv'):
        """
        Génère un scénario complet de commerce de détail avec plusieurs produits.
        """
        print("🏪 Génération de données pour commerce de détail...\n")
        
        products_config = [
            {
                'id': 'PROD_001_RIZ',
                'name': 'Riz Local 5kg',
                'base_demand': 80,
                'trend_slope': 0.2,
                'seasonality_amplitude': 15,
                'noise_std': 8,
                'growth_rate': 0.05
            },
            {
                'id': 'PROD_002_HUILE',
                'name': 'Huile Végétale 1L',
                'base_demand': 60,
                'trend_slope': 0.15,
                'seasonality_amplitude': 12,
                'noise_std': 6,
                'growth_rate': 0.03
            },
            {
                'id': 'PROD_003_SUCRE',
                'name': 'Sucre 1kg',
                'base_demand': 45,
                'trend_slope': 0.1,
                'seasonality_amplitude': 8,
                'noise_std': 5,
                'growth_rate': 0.02
            },
            {
                'id': 'PROD_004_LAIT',
                'name': 'Lait en Poudre 500g',
                'base_demand': 35,
                'trend_slope': 0.05,
                'seasonality_amplitude': 6,
                'noise_std': 4,
                'growth_rate': 0.01
            },
            {
                'id': 'PROD_005_FARINE',
                'name': 'Farine de Blé 1kg',
                'base_demand': 55,
                'trend_slope': 0.08,
                'seasonality_amplitude': 10,
                'noise_std': 7,
                'growth_rate': 0.025
            }
        ]
        
        all_data = []
        
        for config in products_config:
            print(f"  ✓ Génération: {config['name']} ({config['id']})")
            
            df = self.generate_product_sales(
                product_id=config['id'],
                base_demand=config['base_demand'],
                trend_slope=config['trend_slope'],
                seasonality_amplitude=config['seasonality_amplitude'],
                noise_std=config['noise_std'],
                growth_rate=config['growth_rate']
            )
            
            all_data.append(df)
        
        # Combinaison de tous les produits
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Sauvegarde
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(output_path, index=False)
        
        print(f"\n✅ Données générées avec succès!")
        print(f"📁 Fichier: {output_path}")
        print(f"📊 Statistiques:")
        print(f"   • Produits: {len(products_config)}")
        print(f"   • Jours: 90")
        print(f"   • Total enregistrements: {len(final_df)}")
        print(f"   • Ventes totales: {final_df['quantity'].sum():.0f} unités")
        
        return final_df
    
    def generate_pharmacy_scenario(self, output_path: str = 'data/pharmacy_sales.csv'):
        """
        Génère des données pour une pharmacie.
        """
        print("💊 Génération de données pour pharmacie...\n")
        
        products_config = [
            {
                'id': 'MED_001_PARACETAMOL',
                'name': 'Paracétamol 500mg',
                'base_demand': 120,
                'trend_slope': 0.3,
                'seasonality_amplitude': 25,
                'noise_std': 15,
                'growth_rate': 0.04
            },
            {
                'id': 'MED_002_ANTIBIO',
                'name': 'Antibiotique Amoxicilline',
                'base_demand': 40,
                'trend_slope': 0.1,
                'seasonality_amplitude': 8,
                'noise_std': 6,
                'growth_rate': 0.02
            },
            {
                'id': 'MED_003_VITAMINE',
                'name': 'Complément Vitamine C',
                'base_demand': 30,
                'trend_slope': 0.15,
                'seasonality_amplitude': 5,
                'noise_std': 4,
                'growth_rate': 0.06
            }
        ]
        
        all_data = []
        
        for config in products_config:
            print(f"  ✓ Génération: {config['name']} ({config['id']})")
            
            df = self.generate_product_sales(
                product_id=config['id'],
                base_demand=config['base_demand'],
                trend_slope=config['trend_slope'],
                seasonality_amplitude=config['seasonality_amplitude'],
                noise_std=config['noise_std'],
                growth_rate=config['growth_rate']
            )
            
            all_data.append(df)
        
        final_df = pd.concat(all_data, ignore_index=True)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(output_path, index=False)
        
        print(f"\n✅ Données pharmacie générées!")
        print(f"📁 Fichier: {output_path}")
        
        return final_df
    
    def generate_restaurant_scenario(self, output_path: str = 'data/restaurant_sales.csv'):
        """
        Génère des données pour un restaurant.
        """
        print("🍽️  Génération de données pour restaurant...\n")
        
        products_config = [
            {
                'id': 'MENU_001_THIEB',
                'name': 'Thiéboudienne',
                'base_demand': 85,
                'trend_slope': 0.25,
                'seasonality_amplitude': 20,
                'noise_std': 12,
                'growth_rate': 0.035
            },
            {
                'id': 'MENU_002_YASSA',
                'name': 'Poulet Yassa',
                'base_demand': 70,
                'trend_slope': 0.2,
                'seasonality_amplitude': 15,
                'noise_std': 10,
                'growth_rate': 0.03
            },
            {
                'id': 'MENU_003_MAFE',
                'name': 'Mafé',
                'base_demand': 50,
                'trend_slope': 0.15,
                'seasonality_amplitude': 10,
                'noise_std': 8,
                'growth_rate': 0.025
            }
        ]
        
        all_data = []
        
        for config in products_config:
            print(f"  ✓ Génération: {config['name']} ({config['id']})")
            
            df = self.generate_product_sales(
                product_id=config['id'],
                base_demand=config['base_demand'],
                trend_slope=config['trend_slope'],
                seasonality_amplitude=config['seasonality_amplitude'],
                noise_std=config['noise_std'],
                growth_rate=config['growth_rate']
            )
            
            all_data.append(df)
        
        final_df = pd.concat(all_data, ignore_index=True)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(output_path, index=False)
        
        print(f"\n✅ Données restaurant générées!")
        print(f"📁 Fichier: {output_path}")
        
        return final_df


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description='Générateur de données de ventes synthétiques pour Stokkel'
    )
    
    parser.add_argument(
        '--scenario',
        type=str,
        choices=['retail', 'pharmacy', 'restaurant', 'all'],
        default='retail',
        help='Type de scénario à générer'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Seed aléatoire pour reproductibilité'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("   STOKKEL - Générateur de Données d'Exemple")
    print("="*60 + "\n")
    
    generator = SampleDataGenerator(seed=args.seed)
    
    if args.scenario == 'retail' or args.scenario == 'all':
        generator.generate_retail_scenario()
        print()
    
    if args.scenario == 'pharmacy' or args.scenario == 'all':
        generator.generate_pharmacy_scenario()
        print()
    
    if args.scenario == 'restaurant' or args.scenario == 'all':
        generator.generate_restaurant_scenario()
        print()
    
    print("="*60)
    print("✨ Génération terminée avec succès!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()