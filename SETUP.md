# 🚀 Koha OPAC AI Assistant — Complete Setup Guide

Anyone with a running Koha library system can follow this guide step-by-step
to install and run the AI chat assistant on their OPAC.

---

## 📋 What You Need Before Starting

| Requirement | Version | Check with |
|-------------|---------|------------|
| Koha LMS    | 26.05+  | Koha Admin → About |
| Python      | 3.10+   | `python3 --version` |
| pip         | 23+     | `pip3 --version` |
| MariaDB/MySQL | 10.6+ | Already installed with Koha |
| Debian/Ubuntu Linux | 11+ | `lsb_release -a` |

You also need **one** of these free AI API keys (pick any one):

| Provider | Free? | Get Key At |
|----------|-------|------------|
| **Groq** | ✅ Yes, free tier | https://console.groq.com |
| **Google Gemini** | ✅ Yes, free tier | https://aistudio.google.com |
| **OpenAI** | ❌ Paid | https://platform.openai.com |

> **Recommended:** Use **Groq** — it's free, fast, and requires no credit card.

---

## ⚡ Quick Overview

The setup has **2 parts**:

```
Part 1 → Backend (Python server) — runs on your server at port 8000
Part 2 → Plugin  (Koha .kpz file) — uploaded in Koha Admin
```

---

## PART 1 — Backend Server

### Step 1: Get the Code

```bash
git clone https://github.com/justatech-sleepy/koha-opac-ai-plugin.git
cd koha-opac-ai-plugin
git checkout hasnat/feature-ai-voice-vision
```

### Step 2: Set Up the Config File

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

Fill in **only these required lines** (leave everything else as-is):

```env
# --- DATABASE (copy from your Koha config) ---
DB_HOST=localhost
DB_PORT=3306
DB_NAME=koha_library        ← your Koha database name
DB_USER=koha_library        ← your Koha database user
DB_PASSWORD=your_password   ← your Koha database password

# --- AI PROVIDER (pick ONE) ---

# Option A: Groq (recommended — free, fast)
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.1-8b-instant

# Option B: Google Gemini (free)
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=AIzaSy_xxxxxxxxxxxxxxxxxxxx
# GEMINI_MODEL=gemini-1.5-flash-latest

# Option C: OpenAI (paid)
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
# OPENAI_MODEL=gpt-4o-mini

# --- CORS (set to your Koha OPAC URL) ---
ALLOWED_ORIGINS=http://localhost:8081,http://your-koha-server-ip:8081
```

> 💡 **Where to find your Koha DB credentials?**
> Check the file: `/etc/koha/sites/library/koha-conf.xml`
> Look for `<database>`, `<user>`, and `<pass>` tags.

### Step 3: Create Python Virtual Environment & Install Dependencies

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..
```

### Step 4: Start the Backend Server

```bash
bash scripts/run_backend.sh
```

You should see:
```
Starting Koha OPAC AI Assistant Backend on http://0.0.0.0:8000 ...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it works:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"1.0.1","app":"Koha OPAC AI Assistant"}
```

### Step 5: Keep It Running Permanently (Systemd Service)

So the backend starts automatically on reboot:

```bash
sudo nano /etc/systemd/system/koha-ai-backend.service
```

Paste this (replace `/path/to/koha-opac-ai-plugin` with your actual path):

```ini
[Unit]
Description=Koha OPAC AI Assistant Backend
After=network.target mariadb.service

[Service]
User=www-data
WorkingDirectory=/path/to/koha-opac-ai-plugin/backend
ExecStart=/path/to/koha-opac-ai-plugin/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure
EnvironmentFile=/path/to/koha-opac-ai-plugin/backend/.env

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now koha-ai-backend
sudo systemctl status koha-ai-backend
```

---

## PART 2 — Koha Plugin Installation

### Step 6: Build the Plugin Package

```bash
bash scripts/build.sh
```

This creates the file: `KohaOPACAIAssistant-v2.kpz`

### Step 7: Enable Plugin System in Koha

In Koha Staff Interface:
1. Go to **Administration → System Preferences**
2. Search for `UseKohaPlugins`
3. Set it to **Enable** → Save

### Step 8: Upload the Plugin

1. Go to **Administration → Plugins → Upload Plugin**
2. Select the file `KohaOPACAIAssistant-v2.kpz`
3. Click **Upload**

### Step 9: Enable & Configure the Plugin

1. Go to **Administration → Plugins**
2. Find **OPAC AI Assistant** in the list
3. Click **Enable**
4. Click **Configure**
5. Set **API Base URL** to: `http://your-server-ip:8000`
   *(This is where the Python backend is running)*
6. Click **Save**

---

## ✅ Verification

Open your Koha OPAC in a browser. You should see a **floating chat button** in the bottom-right corner.

Click it and try:
- Typing `Python books`
- Typing `Library timings`
- Clicking the 🎤 mic button and speaking a book title
- Clicking the 📷 camera button and scanning a book cover

---

## 🔁 How to Restart the Backend

If the backend stops (e.g. after reboot, if not using systemd):

```bash
cd /path/to/koha-opac-ai-plugin
bash scripts/run_backend.sh
```

---

## 🔄 How to Update After a Git Pull

```bash
git pull
bash scripts/build.sh
```

Then upload the new `KohaOPACAIAssistant-v2.kpz` via **Koha Admin → Plugins → Upload Plugin**.

---

## ❌ Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Chat widget not appearing | Plugin not enabled | Koha Admin → Plugins → Enable |
| "Unable to contact the library service" | Backend not running | Run `bash scripts/run_backend.sh` |
| "Unable to contact the library service" | Wrong API URL in plugin | Koha Admin → Plugin → Configure → check API Base URL |
| Backend crashes on start | Wrong DB credentials | Check `backend/.env` DB settings |
| No AI responses | Wrong or missing API key | Check `LLM_PROVIDER` and the matching API key in `backend/.env` |
| Backend says "address already in use" | Server already running | It's fine! Backend is already running. |
| Voice mic button does nothing | Browser blocks microphone | Allow microphone access in browser settings |
| Camera scan says "couldn't read" | Puter.js still loading | Wait 3 seconds after opening the chat, then try again |

---

## 📁 Project Structure (Reference)

```
koha-opac-ai-plugin/
├── backend/
│   ├── .env                  ← Your config (never commit this)
│   ├── .env.example          ← Template to copy from
│   ├── requirements.txt      ← Python packages
│   └── app/
│       ├── main.py           ← FastAPI server entry point
│       ├── core/config.py    ← Reads .env settings
│       ├── llm/              ← AI chat logic
│       ├── routers/          ← API routes (/api/chat, /health, etc.)
│       └── services/         ← Database search logic
├── frontend/
│   ├── js/
│   │   ├── app.js            ← Main chat logic + Voice + Vision
│   │   ├── config.js         ← Plugin config (API URL, welcome msg)
│   │   ├── ui.js             ← HTML structure of the chat widget
│   │   └── ...
│   └── css/                  ← Styles
├── Koha/Plugin/
│   └── OPACChatBot.pm        ← Perl Koha plugin module
├── scripts/
│   ├── run_backend.sh        ← Start the backend server
│   └── build.sh              ← Build the .kpz plugin file
├── KohaOPACAIAssistant-v2.kpz ← Ready-to-upload plugin package
└── SETUP.md                  ← This file
```

---

## 🔑 Quick API Key Links

- **Groq (Free):** https://console.groq.com/keys
- **Gemini (Free):** https://aistudio.google.com/app/apikey
- **OpenAI (Paid):** https://platform.openai.com/api-keys
