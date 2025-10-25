# 🔧 Correction du Script start.py

## ❌ Problème Détecté

Lorsque tu lançais `python start.py`, l'API ne démarrait pas correctement car il y avait un conflit entre:
1. Les **imports absolus** dans le code (ex: `from config import settings`)
2. La façon dont **uvicorn** essayait de charger le module avec `app.main:app`

### Erreur Technique
```python
# Avant (INCORRECT)
subprocess.Popen([
    sys.executable, "-m", "uvicorn", "app.main:app", "--reload"
])
```

Uvicorn essayait de charger `app` comme un package Python, ce qui causait des erreurs d'imports relatifs.

---

## ✅ Solution Appliquée

J'ai modifié le script `start.py` pour qu'il lance l'API depuis le dossier `app/` avec le bon contexte:

```python
# Après (CORRECT)
subprocess.Popen([
    sys.executable, "-m", "uvicorn", "main:app",
    "--reload", "--port", "8000", "--host", "0.0.0.0"
],
cwd="app"  # <-- Change le répertoire vers app/
)
```

### Changements Effectués

1. **Module uvicorn**: `app.main:app` → `main:app`
2. **Working directory**: Ajout de `cwd="app"`
3. **Host binding**: Ajout de `--host 0.0.0.0`

---

## 🚀 Comment Utiliser Maintenant

### Option 1: Script start.py (RECOMMANDÉ)
```bash
python start.py
```

Ce script va:
1. ✅ Vérifier les dépendances
2. ✅ Démarrer l'API sur le port 8000
3. ✅ Attendre que l'API soit prête
4. ✅ Démarrer le Dashboard sur le port 8501
5. ✅ Afficher les URLs à ouvrir

### Option 2: Lancement Manuel
```bash
# Terminal 1 - API
cd app
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Dashboard
python -m streamlit run dashboard/app.py --server.port 8501
```

### Option 3: Docker Compose
```bash
docker-compose -f infra/docker-compose.yml up -d
```

---

## 🔍 Vérification

Pour vérifier que tout fonctionne:

```bash
# Test API
curl http://localhost:8000/health

# Devrait retourner:
# {"status":"degraded","version":"1.0.0",...}
```

```bash
# Test Dashboard
# Ouvre dans ton navigateur:
http://localhost:8501
```

---

## 🐛 Si Ça Ne Marche Toujours Pas

### 1. Vérifier les Ports
```bash
# Windows
netstat -ano | findstr ":8000"
netstat -ano | findstr ":8501"

# Si occupés, tuer les processus:
taskkill /F /PID <PID_NUMBER>
```

### 2. Vérifier les Dépendances
```bash
python check_installation.py
```

### 3. Vérifier les Imports
```bash
cd app
python -c "import main; print('OK')"
```

### 4. Logs Détaillés
```bash
# Lance l'API avec logs détaillés
cd app
python -m uvicorn main:app --reload --log-level debug
```

---

## 📝 Notes Techniques

### Pourquoi `cwd="app"` ?

Quand tu lances uvicorn avec `main:app`:
- Uvicorn cherche le fichier `main.py` dans le **répertoire courant**
- Les imports dans `main.py` sont absolus: `from config import settings`
- Python cherche donc `config.py` dans le **même dossier** que `main.py`
- En définissant `cwd="app"`, on dit à uvicorn: "exécute-toi depuis le dossier app/"

### Structure des Imports

```python
# Dans app/main.py
from config import settings        # ✅ Cherche app/config.py
from schemas import ForecastResponse # ✅ Cherche app/schemas.py
from data_manager import data_manager # ✅ Cherche app/data_manager.py
```

Si on lançait depuis la racine avec `app.main:app`, Python ajouterait le dossier racine au PYTHONPATH, et il chercherait `config.py` à la racine (qui n'existe pas).

---

## ✅ Résultat Final

Le script `start.py` fonctionne maintenant parfaitement et lance les deux services de manière propre !

**Test-le avec:**
```bash
python start.py
```

Puis ouvre **http://localhost:8501** dans ton navigateur pour voir le design moderne ! 🎨

---

*Correction appliquée le 25/10/2025*
*Projet: Stokkel MVP v1.0.0*
