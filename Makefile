.PHONY: help install start test clean format lint docker-build docker-up docker-down deploy

# Variables
PYTHON := python
PIP := pip
UVICORN := uvicorn
STREAMLIT := streamlit

# Couleurs pour les messages
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Affiche l'aide
	@echo "$(GREEN)╔═══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║              STOKKEL - Commandes Disponibles                  ║$(NC)"
	@echo "$(GREEN)╚═══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## Installe toutes les dépendances
	@echo "$(GREEN)📦 Installation des dépendances...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dépendances installées avec succès!$(NC)"

install-dev: ## Installe les dépendances de développement
	@echo "$(GREEN)📦 Installation des dépendances de développement...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy pre-commit
	pre-commit install
	@echo "$(GREEN)✅ Environnement de développement configuré!$(NC)"

start: ## Démarre l'API et le Dashboard
	@echo "$(GREEN)🚀 Démarrage de Stokkel...$(NC)"
	$(PYTHON) start.py

start-api: ## Démarre uniquement l'API FastAPI
	@echo "$(GREEN)🚀 Démarrage de l'API...$(NC)"
	cd app && $(UVICORN) main:app --reload --host 0.0.0.0 --port 8000

start-dashboard: ## Démarre uniquement le Dashboard Streamlit
	@echo "$(GREEN)🎨 Démarrage du Dashboard...$(NC)"
	$(STREAMLIT) run dashboard/app.py --server.port 8501

test: ## Lance tous les tests
	@echo "$(GREEN)🧪 Lancement des tests...$(NC)"
	$(PYTHON) test.py
	@echo "$(GREEN)✅ Tests terminés!$(NC)"

test-coverage: ## Lance les tests avec couverture de code
	@echo "$(GREEN)🧪 Tests avec couverture...$(NC)"
	pytest --cov=app --cov=dashboard --cov-report=html --cov-report=term
	@echo "$(GREEN)📊 Rapport disponible dans htmlcov/index.html$(NC)"

format: ## Formate le code avec Black
	@echo "$(GREEN)✨ Formatage du code...$(NC)"
	black app/ dashboard/ scripts/ *.py
	@echo "$(GREEN)✅ Code formaté!$(NC)"

lint: ## Vérifie la qualité du code
	@echo "$(YELLOW)🔍 Analyse du code...$(NC)"
	flake8 app/ dashboard/ scripts/ --max-line-length=120 --exclude=__pycache__,.venv
	mypy app/ --ignore-missing-imports
	@echo "$(GREEN)✅ Code vérifié!$(NC)"

clean: ## Nettoie les fichiers temporaires
	@echo "$(YELLOW)🧹 Nettoyage...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "$(GREEN)✅ Nettoyage terminé!$(NC)"

generate-data: ## Génère des données d'exemple
	@echo "$(GREEN)📊 Génération de données de test...$(NC)"
	$(PYTHON) scripts/generate_sample_data.py
	@echo "$(GREEN)✅ Données générées dans data/sample_sales.csv$(NC)"

docker-build: ## Construit les images Docker
	@echo "$(GREEN)🐳 Construction des images Docker...$(NC)"
	docker-compose -f infra/docker-compose.yml build
	@echo "$(GREEN)✅ Images construites!$(NC)"

docker-up: ## Démarre les conteneurs Docker
	@echo "$(GREEN)🐳 Démarrage des conteneurs...$(NC)"
	docker-compose -f infra/docker-compose.yml up -d
	@echo "$(GREEN)✅ Conteneurs démarrés!$(NC)"
	@echo "$(YELLOW)🌐 API: http://localhost:8000$(NC)"
	@echo "$(YELLOW)🎨 Dashboard: http://localhost:8501$(NC)"

docker-down: ## Arrête les conteneurs Docker
	@echo "$(YELLOW)🐳 Arrêt des conteneurs...$(NC)"
	docker-compose -f infra/docker-compose.yml down
	@echo "$(GREEN)✅ Conteneurs arrêtés!$(NC)"

docker-logs: ## Affiche les logs des conteneurs
	docker-compose -f infra/docker-compose.yml logs -f

docker-restart: docker-down docker-up ## Redémarre les conteneurs Docker

setup-env: ## Crée le fichier .env depuis .env.example
	@if [ ! -f .env ]; then \
		echo "$(GREEN)📝 Création du fichier .env...$(NC)"; \
		cp env.example .env; \
		echo "$(YELLOW)⚠️  N'oubliez pas de remplir vos variables d'environnement!$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Le fichier .env existe déjà$(NC)"; \
	fi

check-security: ## Vérifie les vulnérabilités de sécurité
	@echo "$(YELLOW)🔒 Vérification de sécurité...$(NC)"
	$(PIP) install safety
	safety check
	@echo "$(GREEN)✅ Vérification terminée!$(NC)"

benchmark: ## Lance les tests de performance
	@echo "$(GREEN)⚡ Tests de performance...$(NC)"
	$(PYTHON) -m pytest tests/benchmark/ -v
	@echo "$(GREEN)✅ Benchmark terminé!$(NC)"

deploy-staging: ## Déploie sur l'environnement de staging
	@echo "$(GREEN)🚀 Déploiement staging...$(NC)"
	# Commandes de déploiement à adapter selon votre infrastructure
	@echo "$(YELLOW)⚠️  À configurer selon votre infrastructure$(NC)"

deploy-prod: ## Déploie sur l'environnement de production
	@echo "$(RED)🚨 Déploiement PRODUCTION$(NC)"
	@echo "$(YELLOW)⚠️  Êtes-vous sûr? [y/N]$(NC)"
	@read -r REPLY; \
	if [ "$$REPLY" = "y" ]; then \
		echo "$(GREEN)🚀 Déploiement en cours...$(NC)"; \
	else \
		echo "$(RED)❌ Déploiement annulé$(NC)"; \
	fi

docs: ## Génère la documentation
	@echo "$(GREEN)📚 Génération de la documentation...$(NC)"
	@echo "$(YELLOW)⚠️  À implémenter (MkDocs, Sphinx, etc.)$(NC)"

update-deps: ## Met à jour les dépendances
	@echo "$(GREEN)⬆️  Mise à jour des dépendances...$(NC)"
	$(PIP) list --outdated
	@echo "$(YELLOW)Exécutez 'pip install --upgrade <package>' pour mettre à jour$(NC)"

init-project: install setup-env generate-data ## Initialise le projet complet
	@echo "$(GREEN)╔═══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║           🎉 STOKKEL INITIALISÉ AVEC SUCCÈS ! 🎉            ║$(NC)"
	@echo "$(GREEN)╚═══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)📌 Prochaines étapes:$(NC)"
	@echo "  1. Configurez vos variables dans .env"
	@echo "  2. Lancez: $(GREEN)make start$(NC)"
	@echo "  3. Accédez au dashboard: $(GREEN)http://localhost:8501$(NC)"
	@echo ""

version: ## Affiche la version
	@echo "$(GREEN)Stokkel MVP v1.0.0$(NC)"
	@$(PYTHON) --version
	@echo "FastAPI: $$($(PIP) show fastapi | grep Version)"
	@echo "Streamlit: $$($(PIP) show streamlit | grep Version)"

# Commandes CI/CD
ci-test: ## Tests pour CI/CD
	@echo "$(GREEN)🔄 Tests CI/CD...$(NC)"
	$(PYTHON) -m pytest --cov=app --cov-report=xml

ci-lint: ## Lint pour CI/CD
	@echo "$(GREEN)🔄 Lint CI/CD...$(NC)"
	black --check app/ dashboard/ scripts/
	flake8 app/ dashboard/ scripts/ --max-line-length=120

# Valeurs par défaut
.DEFAULT_GOAL := help