# 🔄 Guide de Migration - Intégration des Fichiers

Ce document explique comment intégrer les nouveaux fichiers générés avec votre structure existante.

## 📋 Mapping des Fichiers

### ✅ Fichiers à remplacer/fusionner

| Ancien Fichier | Nouveau Fichier | Action |
|----------------|-----------------|--------|
| `app/main.py` | `api.py` | **Renommer** `api.py` → `app/main.py` |
| `app/forecast_engine.py` | `forecasting.py` | **Renommer** `forecasting.py` → `app/forecast_engine.py` |
| `dashboard/app.py` | `dashboard.py` | **Renommer** `dashboard.py` → `dashboard/app.py` |

### ✨ Nouveaux fichiers à ajouter

| Fichier Généré | Destination | Description |
|----------------|-------------|-------------|
| `start.py` | `start.py` (racine) | Script démarrage automatique |
| `test.py` | `test.py` (racine) | Suite de tests complète |
| `Makefile` | `Makefile` (racine) | Commandes automatisées |
| `env.example` | `env.example` (racine) | Template configuration |
| `requirements.txt` | Fusionner avec existant | Dépendances complètes |
| `infra/docker-compose.yml` | Remplacer | Version avec monitoring |
| `infra/Dockerfile.api` | Remplacer | Image optimisée |
| `infra/Dockerfile.ui` | Remplacer | Image optimisée |
| `scripts/generate_sample_data.py` | Remplacer/améliorer | Version avancée |
| `.github/workflows/ci.yml` | Remplacer | Pipeline complet |
| `ARCHITECTURE.md` | Ajouter | Documentation technique |

---

## 🚀 Plan de Migration (Étape par Étape)

### Étape 1: Sauvegarde

```bash
# Créer une branche de backup
git checkout -b backup-before-migration
git add .
git commit -m "backup: save current state before migration"

# Revenir sur develop
git checkout develop
git checkout -b feature/integrate-new-code
```

### Étape 2: Intégration de l'API

```bash
# Sauvegarder votre ancien main.py
cp app/main.py app/main.py.old

# Copier le nouveau code API
cp api.py app/main.py

# Vérifier les imports
# Si vous aviez des fonctions custom dans l'ancien main.py:
# - Les ajouter manuellement dans le nouveau app/main.py
# - Ou créer un fichier app/custom_routes.py
```

**Modifications nécessaires dans `app/main.py`:**

```python
# Changer les imports relatifs
# AVANT:
from forecasting import SalesForecaster, StockOptimizer

# APRÈS:
from app.forecast_engine import SalesForecaster, StockOptimizer
```

### Étape 3: Intégration du Moteur IA

```bash
# Sauvegarder ancien forecast_engine
cp app/forecast_engine.py app/forecast_engine.py.old

# Copier le nouveau moteur
cp forecasting.py app/forecast_engine.py
```

**Vérifications:**
- ✅ Classes `SalesForecaster` et `StockOptimizer` présentes
- ✅ Méthodes compatibles avec ancienne API
- ✅ Imports fonctionnent

### Étape 4: Intégration du Dashboard

```bash
# Sauvegarder ancien dashboard
cp dashboard/app.py dashboard/app.py.old

# Copier le nouveau dashboard
cp dashboard.py dashboard/app.py
```

**Configuration API URL:**

Dans `dashboard/app.py`, ligne ~30:

```python
# Si API sur même machine:
API_BASE_URL = "http://localhost:8000"

# Si API Docker:
API_BASE_URL = "http://api:8000"

# Si API production:
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

### Étape 5: Ajout des Fichiers Utilitaires

```bash
# Copier les nouveaux fichiers
cp start.py ./start.py
cp test.py ./test.py
cp Makefile ./Makefile
cp env.example ./env.example

# Rendre exécutables
chmod +x start.py test.py
```

### Étape 6: Mise à Jour Docker

```bash
# Backup
cp infra/docker-compose.yml infra/docker-compose.yml.old
cp infra/Dockerfile.api infra/Dockerfile.api.old
cp infra/Dockerfile.ui infra/Dockerfile.ui.old

# Copier nouveaux fichiers
cp docker-compose.yml infra/
cp Dockerfile.api infra/
cp Dockerfile.ui infra/
```

### Étape 7: Fusion des requirements.txt

```bash
# Créer un fichier temporaire avec les deux versions
cat requirements.txt > requirements_new.txt
cat requirements.txt.old | grep -v "^#" >> requirements_new.txt

# Supprimer les doublons et trier
sort requirements_new.txt | uniq > requirements.txt

# Vérifier
cat requirements.txt
```

### Étape 8: Configuration de l'Environnement

```bash
# Créer .env depuis template
cp env.example .env

# Éditer avec vos valeurs
nano .env  # ou vim, code, etc.
```

**Variables essentielles à configurer:**

```bash
# Minimum requis pour démarrer:
API_ENV=development
DATABASE_URL=postgresql://...  # Si vous utilisez PostgreSQL
SECRET_KEY=votre_secret_key_aleatoire_32_chars
```

### Étape 9: CI/CD

```bash
# Backup
cp .github/workflows/ci.yml .github/workflows/ci.yml.old

# Copier nouveau pipeline
cp ci.yml .github/workflows/ci.yml
```

**Secrets GitHub à configurer:**

Dans Settings → Secrets and variables → Actions:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `PRODUCTION_HOST`
- `PRODUCTION_USER`
- `SSH_PRIVATE_KEY`
- `SLACK_WEBHOOK` (optionnel)

### Étape 10: Tests

```bash
# 1. Installer dépendances
make install

# 2. Générer données test
make generate-data

# 3. Lancer tests
make test

# 4. Démarrer l'application
make start
```

---

## 🔍 Vérification Post-Migration

### Checklist Fonctionnelle

- [ ] L'API démarre sans erreur (`http://localhost:8000`)
- [ ] La doc API est accessible (`http://localhost:8000/docs`)
- [ ] Le dashboard démarre (`http://localhost:8501`)
- [ ] Upload CSV fonctionne
- [ ] Génération de prévision fonctionne
- [ ] Recommandations fonctionnent
- [ ] Tests passent (`make test`)
- [ ] Docker build réussit (`make docker-build`)

### Commandes de Diagnostic

```bash
# Vérifier imports Python
python -c "from app.main import app; print('✅ API OK')"
python -c "from app.forecast_engine import SalesForecaster; print('✅ Forecaster OK')"

# Tester l'API
curl http://localhost:8000/health

# Voir logs API
tail -f logs/api.log  # si logs configurés

# Voir processus Docker
docker-compose ps
docker-compose logs api
```

---

## ⚠️ Problèmes Courants & Solutions

### Problème 1: Imports ne fonctionnent pas

**Erreur:**
```
ModuleNotFoundError: No module named 'forecasting'
```

**Solution:**
```python
# Dans app/main.py, changer:
from forecasting import SalesForecaster
# EN:
from app.forecast_engine import SalesForecaster
```

### Problème 2: API ne trouve pas les données

**Erreur:**
```
KeyError: 'main' in sales_data_store
```

**Solution:**
- Uploader des données via le dashboard ou
- Utiliser `make generate-data` pour créer des données test

### Problème 3: Dashboard ne se connecte pas à l'API

**Erreur:**
```
ConnectionError: Cannot connect to API
```

**Solution:**
```python
# Dans dashboard/app.py, vérifier:
API_BASE_URL = "http://localhost:8000"  # Pas http://api:8000 en dev local
```

### Problème 4: Docker containers ne démarrent pas

**Solution:**
```bash
# Nettoyer tout et recommencer
docker-compose down -v
docker system prune -f
make docker-build
make docker-up
```

---

## 🎯 Améliorations Recommandées

### Court Terme (Semaine 1)

1. **Créer `app/data_utils.py`** avec fonctions utilitaires:
```python
def validate_sales_data(df):
    """Valide le format du CSV"""
    required_cols = ['product_id', 'date', 'quantity']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        return False, f"Colonnes manquantes: {missing}"
    return True, None

def prepare_forecast_data(df, product_id):
    """Prépare les données pour Prophet"""
    # ... implémentation
```

2. **Ajouter `app/models.py`** avec modèles Pydantic additionnels

3. **Créer tests unitaires** dans `tests/`

### Moyen Terme (Mois 1)

1. **Ajouter authentification JWT**
2. **Implémenter PostgreSQL** (remplacer stockage mémoire)
3. **Ajouter Redis pour cache**
4. **Setup monitoring** (Prometheus/Grafana)

### Long Terme (Trimestre 1)

1. **API versioning** (`/api/v1/...`)
2. **Webhooks pour notifications**
3. **Multi-tenancy complet**
4. **Deployment Kubernetes**

---

## 📞 Besoin d'Aide?

Si vous rencontrez des difficultés:

1. **Vérifiez les logs:** `make docker-logs` ou `python start.py`
2. **Tests diagnostics:** `make test`
3. **Comparez avec backup:** `git diff backup-before-migration`
4. **Documentation:** Voir `README.md` et `ARCHITECTURE.md`

---

**Bonne migration! 🚀**