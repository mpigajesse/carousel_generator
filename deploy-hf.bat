@echo off
REM =============================================================================
REM deploy-hf.bat - Script de déploiement automatique sur Hugging Face Spaces
REM =============================================================================

echo.
echo ============================================================
echo   DEPLOIEMENT CAROUSEL GENERATOR SUR HUGGING FACE SPACES
echo ============================================================
echo.

REM Vérifier que git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe. Installez-le depuis https://git-scm.com
    pause
    exit /b 1
)

echo [1/6] Verification des fichiers...
if not exist "main.py" (
    echo ERREUR: main.py non trouve!
    pause
    exit /b 1
)
if not exist "Dockerfile.hf" (
    echo ERREUR: Dockerfile.hf non trouve!
    pause
    exit /b 1
)
if not exist "requirements_hf.txt" (
    echo ERREUR: requirements_hf.txt non trouve!
    pause
    exit /b 1
)
echo   ✓ Tous les fichiers sont presents

echo.
echo [2/6] Clone du Space Hugging Face...
if exist "hf-deploy" (
    echo   Suppression de l'ancien dossier hf-deploy...
    rd /s /q hf-deploy
)

git clone https://huggingface.co/spaces/mpigajesse23/carousel-generator hf-deploy
if errorlevel 1 (
    echo ERREUR: Impossible de cloner le Space HF
    pause
    exit /b 1
)
echo   ✓ Space clone

echo.
echo [3/6] Copie des fichiers...
cd hf-deploy

REM Copier tous les fichiers nécessaires
copy ..\main.py .
copy ..\app.py .
copy ..\generate.py .
copy ..\themes.py .
copy ..\md_parser.py .
copy ..\slide.html.j2 .
copy ..\requirements_hf.txt requirements.txt
copy ..\requirements.txt requirements_flask.txt

REM Copier les dossiers
xcopy /E /I /Y ..\templates templates
xcopy /E /I /Y ..\static static

REM Copier le Dockerfile HF
copy ..\Dockerfile.hf Dockerfile
echo   ✓ Fichiers copies

echo.
echo [4/6] Commit des changements...
git add .
git commit -m "🚀 Deploy Carousel Generator v2 - FastAPI + Docker"
echo   ✓ Commit effectue

echo.
echo [5/6] Push vers Hugging Face...
git push
if errorlevel 1 (
    echo.
    echo ATTENTION: Le push a echoue. Verifiez vos identifiants HF.
    echo.
    echo Vous pouvez essayer manuellement:
    echo   cd hf-deploy
    echo   git push
    echo.
) else (
    echo   ✓ Push effectue avec succes
)

echo.
echo [6/6] Nettoyage...
cd ..
echo   ✓ Terminé

echo.
echo ============================================================
echo   DEPLOIEMENT TERMINE!
echo ============================================================
echo.
echo Votre application sera disponible dans quelques minutes a:
echo https://huggingface.co/spaces/mpigajesse23/carousel-generator
echo.
echo Pour verifier le statut du build:
echo   cd hf-deploy
echo   git log
echo.
pause
