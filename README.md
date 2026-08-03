# Koha OPAC AI Assistant

A production-ready universal Koha plugin that embeds an intelligent AI-powered chatbot into the Koha OPAC. Any library in the world can install and use this plugin without modifying a single line of code.

## Features

### Core
- **Universal Plugin** — Works with any Koha installation worldwide. No library-specific hardcoding.
- **No Core Hacks** — Installs completely via Koha's Plugin Manager (`.kpz`), without modifying any Koha source files.
- **Independent Backend** — Powered by a fast, asynchronous FastAPI Python backend.
- **Search Abstraction** — Modular backend supports searching via MariaDB (SQL), Zebra, or Elasticsearch.
- **Dynamic Configuration** — The Koha Staff Interface plugin configuration page allows setting the API backend URL without code changes.

### AI Intelligence
- **Multi-LLM Support** — Switch between **Groq (Llama 3)**, **Google Gemini**, and **OpenAI** by changing one line in `.env`.
- **Universal Catalog Search** — Searches across Books, Journals, Magazines, Periodicals, Newspapers, Theses, DVDs, Audio CDs, E-books, Maps, and more.
- **Conversation Memory** — Maintains context across the last 4 message pairs for a natural, human-like conversation flow.
- **Smart Query Analysis** — Internally corrects typos and spelling before searching (e.g. `"harri poter"` finds `"Harry Potter"`).
- **Subject Intelligence** — Maps natural language to proper library subjects (e.g. `"CS books"` → `subject="Computer Science"`).
- **Controlled Limits** — Returns 3 results for suggestions, 5 for specific searches, up to 30 for broad queries.

### Voice & Vision (Puter.js)
- **Voice Input (STT)** — Tap the microphone to speak your query using the native browser Web Speech API.
- **Text-to-Speech (TTS)** — Every bot reply has a speaker button to read the answer aloud.
- **Camera / Barcode Scanning** — Photograph a book cover or barcode. The Vision AI extracts the title, author, ISBN, or barcode number and searches the catalog automatically.
- **Image Rejection** — Non-book images (e.g. food, clothing) are instantly rejected with a friendly message.

### Security
- **XSS Protection** — All LLM responses are HTML-escaped before rendering.
- **Prompt Injection Defense** — System prompt enforces strict persona with off-topic refusal.
- **CORS Hardening** — API locked to specific allowed origins (configurable via `.env`).
- **Rate Limiting** — IP-based rate limiter (30 req/min) on all endpoints.
- **Input Truncation** — All tool arguments capped at 100 characters to prevent DoS via expensive SQL wildcards.
- **Empty Search Guard** — Backend rejects searches with all-blank parameters to prevent full database dumps.

### UX & Design
- **Dynamic Loading UI** — Rotating contextual status phrases ("Mining diamonds...", "Decoding the scrolls...") during processing.
- **Glassmorphism Design** — Premium dark-mode UI with blur effects, smooth gradients, and micro-animations.
- **Autocomplete Suggestions** — Real-time title suggestions while typing.
- **Responsive** — Works across desktop, tablet, and mobile.

## Architecture

```
Koha OPAC (Browser)
       │
       ▼
┌─────────────────────┐      ┌──────────────────────────┐
│  Koha Plugin (.kpz) │      │  FastAPI Backend          │
│  OPACChatBot.pm     │──────│  /api/chat                │
│  Injects JS/CSS     │      │  /api/suggestions         │
│  into OPAC          │      │                          │
└─────────────────────┘      │  llm_service.py           │
                             │  ├─ Groq / Gemini / OpenAI│
                             │  koha_service.py           │
                             │  ├─ MariaDB search         │
                             └──────────────────────────┘
```

## Quick Links

- [Installation Guide](INSTALL.md) — Step-by-step instructions to deploy the plugin and backend.
- [Build Guide](BUILD.md) — How to build the `.kpz` plugin package.
- [API Reference](docs/API.md) — Details on the backend REST endpoints.

## Requirements

- **Koha**: 26.05+
- **Database**: MariaDB 10.6+
- **Python**: 3.10+
- **Plugin System**: `UseKohaPlugins` must be enabled in Koha's system preferences.
- **LLM API Key**: Groq (free), Google Gemini (free tier), or OpenAI.

## Quick Start

### 1. Configure Backend
```bash
cd backend
cp .env.example .env
# Edit .env and set your GROQ_API_KEY (or GEMINI / OPENAI)
# Set LLM_PROVIDER=groq
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Build & Install Plugin
```bash
bash scripts/build.sh
# Upload KohaOPACAIAssistant-v2.kpz via:
# Koha Staff Interface → Administration → Manage Plugins → Upload Plugin
```

### 3. Configure Plugin
In Koha Staff Interface → Plugin Settings, set the **Backend API URL** to your FastAPI server address (e.g. `http://your-server:8000`).

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) — see the [LICENSE](LICENSE) file for details.
