import os
import subprocess
import re
import shutil

# ==============================
# ⚙️ CONFIGURATION
# ==============================
PROJECT_PATH = r"C:\Users\gaeta\Documents\wikiwhat"
FLUTTER_PATH = r"C:\Users\gaeta\flutter\bin\flutter.bat"
GITHUB_USER = "gaetanlaplante-creator"
REPO_NAME = "wikiwhat"
BASE_HREF = "/wikiwhat/"

# Token depuis les variables d’environnement (✅ sans popup)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("❌ Le token GitHub (GITHUB_TOKEN) n’est pas défini dans Windows.")
    print("➡️  Va dans : Panneau de configuration → Système → Paramètres avancés → Variables d’environnement")
    print("   Puis crée une variable utilisateur nommée GITHUB_TOKEN avec ton token personnel.")
    input("\nAppuie sur Entrée pour quitter…")
    exit(1)

GITHUB_URL = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

os.chdir(PROJECT_PATH)

# ==============================
# 🛠️ BUILD FLUTTER WEB
# ==============================
print("🛠️  Compilation du projet Flutter Web…")
subprocess.run([FLUTTER_PATH, "build", "web", "--release"], check=True)

# ==============================
# 🧹 POST-TRAITEMENT
# ==============================
index_path = os.path.join(PROJECT_PATH, "build", "web", "index.html")
sw_path = os.path.join(PROJECT_PATH, "build", "web", "flutter_service_worker.js")

# Correction du <base href>
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

if '<base href="' in content:
    content = re.sub(r'<base href="[^"]*"', f'<base href="{BASE_HREF}"', content)
else:
    content = content.replace("<head>", f"<head>\n  <base href=\"{BASE_HREF}\">")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"🔧 Base href corrigé : {BASE_HREF}")

# Suppression du service worker pour éviter le cache
if os.path.exists(sw_path):
    os.remove(sw_path)
    print("🧹 Service worker supprimé :", sw_path)

# ==============================
# 📤 DEPLOIEMENT AUTOMATIQUE
# ==============================
print("\n📤 Déploiement automatique sur GitHub Pages…")

subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Déploiement automatisé : base href corrigé"], check=False)
subprocess.run(["git", "push", GITHUB_URL, "main"], check=True)

print("\n✅ Déploiement terminé avec succès !")
print("➡️  Vérifie ton site : https://gaetanlaplante-creator.github.io/wikiwhat")
input("\nAppuie sur Entrée pour quitter…")
