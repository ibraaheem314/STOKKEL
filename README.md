# 🚀 Stokkel - IA pour la Prévision des Ventes et l'Optimisation des Stocks

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **L'IA qui révolutionne la gestion des stocks pour les entreprises africaines**

Stokkel est une solution d'intelligence artificielle complète pour la prévision des ventes et l'optimisation des stocks, spécialement conçue pour les PME africaines. Propulsé par Prophet (Facebook) et doté d'une interface moderne, Stokkel transforme vos données de ventes en insights actionnables.

## ✨ Fonctionnalités Principales

### 🎯 **Prévisions IA Avancées**
- **Modèles Prophet** : Prévisions probabilistes (P10/P50/P90)
- **Détection automatique** de saisonnalité et tendances
- **Intervalles de confiance** pour la prise de décision
- **Horizons flexibles** : 7, 30, 90 jours

### 📊 **Optimisation Intelligente des Stocks**
- **Calcul automatique** du stock de sécurité
- **Points de commande optimaux** basés sur l'IA
- **Recommandations d'approvisionnement** personnalisées
- **Analyse batch** multi-produits

### 🎨 **Interface Moderne**
- **Design startup** avec glassmorphism et animations
- **Dashboard interactif** en temps réel
- **Graphiques Plotly** haute performance
- **Navigation intuitive** et responsive

### 🔧 **Architecture Robuste**
- **API REST** FastAPI haute performance
- **Authentification sécurisée** par token
- **Validation des données** avec Pydantic
- **Documentation automatique** Swagger/ReDoc

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.10+
- pip (gestionnaire de paquets)

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/stokkel.git
cd stokkel
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
# Option 1: Script automatique (recommandé)
python start.py

# Option 2: Manuel
# Terminal 1 - API
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Dashboard
streamlit run dashboard/app.py --server.port 8501
```

4. **Accéder à l'application**
- **Dashboard** : http://localhost:8501
- **API Documentation** : http://localhost:8000/docs

## 📖 Guide d'Utilisation

### 1. **Import des Données**
- Uploadez votre fichier CSV/Excel dans "Gestion des Données"
- Configurez le mapping des colonnes (produit, date, quantité)
- Visualisez et validez vos données

### 2. **Génération de Prévisions**
- Sélectionnez un produit dans "Prévisions"
- Choisissez l'horizon de prévision (7-90 jours)
- Visualisez les résultats avec intervalles de confiance

### 3. **Optimisation des Stocks**
- Accédez à "Recommandations"
- Configurez vos paramètres (délai, niveau de service)
- Recevez des conseils d'approvisionnement optimisés

## 🏗️ Architecture

```
stokkel/
├── app/                    # API Backend (FastAPI)
│   ├── main.py           # Point d'entrée API
│   ├── forecasting.py    # Moteur de prévisions Prophet
│   ├── optimization.py   # Moteur d'optimisation
│   ├── data_manager.py   # Gestion des données
│   └── schemas.py        # Modèles Pydantic
├── dashboard/            # Frontend (Streamlit)
│   ├── app.py           # Application principale
│   ├── components/      # Composants réutilisables
│   └── page_modules/    # Pages du dashboard
├── data/                # Données d'exemple
├── infra/               # Configuration Docker
└── scripts/             # Scripts utilitaires
```

## 🔌 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/upload_sales` | Upload données CSV |
| `GET` | `/products` | Liste des produits |
| `GET` | `/forecast/{product_id}` | Prévision produit |
| `GET` | `/recommendation/{product_id}` | Recommandation produit |
| `POST` | `/batch_recommendations` | Recommandations batch |

## 🐳 Déploiement Docker

```bash
# Build et lancement avec Docker Compose
docker-compose -f infra/docker-compose.yml up --build
```

## 📊 Données d'Exemple

Le projet inclut un fichier `data/sample_sales.csv` avec :
- **5 produits** (PROD001 à PROD005)
- **1825 lignes** de données historiques
- **365 jours** d'historique par produit
- **Données réalistes** avec saisonnalité

## 🧪 Tests

```bash
# Vérification complète du système
python check_installation.py

# Tests unitaires
python -m pytest tests/
```

## 📈 Performance

- **Prévisions** : 3-5s (première fois), ~200ms (cache)
- **Recommandations** : <1s
- **Upload CSV** : <2s (1000 lignes)
- **Interface** : <500ms (chargement)

## 🔒 Sécurité

- **Authentification** par token Bearer
- **Validation** stricte des données d'entrée
- **Sanitisation** des fichiers uploadés
- **Isolation** des environnements

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Équipe

- **Développement** : Équipe Stokkel
- **IA/ML** : Intégration Prophet
- **Design** : Interface moderne startup

## 📞 Support

- **Documentation** : [Wiki GitHub](https://github.com/votre-username/stokkel/wiki)
- **Issues** : [GitHub Issues](https://github.com/votre-username/stokkel/issues)
- **Email** : support@stokkel.ai

---

<div align="center">

**🚀 Stokkel - Transformez vos données en décisions intelligentes**

[![GitHub stars](https://img.shields.io/github/stars/votre-username/stokkel?style=social)](https://github.com/votre-username/stokkel/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/votre-username/stokkel?style=social)](https://github.com/votre-username/stokkel/network)

</div>