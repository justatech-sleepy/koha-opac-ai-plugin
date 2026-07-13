![Python](https://img.shields.io/badge/Python-3.11-blue)

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

![Koha](https://img.shields.io/badge/Koha-Plugin-orange)

![License](https://img.shields.io/badge/License-MIT-yellow)

![Status](https://img.shields.io/badge/Status-Active-success)

# Koha OPAC AI Plugin

Professional AI-powered OPAC assistant for Koha Library Management System.

---

## Overview

Koha OPAC AI Plugin is a modern search assistant designed for the Koha Library Management System.

It allows users to search the library catalog using natural language while providing a modern chatbot interface integrated directly into the Koha OPAC.

Instead of requiring users to navigate traditional search forms, the plugin enables conversational interactions such as:

- Find Python books
- Show Artificial Intelligence books
- Books by Eric Matthes
- Search by ISBN
- Library timings
- Membership information

The project is built with FastAPI, Vanilla JavaScript, and MariaDB while directly integrating with Koha's existing database.

---

## Features

### Current Features

- Modern floating chatbot
- Responsive UI
- Koha OPAC integration
- FastAPI backend
- Natural language search
- Search by title
- Search by author
- Search by ISBN
- Library information
- Membership information
- Book availability
- Professional book cards
- Open Library book cover integration
- Modular architecture
- Clean folder structure

---

### Planned Features

- Subject search
- Publisher search
- Advanced filters
- Recommendations
- Fuzzy search
- Voice search
- Reading history
- User authentication
- Book reservation
- Fine information
- LLM integration
- RAG
- Vector Search

---

## Screenshots

Coming Soon

### Chat Window

image

### Book Search

image

### Search Results

image

---

## Demo

Coming Soon

---

## Folder Structure

```text
koha-opac-ai-plugin/

backend/

frontend/

Koha/

docs/

scripts/

tests/

README.md
```

---

## Project Architecture

```text
Browser

↓

Koha OPAC

↓

JavaScript Plugin

↓

FastAPI Backend

↓

MariaDB

↓

Koha Database
```

---

## Technology Stack

### Backend

- Python 3.11
- FastAPI
- PyMySQL
- MariaDB

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

### Library System

- Koha
- OPAC
- Apache

---

## Installation

### Clone

```bash
git clone https://github.com/YOUR_USERNAME/koha-opac-ai-plugin.git
```

### Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Configuration

Configure database credentials inside

```text
backend/.env
```

Example

```env
DB_HOST=localhost

DB_NAME=koha_library

DB_USER=koha_library

DB_PASSWORD=********
```

---

## Usage

Example searches

```text
Find Python books

Books by Eric Matthes

Artificial Intelligence

9781492056355

Library timings

Membership
```

---

## Roadmap

Phase 1

- Modern UI

Phase 2

- Advanced Search

Phase 3

- Recommendations

Phase 4

- Authentication

Phase 5

- AI Integration

---

## Contributing

Pull Requests are welcome.

For major changes, please open an issue first.

---

## License

MIT License

---

## Author

Hasnat Khan

BS Computer Science

Koha Plugin Developer

AI & Computer Vision Enthusiast

---

## Acknowledgements

Koha Community

Open Library Covers API

FastAPI

MariaDB

Apache Foundation
