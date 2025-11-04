import os
import subprocess
import shutil

# ================================
# Configuration
# ================================
FLUTTER_PATH = r"C:\Users\gaeta\flutter\bin\flutter.bat"
PROJECT_PATH = os.getcwd()
BUILD_WEB_PATH = os.path.join(PROJECT_PATH, "build", "web")
INDEX_HTML_PATH = os.path.join(BUILD_WEB_PATH, "index.html")
SERVICE_WORKER = os.path.join(BUILD_WEB_PATH, "flutter_service_worker.js")

# ================================
# 1. Supprimer le service worker
# ================================
if os.path.exists(SERVICE_WORKER):
    print(f"Suppression de {SERVICE_WORKER} …")
    os.remove(SERVICE_WORKER)

# ================================
# 2. Préparer index.html avec CSP
# ================================
if os.path.exists(INDEX_HTML_PATH):
    print("Ajout de Content Security Policy dans index.html …")
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Vérifie si CSP déjà présent
    if "Content-Security-Policy" not in content:
        csp_meta = ('<meta http-equiv="Content-Security-Policy" '
                    'content="default-src \'self\'; '
                    'script-src \'self\'; '
                    'style-src \'self\' \'unsafe-inline\'; '
                    'img-src \'self\' data:;">\n')
        # Injecte dans <head>
        content = content.replace("<head>", "<head>\n    " + csp_meta)

        with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(content)

# ================================
# 3. Build Web Flutter --release
# ================================
print("\nGénération du build Web Flutter …\n")
subprocess.run([FLUTTER_PATH, "build", "web", "--release"], check=True)

# ================================
# 4. Git add / commit / push
# ================================
print("\nAjout des fichiers au dépôt Git …\n")
subprocess.run(["git", "add", "."], check=True)

commit_message = "Build Web corrigé : suppression service worker, CSP local"
print(f"\nCommit : {commit_message}\n")
subprocess.run(["git", "commit", "-m", commit_message], check=True)

print("\nPush sur GitHub (branche main) …\n")
subprocess.run(["git", "push", "origin", "main"], check=True)

print("\n✅ Déploiement terminé ! Vérifie sur : https://gaetanlaplante-creator.github.io/wikiwhat")
print("N'oublie pas de vider le cache navigateur si nécessaire.")
