<div align="center">

# 🤖 Koha OPAC AI Assistant

**An intelligent, conversational search assistant for the Koha Library Management System**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Koha](https://img.shields.io/badge/Koha-26.05%2B-F97316?style=for-the-badge)](https://koha-community.org/)
[![MariaDB](https://img.shields.io/badge/MariaDB-Database-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](https://github.com/justatech-sleepy/koha-opac-ai-plugin)
[![Version](https://img.shields.io/badge/Version-1.0.1-6366F1?style=for-the-badge)](metadata.json)

<br/>

> Replace your library's traditional search forms with a modern, conversational AI assistant that understands natural language — built natively for Koha.

<br/>

[🚀 Quick Start](#-installation) · [📖 API Reference](docs/API_REFERENCE.md) · [🔌 Koha Integration](docs/KOHA_INTEGRATION.md) · [🗺️ Roadmap](#️-roadmap)

</div>

---

## 📌 Overview

**Koha OPAC AI Assistant** is a production-ready plugin that embeds a floating AI-powered chatbot directly into the Koha OPAC interface. Rather than navigating traditional search forms, patrons can simply type natural language queries and receive instant, rich book results — complete with cover images, availability status, branch location, and call numbers.

The plugin consists of two tightly coupled components:

- **FastAPI Backend** — Intent detection, query processing, and direct MariaDB integration with Koha's database schema
- **Vanilla JS Frontend** — A self-contained floating chatbot widget, injected into Koha's OPAC theme via a single `<script>` block

The system is fully modular, zero-dependency on the Koha Perl stack for search, and ships with a Koha Plugin Package (`.kpz`) for one-click installation.

---

## ✨ Features

### 🔍 Search Capabilities

| Search Type | Example Query | Intent |
|---|---|---|
| **General / Full-text** | `Python books` | `GENERAL_SEARCH` |
| **By Title** | `Find Clean Code` | `TITLE_SEARCH` |
| **By Author** | `Books by Eric Matthes` | `AUTHOR_SEARCH` |
| **By ISBN** | `9781492056355` | `ISBN_SEARCH` |
| **By Publisher** | `Publisher O'Reilly` | `PUBLISHER_SEARCH` |
| **By Barcode** | `Barcode 0001234` | `BARCODE_SEARCH` |
| **By Call Number** | `Call number 005.133` | `CALLNUMBER_SEARCH` |
| **By Branch** | `Books in Central Library` | `BRANCH_SEARCH` |
| **By Language** | `Books in French` | `LANGUAGE_SEARCH` |
| **By Year** | `Published in 2023` | `YEAR_SEARCH` |
| **Recommendations** | `Recommend books similar to Django` | `RECOMMEND` |

### 🏛️ Library Information

| Query | Intent |
|---|---|
| `Library timings`, `What are opening hours?` | `TIMINGS` |
| `Membership`, `How do I join?`, `Register` | `MEMBERSHIP` |

### 💡 UI & UX

- **Floating chatbot widget** — Accessible via a fixed-position toggle button, non-intrusive
- **Skeleton loading** — Animated placeholders while backend fetches results
- **Live autocomplete suggestions** — Debounced suggestions after 3 characters via `GET /api/suggestions`
- **Quick-action buttons** — Clickable chips in the welcome message for common queries
- **Keyboard accessible** — Full Tab/Shift+Tab focus trapping, `Escape` to close, `Enter` to send
- **Book cover integration** — Fetches covers from [Open Library Covers API](https://openlibrary.org/dev/docs/api) by ISBN with graceful fallback
- **Availability badges** — Color-coded `Available` / `Checked Out` status per title
- **Copy counts & branch** — Shows `X of Y copies` and branch location inline
- **Rate limiting** — 20 requests per 60-second window per IP with a friendly in-chat error
- **Zero `console.log` in production** — All debug output is gated behind `CONFIG.DEBUG`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Browser (Patron)                           │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │                    Koha OPAC (Apache)                        │  │
│   │                                                              │  │
│   │  opac-bottom.inc                                             │  │
│   │   └── CSS: variables → theme → chatbot → components →        │  │
│   │               animations → responsive                        │  │
│   │   └── JS:  config → knowledgeBase → faq → intentEngine →     │  │
│   │               utils → api → chatController → ui → app        │  │
│   │                             │                                │  │
│   │                    Local FAQ / Intent                        │  │
│   │                    (answered client-side)                    │  │
│   └────────────────────────────┬─────────────────────────────────┘  │
│                                │ POST /api/chat                     │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     FastAPI Backend     │
                    │                         │
                    │  main.py                │
                    │   ├── Rate Limiter      │
                    │   ├── intent_service    │◄── Regex + keyword NLP
                    │   ├── koha_service      │◄── Parameterized SQL
                    │   └── formatter_service │◄── HTML card renderer
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     MariaDB / Koha DB   │
                    │                         │
                    │  biblio                 │
                    │  biblioitems            │
                    │  items                  │
                    │  biblio_metadata (MARC) │
                    └─────────────────────────┘
```

### Intent Resolution Pipeline

```
User Message
    │
    ▼
[Frontend: intentEngine.js]  ──► Local FAQ / Knowledge Base answer (instant)
    │  (no backend call)
    │ (if not local)
    ▼
[Backend: intent_service.py]
    ├── TIMINGS / MEMBERSHIP       ──► Static HTML response
    ├── ISBN regex \d{10,13}       ──► ISBN_SEARCH
    ├── Year regex (19|20)\d{2}    ──► YEAR_SEARCH
    ├── Keyword: "by", "author"    ──► AUTHOR_SEARCH
    ├── Keyword: "publisher"       ──► PUBLISHER_SEARCH
    ├── Keyword: "branch"          ──► BRANCH_SEARCH
    ├── Keyword: "recommend"       ──► RECOMMEND → AUTHOR_SEARCH fallback
    └── Default                    ──► TITLE_SEARCH / GENERAL_SEARCH
    │
    ▼
[koha_service.py]  ──► Optimized SQL against Koha MariaDB
    │
    ▼
[formatter_service.py]  ──► HTML book cards with cover, status, branch
```

---

## 📁 Folder Structure

```
koha-opac-ai-plugin/
│
├── backend/                        # FastAPI Python backend
│   ├── requirements.txt            # Pinned dependencies
│   └── app/
│       ├── main.py                 # App entry, routes, rate limiter
│       ├── api/
│       │   └── chat.py             # /api/chat route handler
│       ├── core/
│       │   ├── config.py           # Settings via python-dotenv
│       │   └── database.py         # PyMySQL connection factory
│       ├── intents/
│       │   └── engine.py           # Knowledge-base intent matcher
│       ├── knowledge/              # Local knowledge base definitions
│       ├── llm/                    # LLM integration (planned)
│       ├── models/                 # Pydantic request/response models
│       ├── rag/                    # RAG pipeline (planned)
│       ├── services/
│       │   ├── database.py         # DB query helpers
│       │   ├── formatter_service.py# HTML book card renderer
│       │   ├── intent_service.py   # NLP intent + keyword extractor
│       │   └── koha_service.py     # All Koha DB search functions
│       └── utils/                  # Shared utility helpers
│
├── frontend/                       # Vanilla JS + CSS chatbot widget
│   ├── css/
│   │   ├── variables.css           # CSS custom properties / design tokens
│   │   ├── theme.css               # Color theme
│   │   ├── chatbot.css             # Core chatbot shell styles
│   │   ├── components.css          # Book cards, badges, skeleton, inputs
│   │   ├── animations.css          # Keyframe animations
│   │   └── responsive.css          # Mobile breakpoints
│   ├── js/
│   │   ├── config.js               # Runtime config (API URL, debug flag)
│   │   ├── knowledgeBase.js        # Local knowledge base
│   │   ├── faq.js                  # FAQ definitions
│   │   ├── intentEngine.js         # Client-side intent detection
│   │   ├── utils.js                # debounce, escapeHTML, sleep
│   │   ├── api.js                  # fetch wrappers for backend
│   │   ├── chatController.js       # Message send/receive orchestration
│   │   ├── ui.js                   # DOM builder: chat shell, skeletons
│   │   └── app.js                  # Bootstrap, event listeners, observers
│   └── assets/                     # Static assets (logo, icons)
│
├── Koha/
│   └── Plugin/
│       └── OPACChatBot.pm          # Koha Plugin Package entry point (Perl)
│
├── docs/
│   ├── API_REFERENCE.md            # REST endpoint reference
│   ├── ARCHITECTURE.md             # System architecture
│   ├── INSTALL.md                  # Detailed installation guide
│   ├── KOHA_INTEGRATION.md         # opac-bottom.inc injection guide
│   ├── Copy_Plugin_Assets.md       # Manual asset copy commands
│   └── koha_api.json               # Full Koha REST API spec (OpenAPI)
│
├── scripts/
│   ├── deploy.sh                   # One-command deploy (copy assets + restart)
│   ├── install.sh                  # Initial environment setup
│   ├── run_backend.sh              # Start uvicorn dev server
│   ├── run_frontend.sh             # Serve frontend locally
│   └── backup.sh                   # Backup plugin files
│
├── tests/
│   ├── test_api.py                 # API endpoint tests
│   ├── test_database.py            # Database layer tests
│   ├── test_intents.py             # Intent detection tests
│   └── test_search.py              # Search function tests
│
├── KohaOPACAIAssistant.kpz         # Koha Plugin Package (installable)
├── OPAC-AI-Assistant.kpz           # Alternative plugin package
├── metadata.json                   # Plugin metadata (name, version, author)
├── CHANGELOG.md                    # Version history
└── README.md                       # This file
```

---

## 🛠️ Technology Stack

### Backend
| Package | Version | Purpose |
|---|---|---|
| Python | 3.11 | Runtime |
| FastAPI | 0.139.0 | Web framework, OpenAPI, async routing |
| Uvicorn | 0.50.0 | ASGI server |
| PyMySQL | 1.2.0 | MariaDB / MySQL driver |
| Pydantic | 2.13.4 | Request/response validation |
| python-dotenv | 1.2.2 | Environment variable management |
| Starlette | 1.3.1 | ASGI toolkit (FastAPI core) |

### Frontend
| Technology | Purpose |
|---|---|
| Vanilla JavaScript (ES6+) | Chatbot logic, DOM management |
| CSS Custom Properties | Design token system |
| CSS Keyframe Animations | Skeleton loaders, transitions |
| Open Library Covers API | Book cover images by ISBN |

### Infrastructure
| Component | Technology |
|---|---|
| Web Server | Apache (with Koha Plack) |
| Database | MariaDB (Koha's existing instance) |
| OS | Debian 12 / Ubuntu 24.04 LTS |
| Plugin System | Koha Plugin Framework (`Koha::Plugins::Base`) |

---

## ✅ Compatibility

| Component | Supported Versions |
|---|---|
| **Koha** | 26.05+ (minimum), no maximum |
| **Debian** | 12 (Bookworm) |
| **Ubuntu** | 24.04 LTS |
| **MariaDB** | 10.x, 11.x |
| **Apache** | 2.4+ |
| **Python** | 3.11 |
| **Browsers** | Chrome, Firefox, Edge, Safari |

---

## 🚀 Installation

### Prerequisites

- Koha ILS installed and running
- Python 3.11 installed on the server
- Access to the Koha MariaDB database
- `sudo` access for copying assets to the Koha theme directory

---

### 1. Clone the Repository

```bash
git clone https://github.com/justatech-sleepy/koha-opac-ai-plugin.git
cd koha-opac-ai-plugin
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows

# Install pinned dependencies
pip install -r requirements.txt
```

---

### 3. Configure Environment

Create the environment file:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```env
# Application
APP_NAME=Koha OPAC AI Assistant
APP_VERSION=1.0.1
DEBUG=False

# Koha
KOHA_URL=http://localhost:8080

# Database (Koha MariaDB credentials)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=koha_library
DB_USER=koha_library
DB_PASSWORD=your_secure_password_here
```

> **Security Note:** Never commit `.env` to version control. It is already listed in `.gitignore`.

---

### 4. Start the Backend

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production (recommended)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Or use the provided script:

```bash
bash scripts/run_backend.sh
```

Verify the backend is healthy:

```bash
curl http://localhost:8000/health
# {"status":"healthy"}
```

---

### 5. Deploy Frontend Assets to Koha

Copy CSS and JavaScript files into the Koha OPAC theme directory:

```bash
sudo cp frontend/css/*.css \
  /usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/css/

sudo cp frontend/js/*.js \
  /usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/js/

sudo cp frontend/assets/logo.svg \
  /usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/
```

Or use the automated deploy script:

```bash
bash scripts/deploy.sh
```

The deploy script will copy assets, restart Apache, and restart Koha Plack automatically.

---

### 6. Inject the Plugin into Koha OPAC

Edit the Koha OPAC bottom include file:

```bash
sudo nano /usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/en/includes/opac-bottom.inc
```

Add the following **before the closing `</body>` tag**:

```html
<!-- Koha OPAC AI Assistant -->
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/variables.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/theme.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/chatbot.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/components.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/animations.css">
<link rel="stylesheet" href="/opac-tmpl/bootstrap/css/responsive.css">

<script src="/opac-tmpl/bootstrap/js/config.js"></script>
<script src="/opac-tmpl/bootstrap/js/knowledgeBase.js"></script>
<script src="/opac-tmpl/bootstrap/js/faq.js"></script>
<script src="/opac-tmpl/bootstrap/js/intentEngine.js"></script>
<script src="/opac-tmpl/bootstrap/js/utils.js"></script>
<script src="/opac-tmpl/bootstrap/js/api.js"></script>
<script src="/opac-tmpl/bootstrap/js/chatController.js"></script>
<script src="/opac-tmpl/bootstrap/js/ui.js"></script>
<script src="/opac-tmpl/bootstrap/js/app.js"></script>
<!-- End Koha OPAC AI Assistant -->
```

Then restart services:

```bash
sudo systemctl restart apache2
sudo koha-plack --restart library    # replace 'library' with your instance name
```

---

### Alternative: Install via Koha Plugin Manager

1. Log in to the Koha staff interface
2. Go to **Administration → Koha plugins**
3. Click **Upload plugin**
4. Upload `KohaOPACAIAssistant.kpz`
5. Enable the plugin

---

## ⚙️ Configuration

### Frontend Configuration

Update `frontend/js/config.js` to point to your backend:

```javascript
// config.js
window.KohaChatPlugin.CONFIG = {
  API_URL: "http://your-server:8000",   // FastAPI backend URL
  DEBUG: false,                          // Set true for development
  TYPING_DELAY: 400,                     // Simulated typing delay (ms)
  WELCOME_MESSAGE: "Hello! How can I help you find a book today?"
};
```

### Rate Limiting

Default: **20 requests per 60 seconds** per IP address. Adjust in `backend/app/main.py`:

```python
RATE_LIMIT_WINDOW = 60       # seconds
RATE_LIMIT_MAX_REQUESTS = 20 # max requests per window
```

---

## 🔌 API Reference

**Base URL:** `http://your-server:8000`

### Health Check

```http
GET /health
```
```json
{ "status": "healthy" }
```

---

### Chat

```http
POST /api/chat
Content-Type: application/json

{ "message": "Find Python books" }
```

**Response:**
```json
{
  "response": "<h3>Search Results (5)</h3><div class='books-container'>..."
}
```

Returns rendered HTML book cards directly for injection into the chat window.

**Rate limited:** 20 requests / 60 seconds per IP.

---

### Autocomplete Suggestions

```http
GET /api/suggestions?q=pyt
```
```json
{
  "suggestions": ["Python Crash Course", "Python for Data Analysis"]
}
```

Minimum query length: **3 characters**. Returns up to 7 suggestions by title match.

---

### Error Responses

All errors return HTTP `200` with a user-friendly HTML error card (for seamless chat rendering):

| Condition | Message |
|---|---|
| Rate limit exceeded | `Slow Down — You are searching too fast.` |
| Database unreachable | `Service Unavailable — The catalog is under maintenance.` |
| No results | `No books found — Try another keyword.` |

See the full API specification at [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md).

---

## 💬 Usage Examples

Type any of these directly into the chat window:

```
# Title searches
Find Python books
Show me books about Artificial Intelligence
Clean Code

# Author searches
Books by Eric Matthes
Written by Robert C. Martin

# ISBN lookup
9781492056355

# Publisher search
Publisher O'Reilly

# Branch / location
Books in Central Library

# Language
Books in French

# Publication year
Published in 2023
Books from 2020

# Recommendations
Recommend books similar to Django

# Library information
Library timings
What are your opening hours?
Membership
How do I register?
```

---

## 🔒 Security & Production Notes

- **Database credentials** are loaded from `.env` via `python-dotenv` and never hardcoded
- **SQL injection prevention** — All queries use PyMySQL parameterized statements (`%s` placeholders)
- **XSS prevention** — Book titles, authors, and branch names are HTML-escaped via `html.escape()` in `formatter_service.py`
- **Rate limiting** — Built-in per-IP rate limiter in `main.py`; no external dependency required
- **No `console.log` in production** — All frontend debug output is gated behind `CONFIG.DEBUG`
- **No stack traces exposed** — Backend exceptions are caught and returned as friendly HTML messages
- **CORS** — Currently set to `allow_origins=["*"]`; restrict this to your Koha OPAC domain in production

```python
# backend/app/main.py — restrict CORS for production
allow_origins=["https://opac.yourlibrary.org"]
```

---

## 🗺️ Roadmap

| Phase | Feature | Status |
|---|---|---|
| **Phase 1 — Core** | Floating chatbot UI | ✅ Complete |
| | Natural language intent detection | ✅ Complete |
| | Title, Author, ISBN, Publisher search | ✅ Complete |
| | Barcode, Call Number, Branch, Language, Year search | ✅ Complete |
| | Book availability & copy count | ✅ Complete |
| | Open Library cover integration | ✅ Complete |
| | Rate limiting | ✅ Complete |
| | Autocomplete suggestions | ✅ Complete |
| **Phase 2 — Advanced Search** | Subject / topic search | 🔜 Planned |
| | Advanced filter combinations | 🔜 Planned |
| | Fuzzy search tolerance | 🔜 Planned |
| **Phase 3 — AI & Recommendations** | LLM integration | 🔜 Planned |
| | RAG pipeline | 🔜 Planned |
| | Vector search | 🔜 Planned |
| | Personalized recommendations | 🔜 Planned |
| **Phase 4 — Patron Features** | User authentication | 🔜 Planned |
| | Book reservation | 🔜 Planned |
| | Fine information | 🔜 Planned |
| | Reading history | 🔜 Planned |
| | Voice search | 🔜 Planned |

---

## 🧪 Testing

```bash
cd backend
source .venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python -m pytest tests/test_api.py -v
python -m pytest tests/test_intents.py -v
python -m pytest tests/test_search.py -v
python -m pytest tests/test_database.py -v
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "feat: add subject search support"`
4. **Push** to your branch: `git push origin feature/your-feature-name`
5. **Open a Pull Request** — please describe the problem and solution clearly

**For major changes**, please open an issue first to discuss the proposed approach.

**Commit message convention:**
```
feat: add new feature
fix: correct a bug
docs: update documentation
refactor: restructure code without changing behavior
test: add or update tests
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---



## 🙏 Acknowledgements

- [**Koha Community**](https://koha-community.org/) — The world's first free and open-source library system
- [**Open Library**](https://openlibrary.org/) — Book cover images via the Covers API
- [**FastAPI**](https://fastapi.tiangolo.com/) — High-performance Python web framework
- [**MariaDB Foundation**](https://mariadb.org/) — The open-source relational database
- [**Apache Software Foundation**](https://www.apache.org/) — The web server powering Koha

---

<div align="center">

**Made with ❤️ for libraries and librarians**

⭐ Star this repo if it helps your library!

</div>
