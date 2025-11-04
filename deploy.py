import os
import subprocess
import sys
import shutil

# ------------------------------
# Configuration utilisateur
# ------------------------------
PROJECT_DIR = r"C:\Users\gaeta\Documents\wikiwhat"
GITHUB_USER = "gaetanlaplante-creator"
REPO_NAME = "wikiwhat"
BRANCH_WEB = "gh-pages"
MAIN_DART = os.path.join(PROJECT_DIR, "lib", "main.dart")
TOKEN = os.environ.get("GITHUB_TOKEN")

# ------------------------------
# Fonctions utilitaires
# ------------------------------
def safe_run(cmd, cwd=None):
    """Exécute une commande et reste ouvert si erreur"""
    try:
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Commande échouée: {cmd}\nErreur: {e}")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)

def ensure_dir(path):
    """Crée un dossier s'il n'existe pas"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Dossier créé : {path}")
    else:
        print(f"Dossier existant conservé : {path}")

def ensure_file(path):
    """Crée un fichier vide s'il n'existe pas"""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
        print(f"Fichier créé : {path}")
    else:
        print(f"Fichier existant conservé : {path}")

# ------------------------------
# Préparation des dossiers
# ------------------------------
dirs_to_create = [
    os.path.join(PROJECT_DIR, "lib"),
    os.path.join(PROJECT_DIR, "assets", "images"),
    os.path.join(PROJECT_DIR, "assets", "audio"),
    os.path.join(PROJECT_DIR, "web")
]

for d in dirs_to_create:
    ensure_dir(d)

ensure_file(MAIN_DART)
ensure_file(os.path.join(PROJECT_DIR, "web", "index.html"))

# ------------------------------
# Build Flutter Web
# ------------------------------
print("\n✅ Build Flutter Web en cours...")
safe_run(f"flutter build web --release", cwd=PROJECT_DIR)
print("✅ Build terminé avec succès !")

# ------------------------------
# Git operations
# ------------------------------
os.chdir(PROJECT_DIR)

# Vérifier que TOKEN est défini
if not TOKEN:
    print("❌ Erreur : GITHUB_TOKEN non défini dans les variables d'environnement.")
    input("Appuyez sur Entrée pour fermer...")
    sys.exit(1)

# Initialiser git si besoin
if not os.path.exists(os.path.join(PROJECT_DIR, ".git")):
    safe_run("git init", cwd=PROJECT_DIR)

# Ajouter remote si nécessaire
remote_url = f"https://{TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
safe_run(f"git remote remove origin || echo 'remote not found'", cwd=PROJECT_DIR)
safe_run(f"git remote add origin {remote_url}", cwd=PROJECT_DIR)

# Commit et push
safe_run("git add .", cwd=PROJECT_DIR)
safe_run('git commit -m "Déploiement automatique"', cwd=PROJECT_DIR)
safe_run(f"git push origin main --force", cwd=PROJECT_DIR)

print("\n✅ Déploiement terminé avec succès !")
input("Appuyez sur Entrée pour fermer...")
