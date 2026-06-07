@echo off
echo ========================================
echo GitHub Authentication Fix
echo ========================================
echo.
echo This script will help fix GitHub authentication issues.
echo.
echo Choose an option:
echo.
echo 1. Clear cached GitHub credentials (then retry push)
echo 2. Show current git configuration
echo 3. Test GitHub connection
echo 4. Open GitHub PAT creation page
echo 5. Cancel
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto clear_creds
if "%choice%"=="2" goto show_config
if "%choice%"=="3" goto test_connection
if "%choice%"=="4" goto open_token
if "%choice%"=="5" goto end

:clear_creds
echo.
echo Clearing GitHub credentials...
git credential-manager erase https://github.com
echo Done!
echo.
echo Now try running: COMPLETE_PUSH.bat
echo You will be prompted for your GitHub username and password/token.
echo.
goto end

:show_config
echo.
echo Current Git Configuration:
echo.
git config --list | findstr "user\|remote\|credential"
echo.
goto end

:test_connection
echo.
echo Testing GitHub connection...
git ls-remote https://github.com/dkg-diabetescare-ai/diabetescare-ai.git
if errorlevel 1 (
    echo.
    echo ERROR: Cannot connect to repository
    echo This likely means authentication is required.
) else (
    echo.
    echo SUCCESS: Connection works!
)
echo.
goto end

:open_token
echo.
echo Opening GitHub Personal Access Token creation page...
start https://github.com/settings/tokens/new
echo.
echo Steps to create a token:
echo 1. Give it a name: "diabetescare-ai-push"
echo 2. Select scope: "repo" (Full control of private repositories)
echo 3. Click "Generate token"
echo 4. Copy the token (you won't see it again!)
echo.
echo Then run this command (replace YOUR_TOKEN):
echo git remote set-url origin https://YOUR_TOKEN@github.com/dkg-diabetescare-ai/diabetescare-ai.git
echo.
goto end

:end
echo.
pause
