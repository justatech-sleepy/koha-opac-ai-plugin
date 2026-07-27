# Installation Guide

> **Koha OPAC AI Assistant** — v1.0.1 | Koha ≥ 26.05 | Python ≥ 3.10

---

## Table of Contents

1. [Requirements](#requirements)
2. [Backend Setup](#backend-setup)
3. [Plugin Installation](#plugin-installation)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Upgrading](#upgrading)
7. [Uninstalling](#uninstalling)
8. [Troubleshooting](#troubleshooting)

---

## Requirements

| Component | Minimum Version |
|-----------|----------------|
| Koha | 26.05 |
| MariaDB | 10.6 |
| Python | 3.10 |
| pip | 23.0 |
| uvicorn | 0.20 |
| Debian / Ubuntu | 11+ |

**Koha must have the Plugin System enabled:**

```
# In Koha system preferences:
UseKohaPlugins = 1
```

---

## Backend Setup

### 1. Clone the repository

```bash
git clone https://github.com/justatech-sleepy/koha-opac-ai-plugin.git
cd koha-opac-ai-plugin
git checkout feature/standalone-kpz-plugin
```

### 2. Create and configure `.env`

```bash
cp backend/.env.example backend/.env
nano backend/.env
```

Fill in at minimum:

```env
DB_HOST=localhost
DB_NAME=koha_library
DB_USER=koha_library
DB_PASSWORD=your_password
SEARCH_ENGINE=sql
```

### 3. Create a Python virtual environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the preflight check

```bash
cd ..   # back to repo root
bash scripts/install.sh
```

All items should show `[PASS]`.

### 5. Start the backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production (persistent), use systemd:

```bash
# /etc/systemd/system/koha-ai-backend.service
[Unit]
Description=Koha OPAC AI Assistant Backend
After=network.target mariadb.service

[Service]
User=www-data
WorkingDirectory=/path/to/koha-opac-ai-plugin/backend
ExecStart=/path/to/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure
EnvironmentFile=/path/to/koha-opac-ai-plugin/backend/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now koha-ai-backend
```

Verify:

```bash
curl http://localhost:8000/health
# {"status":"healthy","version":"1.0.1","app":"Koha OPAC AI Assistant"}
```

---

## Plugin Installation

### 1. Build the KPZ package

```bash
bash scripts/build.sh
# Output: KohaOPACAIAssistant-v2.kpz
```

### 2. Upload via Koha Admin

1. Log in to the **Koha Staff Interface**
2. Go to **Administration → Plugins → Upload Plugin**
3. Select `KohaOPACAIAssistant-v2.kpz`
4. Click **Upload**

### 3. Enable and configure

1. Go to **Administration → Plugins**
2. Find **OPAC AI Assistant** in the list
3. Click **Enable**
4. Click **Configure**
5. Set **API Base URL** to the URL of your backend, e.g. `http://your-server:8000`
6. Click **Save**

---

## Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| API Base URL | URL of the FastAPI backend | `http://127.0.0.1:8000` |
| Plugin Enabled | Enable/disable the chat widget | `1` (enabled) |
| Debug Mode | Enable browser console logging | `0` (disabled) |

---

## Verification

After installation, open the Koha OPAC in a browser:

- The chat widget (floating button) should appear in the bottom-right corner.
- Click the button to open the chat window.
- Type a search query, e.g. `Python books`

If the widget does not appear:

```bash
# Check Koha OPAC error log
sudo tail -50 /var/log/koha/library/opac-error.log

# Check the backend is running
curl http://localhost:8000/health

# Verify the plugin is enabled
# Koha Admin → Plugins → OPAC AI Assistant → Status
```

---

## Upgrading

1. Pull the latest code: `git pull`
2. Rebuild the KPZ: `bash scripts/build.sh`
3. Upload the new `.kpz` via **Koha Admin → Plugins → Upload Plugin**
4. Koha will call the plugin's `upgrade()` hook automatically.

---

## Uninstalling

1. Go to **Koha Admin → Plugins → OPAC AI Assistant**
2. Click **Disable**, then **Uninstall**
3. Stop and remove the backend service if no longer needed:
   ```bash
   sudo systemctl disable --now koha-ai-backend
   ```

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Plugin not in list after upload | Wrong KPZ structure or missing `canonicalname` | Run `bash scripts/build.sh` to rebuild |
| `Can't locate Koha/Plugin/OPACChatBot.pm` | KPZ used Windows path separators | Rebuild with `build.sh` on Linux |
| Chat widget not appearing | Plugin not enabled or JS error | Enable plugin; check browser console |
| Backend connection refused | Backend not running or wrong API URL | Start backend; check Configure → API Base URL |
| Database connection failed | Wrong `.env` credentials | Verify `backend/.env` settings |
| Rate limit error | Too many requests from same IP | Wait 60 seconds |
