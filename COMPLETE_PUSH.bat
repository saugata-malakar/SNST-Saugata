@echo off
echo ========================================
echo DiabetesCare AI - Complete Git Push
echo ========================================
echo.

REM Add new documentation files
echo [1/7] Adding documentation files...
git add README.md PUSH_INSTRUCTIONS.md
git commit -m "Add comprehensive README and push instructions"

REM Push to main branch
echo.
echo [2/7] Pushing to main branch...
echo NOTE: You may be prompted for GitHub credentials
git push origin main
if errorlevel 1 (
    echo.
    echo ERROR: Failed to push to main branch
    echo Please check your GitHub credentials and try again
    echo.
    echo Options:
    echo 1. Run: gh auth login
    echo 2. Or generate a Personal Access Token at: https://github.com/settings/tokens
    echo 3. Or run: git credential-manager erase https://github.com
    pause
    exit /b 1
)

REM Create Saugata's branch
echo.
echo [3/7] Creating Saugata's work branch...
git checkout -b saugata-work
echo # Saugata Malakar's Work > SAUGATA_WORK.md
echo. >> SAUGATA_WORK.md
echo ## My Contributions: >> SAUGATA_WORK.md
echo - ML wound severity model (ml/wound_severity/) >> SAUGATA_WORK.md
echo - ML wound tissue classification (ml/wound_tissue/) >> SAUGATA_WORK.md
echo - Federated learning implementation (sahil_federated/) >> SAUGATA_WORK.md
echo - Frontend interface (frontend/) >> SAUGATA_WORK.md
echo - Training scripts and utilities >> SAUGATA_WORK.md
echo - Batch automation scripts >> SAUGATA_WORK.md
git add SAUGATA_WORK.md
git commit -m "Saugata Malakar's contributions - ML, FL, and Frontend"

echo.
echo [4/7] Pushing Saugata's branch...
git push origin saugata-work

REM Create Professor's branch
echo.
echo [5/7] Creating Professor's work branch...
git checkout main
git checkout -b professor-sharif-work
echo # Professor Sharif Hossain Sarkar's Work > PROFESSOR_WORK.md
echo. >> PROFESSOR_WORK.md
echo ## Professor's Contributions: >> PROFESSOR_WORK.md
echo - Backend API enhancements (backend/api/) >> PROFESSOR_WORK.md
echo - Privacy and data erasure features (backend/database/erasure.py) >> PROFESSOR_WORK.md
echo - Security implementations >> PROFESSOR_WORK.md
echo - Database model improvements (backend/database/models.py) >> PROFESSOR_WORK.md
echo - Configuration management (backend/utils/config.py) >> PROFESSOR_WORK.md
echo - Export functionality (backend/api/routers/export.py) >> PROFESSOR_WORK.md
git add PROFESSOR_WORK.md
git commit -m "Professor Sharif's contributions - Backend, Security, and Privacy"

echo.
echo [6/7] Pushing Professor's branch...
git push origin professor-sharif-work

REM Return to main and show summary
echo.
echo [7/7] Returning to main branch...
git checkout main

echo.
echo ========================================
echo SUCCESS! All branches pushed
echo ========================================
echo.
echo Branch Structure:
git branch -a
echo.
echo Repository URL: https://github.com/dkg-diabetescare-ai/diabetescare-ai
echo.
echo Next Steps:
echo 1. Visit the repository on GitHub
echo 2. Verify all three branches are present
echo 3. Set main as the default branch if needed
echo 4. Add collaborators with appropriate permissions
echo.
pause
