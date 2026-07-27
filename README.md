# Koha OPAC AI Assistant

A production-ready Koha 26.05 plugin that embeds an AI-powered chatbot into the Koha OPAC.

The plugin provides a modern, responsive chat interface that allows library patrons to search the catalog, check item availability, and ask library-related questions (like timings and membership).

## Features

- **No Core Hacks**: Installs completely via Koha's Plugin Manager (`.kpz`), without modifying any Koha source files (no edits to `opac-bottom.inc`).
- **Independent Backend**: Powered by a fast, asynchronous FastAPI Python backend that handles intent detection and search queries.
- **Search Abstraction**: Modular backend architecture supports searching via MariaDB (SQL), Zebra, or Elasticsearch.
- **Dynamic Configuration**: The Koha Staff Interface plugin configuration page allows setting the API backend URL without changing any code.
- **Responsive UI**: A modern vanilla JS frontend injected safely into the OPAC.

## Architecture

This project is separated into two decoupled components:

1. **Koha Plugin (Frontend Injector)**: A Perl module (`OPACChatBot.pm`) that Koha loads. It injects the CSS and JavaScript for the chat widget into the OPAC.
2. **Backend Service**: A standalone FastAPI Python service that receives chat requests, detects intent, queries the Koha database or search engine, and returns results to the widget.

## Quick Links

- [Installation Guide](INSTALL.md) - Step-by-step instructions to deploy the plugin and backend.
- [Build Guide](BUILD.md) - How to build the `.kpz` plugin package.
- [API Reference](docs/API.md) - Details on the backend REST endpoints.

## Requirements

- **Koha**: 26.05+
- **Database**: MariaDB 10.6+
- **Python**: 3.10+
- **Plugin System**: `UseKohaPlugins` must be enabled in Koha's system preferences.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) — see the [LICENSE](LICENSE) file for details.
