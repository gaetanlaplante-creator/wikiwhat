import os
import subprocess
import sys

# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------
# Nom du dépôt et branche
REPO_NAME = "wikiwhat"
BRANCH = "main"
USERNAME = "gaeta-laplante"  # Ton compte GitHub
# Chemin complet vers flutter.bat (Windows)
FLUTTER_PATH = r"C:\Users\gaeta\Documents\flutter\bin\flutter.bat"

# Dossiers à créer
folders = [
    "lib",
    "assets/images",
    "assets/audio",
    "web"
]

# Fichiers à préserver
files_to_keep = [
    "lib/main.dart",
    "web/index.html"
]

# Vérification token GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ Erreur : la variable d'environnement GITHUB_TOKEN n'est pas définie.")
    sys.exit(1)

REPO_URL = f"https://{GITHUB_TOKEN}@github.com/{USERNAME}/{REPO_NAME}.git"

# -------------------------------------------------------------------
# 1️⃣ Création des dossiers
# -------------------------------------------------------------------
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Dossier créé ou existant : {folder}")

# -------------------------------------------------------------------
# 2️⃣ Vérification des fichiers existants
# -------------------------------------------------------------------
for file_path in files_to_keep:
    if os.path.exists(file_path):
        print(f"Fichier existant conservé : {file_path}")
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("// fichier initial\n")
        print(f"Fichier créé : {file_path}")

# -------------------------------------------------------------------
# 3️⃣ Build Flutter Web
# -------------------------------------------------------------------
print("\n✅ Build Flutter Web en cours...")
try:
    subprocess.run([FLUTTER_PATH, "build", "web"], check=True)
    print("✅ Build terminé avec succès !")
except subprocess.CalledProcessError as e:
    print(f"❌ Build Flutter Web échoué : {e}")
    sys.exit(1)

# -------------------------------------------------------------------
# 4️⃣ Git add, commit et push automatique
# -------------------------------------------------------------------
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Déploiement automatique"], check=True)
    subprocess.run(["git", "push", REPO_URL, BRANCH], check=True)
    print("\n✅ Déploiement GitHub terminé avec succès !")
except subprocess.CalledProcessError as e:
    print(f"❌ Git operation échouée : {e}")
    sys.exit(1)

# -------------------------------------------------------------------
# 5️⃣ Fin
# -------------------------------------------------------------------
print("\n🎉 Script terminé. Vous pouvez ouvrir votre dépôt GitHub pour vérifier le déploiement.")
