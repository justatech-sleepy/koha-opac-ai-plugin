# Build Guide

> How to build and publish the `KohaOPACAIAssistant-v2.kpz` plugin package.

---

## Quick Build

```bash
# From the repository root
bash scripts/build.sh
```

This produces `KohaOPACAIAssistant-v2.kpz` ready to upload to Koha.

---

## What `build.sh` Does

| Step | Action |
|------|--------|
| 1 | Checks prerequisites (`zip`, `python3`) |
| 2 | Validates `metadata.json` (required fields, `canonicalname` format) |
| 3 | Validates `Koha/Plugin/OPACChatBot.pm` (package declaration, Perl syntax) |
| 4 | Checks frontend CSS and JS files exist |
| 5 | Cleans previous build artifacts |
| 6 | Assembles the package in a temp directory with correct paths |
| 7 | Creates the `.kpz` (zip archive) with Unix path separators |
| 8 | Verifies the archive (required entries, no Windows backslashes, `canonicalname`) |
| 9 | Reports size and file count |

---

## KPZ Package Structure

```
KohaOPACAIAssistant-v2.kpz
├── metadata.json
├── README.md
├── LICENSE
├── Koha/
│   └── Plugin/
│       └── OPACChatBot.pm
├── css/
│   ├── variables.css
│   ├── theme.css
│   ├── components.css
│   ├── chatbot.css
│   ├── responsive.css
│   └── animations.css
├── js/
│   ├── config.js
│   ├── icons.js
│   ├── utils.js
│   ├── faq.js
│   ├── knowledgeBase.js
│   ├── intentEngine.js
│   ├── api.js
│   ├── ui.js
│   ├── chatController.js
│   └── app.js
└── images/
    ├── logo.svg
    └── icons/
        └── *.svg
```

> **Important:** `frontend/` from the source tree is NOT included in the KPZ.
> `build.sh` copies `frontend/css/` → `css/` and `frontend/js/` → `js/` at the archive root.

---

## Manual Build (if needed)

```bash
# Create a clean temp directory
mkdir /tmp/kpz_build
mkdir -p /tmp/kpz_build/Koha/Plugin
mkdir -p /tmp/kpz_build/css /tmp/kpz_build/js /tmp/kpz_build/images

# Copy plugin files
cp Koha/Plugin/OPACChatBot.pm /tmp/kpz_build/Koha/Plugin/
cp metadata.json README.md LICENSE /tmp/kpz_build/

# Copy CSS in load order
for f in variables.css theme.css components.css chatbot.css responsive.css animations.css; do
    cp frontend/css/$f /tmp/kpz_build/css/
done

# Copy JS in load order
for f in config.js icons.js utils.js faq.js knowledgeBase.js intentEngine.js api.js ui.js chatController.js app.js; do
    cp frontend/js/$f /tmp/kpz_build/js/
done

# Zip (must be done from inside the temp dir for correct paths)
cd /tmp/kpz_build
zip -r /path/to/repo/KohaOPACAIAssistant-v2.kpz .

# Verify
unzip -l /path/to/repo/KohaOPACAIAssistant-v2.kpz
```

---

## Common Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `metadata.json is missing fields` | Required field absent | Add the missing field to `metadata.json` |
| `canonicalname must start with Koha::Plugin::` | Wrong `canonicalname` value | Fix `metadata.json` |
| `Koha/Plugin/OPACChatBot.pm does not declare package` | Package name mismatch | Check the `package` line in the `.pm` |
| `Windows backslash paths found` | Built on Windows | Build on Linux/WSL only |
| `No .css files found` | Missing `frontend/css/` | Ensure CSS files exist |

---

## Versioning

Update the version in **both** files when releasing:

| File | Key |
|------|-----|
| `metadata.json` | `"version": "x.y.z"` |
| `Koha/Plugin/OPACChatBot.pm` | `version => 'x.y.z',` |

Use [Semantic Versioning](https://semver.org/):
- **PATCH** (`1.0.1 → 1.0.2`): Bug fixes, CSS/JS tweaks
- **MINOR** (`1.0.x → 1.1.0`): New features, new endpoints
- **MAJOR** (`1.x → 2.0.0`): Breaking changes, Koha version requirement change

---

## CI/CD

GitHub Actions automatically builds the KPZ on every push to `main` and `feature/**` branches.
The built `.kpz` is uploaded as a GitHub Actions artifact for 30 days.
