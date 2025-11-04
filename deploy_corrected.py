import os
import subprocess
import sys

# Chemins
PROJECT_PATH = r"C:\Users\gaeta\Documents\wikiwhat"
FLUTTER_PATH = r"C:\Users\gaeta\flutter\bin\flutter.bat"
BUILD_PATH = os.path.join(PROJECT_PATH, "build", "web")
SERVICE_WORKER = os.path.join(BUILD_PATH, "flutter_service_worker.js")

def run(cmd, cwd=None):
    """Exécute une commande shell et affiche la sortie"""
    try:
        print(f"\n>> Exécution : {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("⚠️ Erreur : ", e.stderr)
        sys.exit(1)

# Étape 1 : suppression du service worker obsolète
if os.path.exists(SERVICE_WORKER):
    print(f"Suppression de {SERVICE_WORKER} …")
    os.remove(SERVICE_WORKER)
else:
    print("Service worker introuvable, suppression non nécessaire.")

# Étape 2 : Build Web release
print("Génération du build Web Flutter …")
run([FLUTTER_PATH, "build", "web", "--release"], cwd=PROJECT_PATH)

# Étape 3 : git add
print("Ajout des fichiers au dépôt Git …")
run(["git", "add", "."], cwd=PROJECT_PATH)

# Étape 4 : git commit
commit_msg = "Build Web corrigé : suppression service worker, ressources locales"
print(f"Commit : {commit_msg}")
run(["git", "commit", "-m", commit_msg], cwd=PROJECT_PATH)

# Étape 5 : git push
print("Push sur GitHub (branche main) …")
run(["git", "push", "origin", "main"], cwd=PROJECT_PATH)

print("\n✅ Déploiement terminé ! Vérifie sur : https://gaetanlaplante-creator.github.io/wikiwhat")
print("N'oublie pas de vider le cache navigateur si nécessaire.")
