@echo off
chcp 65001 >nul 2>&1
title METACYTECH - Launcher
cd /d "%~dp0"

echo.
echo  ============================================================
echo.
echo    M   M  EEEE  TTTTT   A     C   C  Y   Y  TTTTT  EEEE  C   C  H   H
echo    MM MM  E        T    A A    C       Y Y      T    E      C   C   H H
echo    M M M  EEE      T   A   A   C        Y       T    EEE    C C    HHH
echo    M   M  E        T   AAAAA    C       Y       T    E      C   C   H H
echo    M   M  EEEE     T   A   A    C      Y       T    EEEE   C   C   H H
echo.
echo  ============================================================
echo.
echo    Dual Template: BNI + TikTok  *  Cloudflare Tunnel
echo.
echo  ============================================================
echo.

:: Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python tidak ditemukan! Install Python 3.8+
    echo  Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check launcher.py exists
if not exist "launcher.py" (
    echo  [ERROR] launcher.py tidak ditemukan!
    echo  Current dir: %cd%
    echo.
    pause
    exit /b 1
)

:: Run the launcher
echo  Starting METACYTECH launcher...
echo  ============================================================
echo.
python launcher.py

:: If launcher exits with error, show message
if errorlevel 1 (
    echo.
    echo  ============================================================
    echo  [ERROR] Launcher error code: %errorlevel%
    echo  ============================================================
    echo.
    pause
)
