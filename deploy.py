import os
import subprocess
import shutil

# ===========================
# Configuration des chemins
# ===========================
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
FLUTTER_BAT = r"C:\Users\gaeta\Documents\flutter\bin\flutter.bat"  # Chemin complet pour Windows
FOLDERS = [
    "lib",
    "assets/images",
    "assets/audio",
    "web"
]

FILES = {
    "lib/main.dart": "// main.dart existant ou vide",
    "web/index.html": "<!-- index.html existant ou vide -->"
}

# ===========================
# Création des dossiers
# ===========================
for folder in FOLDERS:
    folder_path = os.path.join(PROJECT_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Dossier créé ou existant : {folder}")

# ===========================
# Création des fichiers si absents
# ===========================
for file_path, content in FILES.items():
    full_path = os.path.join(PROJECT_DIR, file_path)
    if not os.path.exists(full_path):
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fichier créé : {file_path}")
    else:
        print(f"Fichier existant conservé : {file_path}")

# ===========================
# Build Flutter Web
# ===========================
try:
    print("\n✅ Build Flutter Web en cours...")
    subprocess.run([FLUTTER_BAT, "build", "web"], check=True)
    print("✅ Build terminé avec succès !")
except subprocess.CalledProcessError as e:
    print("❌ Erreur lors du build Flutter Web :", e)
except FileNotFoundError:
    print("❌ Flutter.bat introuvable, vérifier le chemin dans le script")

# ===========================
# Déploiement GitHub (exemple simplifié)
# ===========================
# Note : Utiliser GITHUB_TOKEN comme variable système, jamais en clair
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Déploiement automatique"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("✅ Déploiement GitHub terminé !")
except subprocess.CalledProcessError as e:
    print("❌ Erreur Git :", e)

print("\n📌 Script terminé.")
