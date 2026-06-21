# 🏦 Transaksi Transfer Bank

Aplikasi web transfer bank dengan integrasi Telegram Bot untuk notifikasi real-time. Dibangun dengan **Next.js 16** + **React 19** dan dilengkapi Python launcher dengan **ngrok tunnel**.

## ✨ Fitur

- 📱 Tampilan responsive (mobile-friendly)
- 🔔 Notifikasi Telegram real-time
- 🌐 Ngrok tunnel untuk akses dari mana saja
- 🖥️ One-click launcher (Python + Batch)

## 📋 Persyaratan

| Komponen | Versi Minimum |
|----------|---------------|
| Node.js  | 18+           |
| npm      | 9+            |
| Python   | 3.8+          |
| ngrok    | any           |

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/iqbalgsr46/transaksi-transfer-bank.git
cd transaksi-transfer-bank
```

### 2. Install Dependencies

**Node.js dependencies:**
```bash
npm install
```

**Python dependencies (untuk launcher):**
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Copy file `.env.example` menjadi `.env.local`:

```bash
cp .env.example .env.local
```

Lalu edit `.env.local` dan isi dengan data Anda:

```env
TELEGRAM_BOT_TOKEN=your_token_dari_botfather
TELEGRAM_CHAT_ID=your_chat_id
```

### 4. Jalankan

**Menggunakan launcher (recommended):**
```bash
python launcher.py
```
Atau di Windows, klik ganda `run.bat`

**Manual (dev server saja):**
```bash
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000)

## 📂 Struktur Project

```
transaksi-transfer-bank/
├── src/                    # Source code Next.js
│   └── app/                # App Router pages
├── public/                 # Static assets
├── templates/              # HTML templates
├── launcher.py             # Python launcher + ngrok
├── run.bat                 # Windows launcher
├── start.bat               # Windows quick start
├── start.ps1               # PowerShell launcher
├── run.sh                  # Linux/Mac launcher
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
└── .env.local              # Environment variables (NOT committed)
```

## ⚙️ Konfigurasi Telegram Bot

1. Buka Telegram, cari **@BotFather**
2. Ketik `/newbot` dan ikuti instruksi
3. Copy token yang diberikan → paste ke `TELEGRAM_BOT_TOKEN`
4. Kirim pesan ke **@userinfobot** untuk mendapatkan chat ID
5. Paste chat ID ke `TELEGRAM_CHAT_ID`

## 🔧 Build for Production

```bash
npm run build
npm run start
```

## 📄 License

MIT

---

Made with ❤️ by [iqbalgsr46](https://github.com/iqbalgsr46)
