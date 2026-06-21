#!/bin/bash
# METACYTECH - Launcher for Linux / Android (Termux)
# Cross-platform launcher - works on Linux, macOS, and Android (Termux)

set -e

# Colors
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
CYAN='\033[0;96m'
WHITE='\033[1;97m'
RESET='\033[0m'

clear

echo -e "${RED}============================================================${RESET}"
echo ""
echo -e "${WHITE}   M   M  EEEE  TTTTT   A     C   C  Y   Y  TTTTT  EEEE  C   C  H   H${RESET}"
echo -e "${WHITE}   MM MM  E        T    A A    C       Y Y      T    E      C   C   H H${RESET}"
echo -e "${WHITE}   M M M  EEE      T   A   A   C        Y       T    EEE    C C    HHH${RESET}"
echo -e "${WHITE}   M   M  E        T   AAAAA    C       Y       T    E      C   C   H H${RESET}"
echo -e "${WHITE}   M   M  EEEE     T   A   A    C      Y       T    EEEE   C   C   H H${RESET}"
echo ""
echo -e "${RED}============================================================${RESET}"
echo -e "${WHITE}  METACYTECH  *  Cloudflare Tunnel  *  Telegram${RESET}"
echo -e "${RED}============================================================${RESET}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}  [ERROR] Python tidak ditemukan! Install Python 3.8+${RESET}"
    echo ""
    # Detect package manager
    if command -v pkg &> /dev/null; then
        echo -e "${YELLOW}  Termux detected. Install with: pkg install python${RESET}"
    elif command -v apt &> /dev/null; then
        echo -e "${YELLOW}  Install with: sudo apt install python3${RESET}"
    elif command -v pacman &> /dev/null; then
        echo -e "${YELLOW}  Install with: sudo pacman -S python${RESET}"
    elif command -v dnf &> /dev/null; then
        echo -e "${YELLOW}  Install with: sudo dnf install python3${RESET}"
    else
        echo -e "${YELLOW}  Download: https://www.python.org/downloads/${RESET}"
    fi
    echo ""
    exit 1
fi

# Use python3 if available, fallback to python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check launcher.py
if [ ! -f "launcher.py" ]; then
    echo -e "${RED}  [ERROR] launcher.py tidak ditemukan!${RESET}"
    echo "  Current dir: $(pwd)"
    echo ""
    exit 1
fi

# Check and install Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}  Installing dependencies...${RESET}"
    npm install
fi

# Check and install cloudflared (Termux / Linux)
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}  cloudflared not found, attempting to install...${RESET}"
    if command -v pkg &> /dev/null; then
        # Termux
        pkg install cloudflared -y 2>/dev/null || echo -e "${YELLOW}  Manual install: download from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/${RESET}"
    elif command -v apt &> /dev/null; then
        # Debian/Ubuntu
        ARCH=$(uname -m)
        if [ "$ARCH" = "x86_64" ]; then
            wget -q "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64" -O /tmp/cloudflared && chmod +x /tmp/cloudflared && sudo mv /tmp/cloudflared /usr/local/bin/ 2>/dev/null || echo -e "${YELLOW}  Manual install needed${RESET}"
        elif [ "$ARCH" = "aarch64" ]; then
            wget -q "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64" -O /tmp/cloudflared && chmod +x /tmp/cloudflared && sudo mv /tmp/cloudflared /usr/local/bin/ 2>/dev/null || echo -e "${YELLOW}  Manual install needed${RESET}"
        fi
    fi
fi

# Run the launcher
echo -e "${CYAN}  Starting METACYTECH launcher...${RESET}"
echo -e "${RED}============================================================${RESET}"
echo ""
$PYTHON_CMD launcher.py
