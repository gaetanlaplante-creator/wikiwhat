import os
import shutil
import subprocess
import sys

# ===========================
# CONFIGURATION
# ===========================
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
FLUTTER_PATH = r"C:\Users\gaeta\flutter\bin\flutter.bat"  # chemin correct vers flutter.bat
GITHUB_USER = "gaetanlaplante-creator"
REPO_NAME = "wikiwhat"
GITHUB_URL = f"https://{os.environ.get('GITHUB_TOKEN', '')}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

# ===========================
# FONCTIONS UTILITAIRES
# ===========================
def pause(msg="Appuyez sur Entrée pour continuer..."):
    input(msg)

def safe_run(cmd, cwd=PROJECT_DIR):
    try:
        print(f"> {cmd}")
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        pause()
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ Fichier introuvable : {e}")
        pause()
        sys.exit(1)

def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Dossier créé : {path}")
    else:
        print(f"Dossier existant conservé : {path}")

def check_file(path):
    if not os.path.exists(path):
        print(f"⚠️ Fichier manquant : {path}")
        pause()
    else:
        print(f"Fichier existant conservé : {path}")

# ===========================
# VERIFICATION DE L'ENVIRONNEMENT
# ===========================
print("📂 Vérification des dossiers et fichiers...")

folders = [
    os.path.join(PROJECT_DIR, "lib"),
    os.path.join(PROJECT_DIR, "assets", "images"),
    os.path.join(PROJECT_DIR, "assets", "audio"),
    os.path.join(PROJECT_DIR, "web")
]

files = [
    os.path.join(PROJECT_DIR, "lib", "main.dart"),
    os.path.join(PROJECT_DIR, "web", "index.html")
]

for f in folders:
    check_folder(f)
for f in files:
    check_file(f)

# ===========================
# BUILD FLUTTER WEB
# ===========================
print("\n✅ Build Flutter Web en cours...")
if not os.path.isfile(FLUTTER_PATH):
    print(f"❌ Flutter non trouvé : {FLUTTER_PATH}")
    pause()
    sys.exit(1)

safe_run(f'"{FLUTTER_PATH}" build web')

print("✅ Build terminé avec succès !")

# ===========================
# DEPLOIEMENT GITHUB
# ===========================
print("\n📤 Déploiement automatique sur GitHub Pages...")

# Vérifier le token
if "GITHUB_TOKEN" not in os.environ or not os.environ["GITHUB_TOKEN"]:
    print("❌ GITHUB_TOKEN non défini. Définissez-le dans les variables système.")
    pause()
    sys.exit(1)

# Copier les fichiers build/web vers root temporaire
WEB_BUILD = os.path.join(PROJECT_DIR, "build", "web")
TMP_DEPLOY = os.path.join(PROJECT_DIR, "tmp_deploy")
if os.path.exists(TMP_DEPLOY):
    shutil.rmtree(TMP_DEPLOY)
shutil.copytree(WEB_BUILD, TMP_DEPLOY)

# Git commands
safe_run("git add .")
safe_run('git commit -m "Déploiement automatique"', cwd=PROJECT_DIR)
safe_run(f"git push {GITHUB_URL} main", cwd=PROJECT_DIR)

# Nettoyage temporaire
shutil.rmtree(TMP_DEPLOY, ignore_errors=True)

print("✅ Déploiement terminé avec succès !")
pause()
