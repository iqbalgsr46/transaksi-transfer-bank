@echo off
echo ============================================
echo   BANK TRANSFER VERIFICATION LAUNCHER
echo   100%% FREE - Python + Ngrok + Next.js
echo ============================================
echo.

echo [1] Checking Python...
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2] Checking Ngrok...
ngrok --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ngrok not found in PATH.
    echo Please install ngrok from: https://ngrok.com/download
    echo OR install via: choco install ngrok
    echo OR: npm install -g ngrok
    echo.
    set /p CONTINUE="Continue without ngrok? (y/n): "
    if /i not "%CONTINUE%"=="y" (
        pause
        exit /b 1
    )
)

echo.
echo [3] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo [4] Checking dependencies...
if not exist "node_modules" (
    echo ⚠️  node_modules not found. Installing...
    call npm install
) else (
    echo ✅ Node.js dependencies found
)

echo.
echo [5] Checking Python dependencies...
pip install -r requirements.txt --quiet

echo.
echo [6] Checking Telegram configuration...
if exist ".env.local" (
    echo ✅ .env.local found
) else (
    echo ⚠️  .env.local not found
    echo    Data will not be sent to Telegram
    echo    Create .env.local with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
)

echo.
echo ============================================
echo   🚀 STARTING SYSTEM...
echo ============================================
echo.

python launcher.py

echo.
echo ============================================
echo   System stopped.
echo ============================================
pause