"""
Script de démarrage automatique pour Stokkel MVP
Lance l'API et le dashboard en parallèle
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def print_banner():
    """Affiche le banner de démarrage"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🎯 STOKKEL - MVP Launch Script              ║
    ║                                                           ║
    ║     IA pour la Prévision des Ventes & Optimisation       ║
    ║                    des Stocks                             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'streamlit',
        'pandas',
        'prophet',
        'plotly'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n❌ Packages manquants: {', '.join(missing)}")
        print("\n💡 Installez-les avec: pip install -r requirements.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées\n")
    return True

def start_api():
    """Démarre le serveur API"""
    print("🚀 Démarrage de l'API FastAPI...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("")

    # Démarrage de l'API avec uvicorn depuis le dossier app
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="app"  # Change le répertoire de travail vers app/
    )

    return api_process

def start_dashboard():
    """Démarre le dashboard Streamlit"""
    print("🎨 Démarrage du Dashboard Streamlit...")
    print("   URL: http://localhost:8501")
    print("")
    
    # Démarrage du dashboard avec streamlit
    dashboard_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "dashboard/app.py", 
         "--server.headless", "true", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return dashboard_process

def wait_for_api():
    """Attend que l'API soit prête"""
    import requests
    
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ API prête!")
                return True
        except:
            pass
        
        time.sleep(1)
        if i % 5 == 0:
            print(f"⏳ Attente de l'API... ({i+1}/{max_attempts}s)")
    
    print("❌ L'API ne répond pas après 30 secondes")
    return False

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérification du répertoire
    if not Path("app/main.py").exists() or not Path("dashboard/app.py").exists():
        print("❌ Erreur: Fichiers app/main.py ou dashboard/app.py introuvables")
        print("💡 Assurez-vous d'être dans le bon répertoire")
        sys.exit(1)
    
    # Vérification des dépendances
    if not check_dependencies():
        sys.exit(1)
    
    print("=" * 60)
    print("🎯 DÉMARRAGE DE STOKKEL")
    print("=" * 60)
    print("")
    
    # Démarrage de l'API
    api_process = start_api()
    
    # Attente que l'API soit prête
    time.sleep(3)  # Délai initial
    
    if not wait_for_api():
        api_process.terminate()
        sys.exit(1)
    
    print("")
    
    # Démarrage du dashboard
    dashboard_process = start_dashboard()
    
    # Attente du dashboard
    time.sleep(5)
    
    print("")
    print("=" * 60)
    print("✅ STOKKEL EST OPÉRATIONNEL!")
    print("=" * 60)
    print("")
    print("📡 API Backend:      http://localhost:8000")
    print("📚 Documentation:    http://localhost:8000/docs")
    print("🎨 Dashboard:        http://localhost:8501")
    print("")
    print("=" * 60)
    print("")
    print("💡 Conseils:")
    print("   - Ouvrez http://localhost:8501 dans votre navigateur")
    print("   - Utilisez Ctrl+C pour arrêter l'application")
    print("   - Consultez README.md pour le guide d'utilisation")
    print("")
    print("🚀 Bon travail avec Stokkel!")
    print("")
    
    try:
        # Maintenir les processus en vie
        while True:
            time.sleep(1)
            
            # Vérifier que les processus sont toujours actifs
            if api_process.poll() is not None:
                print("\n❌ L'API s'est arrêtée de manière inattendue")
                dashboard_process.terminate()
                sys.exit(1)
            
            if dashboard_process.poll() is not None:
                print("\n❌ Le dashboard s'est arrêté de manière inattendue")
                api_process.terminate()
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt de Stokkel...")
        
        # Arrêt propre des processus
        print("   Arrêt du dashboard...")
        dashboard_process.terminate()
        dashboard_process.wait(timeout=5)
        
        print("   Arrêt de l'API...")
        api_process.terminate()
        api_process.wait(timeout=5)
        
        print("\n✅ Stokkel arrêté proprement")
        print("👋 À bientôt!")

if __name__ == "__main__":
    main()