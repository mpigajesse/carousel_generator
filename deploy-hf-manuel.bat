@echo off
REM =============================================================================
REM deploy-hf-manuel.bat - Guide pas à pas pour le déploiement manuel
REM =============================================================================

echo.
echo ============================================================
echo   GUIDE DE DEPLOIEMENT MANUEL - HUGGING FACE SPACES
echo ============================================================
echo.
echo Ce script vous guide etape par etape pour deployer sur HF Spaces.
echo.
pause

echo.
echo ETAPE 1/5 : Verifier que vous avez un compte Hugging Face
echo.
echo -> Ouvrez https://huggingface.co dans votre navigateur
echo -> Si vous n'avez pas de compte, cliquez sur "Sign Up"
echo.
pause

echo.
echo ETAPE 2/5 : Creer un nouveau Space
echo.
echo -> Allez sur https://huggingface.co/new-space
echo -> Remplissez:
echo    Space name: carousel-generator
echo    License: MIT
echo    Visibility: Public (ou Private si vous preferez)
echo    SDK: Docker
echo    Owner: mpigajesse23
echo.
pause

echo.
echo ETAPE 3/5 : Preparer le dossier de deploiement
echo.
echo Appuyez sur une touche pour creer le dossier hf-deploy et copier les fichiers...
pause

REM Créer le dossier
if exist "hf-deploy" (
    echo Dossier hf-deploy existe deja, nettoyage...
    rd /s /q hf-deploy
)
mkdir hf-deploy
cd hf-deploy

echo.
echo Copie des fichiers...

REM Initialiser git
git init

REM Copier les fichiers
copy ..\main.py .
copy ..\app.py .
copy ..\generate.py .
copy ..\themes.py .
copy ..\md_parser.py .
copy ..\slide.html.j2 .
copy ..\requirements_hf.txt requirements.txt
xcopy /E /I /Y ..\templates templates
xcopy /E /I /Y ..\static static
copy ..\Dockerfile.hf Dockerfile
copy ..\README_hf.md README.md

echo.
echo Fichiers copies avec succes!

cd ..

echo.
echo ETAPE 4/5 : Configurer Git pour Hugging Face
echo.
echo Dans le dossier hf-deploy, executez:
echo.
echo   cd hf-deploy
echo   git remote add origin https://huggingface.co/spaces/mpigajesse23/carousel-generator
echo   git add .
echo   git commit -m "Deploy initial"
echo   git push -u origin main
echo.
echo IMPORTANT: Vous aurez besoin de vos identifiants Hugging Face
echo Pour generer un token: https://huggingface.co/settings/tokens
echo.
pause

echo.
echo ETAPE 5/5 : Verifier le deploiement
echo.
echo Apres le push, allez sur:
echo https://huggingface.co/spaces/mpigajesse23/carousel-generator
echo.
echo Le build prend 2-5 minutes. Vous pouvez voir les logs dans l'onglet "App".
echo.
echo ============================================================
echo   GUIDE TERMINE!
echo ============================================================
echo.
pause
