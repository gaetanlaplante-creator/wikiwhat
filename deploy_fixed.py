import os
import subprocess

# === Configuration ===
project_path = r"C:\Users\gaeta\Documents\wikiwhat"
flutter_path = r"C:\Users\gaeta\flutter\bin\flutter.bat"
base_href = "/wikiwhat/"  # ✅ chemin GitHub Pages

os.chdir(project_path)

print("🛠️  Compilation du projet Flutter Web…")
subprocess.run([flutter_path, "build", "web", "--release"], check=True)

# === Correction automatique du <base href> ===
index_path = os.path.join(project_path, "build", "web", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remplacer base href s’il existe, sinon l’ajouter
if '<base href="' in content:
    import re
    content = re.sub(r'<base href="[^"]*"', f'<base href="{base_href}"', content)
else:
    content = content.replace(
        "<head>",
        f"<head>\n  <base href=\"{base_href}\">"
    )

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("🔧 Base href corrigé :", base_href)

# === Suppression du service worker pour simplifier le cache ===
sw_path = os.path.join(project_path, "build", "web", "flutter_service_worker.js")
if os.path.exists(sw_path):
    os.remove(sw_path)
    print("🧹 Service worker supprimé :", sw_path)

# === Commit + Push GitHub ===
print("\n📤 Déploiement sur GitHub Pages…")
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Déploiement : base href corrigé pour GitHub Pages"], check=False)
subprocess.run([
    "git", "push",
    "https://github.com/gaetanlaplante-creator/wikiwhat.git",
    "main"
], check=True)

print("\n✅ Déploiement terminé avec succès !")
print("➡️  Vérifie ton site : https://gaetanlaplante-creator.github.io/wikiwhat")
input("Appuyez sur Entrée pour continuer…")
