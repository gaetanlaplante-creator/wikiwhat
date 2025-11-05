import os
import shutil
import subprocess
import sys

# ===========================
# CONFIGURATION
# ===========================
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
FLUTTER_PATH = r"C:\Users\gaeta\flutter\bin\flutter.bat"
GITHUB_USER = "gaetanlaplante-creator"
REPO_NAME = "wikiwhat"
GITHUB_URL = f"https://{os.environ.get('GITHUB_TOKEN', '')}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

# ===========================
# FONCTIONS UTILITAIRES
# ===========================
def pause(msg="Appuyez sur Entrée pour continuer..."):
    input(msg)

def safe_run(cmd, cwd=PROJECT_DIR):
    print(f"> {cmd}")
    try:
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur : {e}")
        pause()
        sys.exit(1)

# ===========================
# ÉTAPE 1 : BUILD FLUTTER
# ===========================
print("🛠️  Compilation du projet Flutter Web…")
if not os.path.isfile(FLUTTER_PATH):
    print("❌ Flutter introuvable.")
    pause()
    sys.exit(1)

safe_run(f'"{FLUTTER_PATH}" build web --release')

# ===========================
# ÉTAPE 2 : SUPPRESSION SERVICE WORKER
# ===========================
SERVICE_WORKER = os.path.join(PROJECT_DIR, "build", "web", "flutter_service_worker.js")
if os.path.exists(SERVICE_WORKER):
    print(f"🧹 Suppression du service worker : {SERVICE_WORKER}")
    os.remove(SERVICE_WORKER)
else:
    print("⚠️ Aucun service worker trouvé, rien à supprimer.")

# ===========================
# ÉTAPE 3 : DEPLOIEMENT GIT
# ===========================
print("\n📤 Déploiement sur GitHub Pages…")

if not os.environ.get("GITHUB_TOKEN"):
    print("❌ GITHUB_TOKEN manquant. Définis-le avant d’exécuter ce script.")
    pause()
    sys.exit(1)

safe_run("git add .")
safe_run('git commit -m "Déploiement : build Flutter Web sans service worker"')
safe_run(f"git push {GITHUB_URL} main")

print("\n✅ Déploiement terminé avec succès !")
print("➡️  Vérifie ton site : https://gaetanlaplante-creator.github.io/wikiwhat")
pause()
