#!/usr/bin/env bash
# =============================================================================
# install.sh — Preflight checker for the Koha OPAC AI Assistant
#
# Verifies that the environment meets all requirements before you:
#  1. Upload the .kpz to Koha
#  2. Start the backend
#
# Usage:
#   bash scripts/install.sh
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------
# Colours
# -----------------------------------------------------------------------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

pass()  { echo -e "  ${GREEN}[PASS]${NC} $*"; }
fail()  { echo -e "  ${RED}[FAIL]${NC} $*"; ERRORS=$((ERRORS+1)); }
warn()  { echo -e "  ${YELLOW}[WARN]${NC} $*"; WARNINGS=$((WARNINGS+1)); }
info()  { echo -e "${CYAN}---------- $* ----------${NC}"; }

ERRORS=0
WARNINGS=0
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Koha OPAC AI Assistant — Preflight Check${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# -----------------------------------------------------------------------
# 1. Koha
# -----------------------------------------------------------------------
info "Koha"

if command -v koha-foreach >/dev/null 2>&1 || [[ -d /etc/koha ]]; then
    pass "Koha installation detected"
else
    warn "Could not detect Koha installation (/etc/koha missing)"
fi

# Check UseKohaPlugins
if command -v mysql >/dev/null 2>&1; then
    ENV_FILE="/etc/koha/sites/library/koha-conf.xml"
    if [[ -f "${ENV_FILE}" ]]; then
        pass "Koha config found: ${ENV_FILE}"
    else
        warn "Koha config not found (checked ${ENV_FILE})"
    fi
fi

# Check Koha version
if [[ -f /usr/share/koha/lib/Koha.pm ]]; then
    KOHA_VER=$(grep "our \$VERSION" /usr/share/koha/lib/Koha.pm | head -1 | grep -oP "[\d.]+" | head -1)
    if [[ -n "${KOHA_VER}" ]]; then
        pass "Koha version: ${KOHA_VER}"
    fi
elif command -v koha-foreach >/dev/null 2>&1; then
    pass "Koha binary tools found"
else
    warn "Cannot determine Koha version"
fi

# -----------------------------------------------------------------------
# 2. Perl modules
# -----------------------------------------------------------------------
info "Perl"

perl_module_check() {
    local mod="$1"
    if perl -e "use ${mod};" 2>/dev/null; then
        pass "Perl module: ${mod}"
    else
        fail "Perl module missing: ${mod}  (install via: cpan ${mod})"
    fi
}

perl_module_check "Modern::Perl"
perl_module_check "Koha::Plugins::Base"
perl_module_check "Koha::Logger"

# -----------------------------------------------------------------------
# 3. Python
# -----------------------------------------------------------------------
info "Python"

if command -v python3 >/dev/null 2>&1; then
    PY_VER=$(python3 --version | grep -oP "\d+\.\d+")
    PY_MAJOR=$(echo "${PY_VER}" | cut -d. -f1)
    PY_MINOR=$(echo "${PY_VER}" | cut -d. -f2)
    if [[ "${PY_MAJOR}" -ge 3 && "${PY_MINOR}" -ge 10 ]]; then
        pass "Python ${PY_VER} (≥ 3.10 required)"
    else
        fail "Python ${PY_VER} is too old — need 3.10+"
    fi
else
    fail "python3 not found"
fi

# pip
if command -v pip3 >/dev/null 2>&1 || python3 -m pip --version >/dev/null 2>&1; then
    pass "pip available"
else
    fail "pip not found — install via: apt install python3-pip"
fi

# uvicorn
if python3 -m uvicorn --version >/dev/null 2>&1 || command -v uvicorn >/dev/null 2>&1; then
    pass "uvicorn available"
else
    fail "uvicorn not found — install via: pip install uvicorn"
fi

# -----------------------------------------------------------------------
# 4. Python dependencies
# -----------------------------------------------------------------------
info "Python Dependencies"

REQ="${REPO_ROOT}/backend/requirements.txt"
if [[ -f "${REQ}" ]]; then
    while IFS= read -r pkg; do
        [[ -z "${pkg}" || "${pkg}" =~ ^# ]] && continue
        name=$(echo "${pkg}" | cut -d'[' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | cut -d'=' -f1 | tr -d ' ')
        if python3 -c "import ${name//-/_}" 2>/dev/null || python3 -c "import ${name}" 2>/dev/null; then
            pass "Python pkg: ${name}"
        else
            warn "Python pkg not installed: ${name}  (run: pip install -r backend/requirements.txt)"
        fi
    done < "${REQ}"
else
    warn "backend/requirements.txt not found"
fi

# -----------------------------------------------------------------------
# 5. MariaDB / MySQL
# -----------------------------------------------------------------------
info "Database"

if command -v mysql >/dev/null 2>&1 || command -v mariadb >/dev/null 2>&1; then
    pass "MariaDB/MySQL client available"
else
    warn "MySQL/MariaDB client not found"
fi

ENV_BACKEND="${REPO_ROOT}/backend/.env"
if [[ -f "${ENV_BACKEND}" ]]; then
    pass ".env file found: ${ENV_BACKEND}"
    for key in DB_HOST DB_NAME DB_USER DB_PASSWORD SEARCH_ENGINE; do
        if grep -q "^${key}=" "${ENV_BACKEND}"; then
            pass ".env has ${key}"
        else
            fail ".env is missing ${key}"
        fi
    done

    # Test DB connection
    source "${ENV_BACKEND}"
    if command -v mysql >/dev/null 2>&1; then
        if mysql -h"${DB_HOST:-localhost}" -u"${DB_USER:-}" -p"${DB_PASSWORD:-}" \
                 -P"${DB_PORT:-3306}" "${DB_NAME:-}" -e "SELECT 1;" >/dev/null 2>&1; then
            pass "Database connection OK (${DB_NAME:-?} on ${DB_HOST:-localhost})"
        else
            fail "Cannot connect to database — check .env credentials"
        fi
    fi
else
    fail ".env not found at ${ENV_BACKEND}"
    warn "Copy backend/.env.example to backend/.env and fill in your credentials"
fi

# -----------------------------------------------------------------------
# 6. KPZ package
# -----------------------------------------------------------------------
info "KPZ Package"

KPZ=$(find "${REPO_ROOT}" -maxdepth 1 -name "*.kpz" | head -1)
if [[ -n "${KPZ}" ]]; then
    pass "KPZ found: ${KPZ}"
    if unzip -l "${KPZ}" | grep -q "Koha/Plugin/OPACChatBot.pm"; then
        pass "KPZ contains Koha/Plugin/OPACChatBot.pm"
    else
        fail "KPZ does not contain Koha/Plugin/OPACChatBot.pm — run: bash scripts/build.sh"
    fi
else
    warn "No .kpz file found — run: bash scripts/build.sh"
fi

# -----------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------
echo ""
echo -e "${CYAN}============================================${NC}"
echo    "  PREFLIGHT SUMMARY"
echo -e "${CYAN}============================================${NC}"
echo    "  Errors:   ${ERRORS}"
echo    "  Warnings: ${WARNINGS}"

if [[ "${ERRORS}" -eq 0 ]]; then
    echo -e "  ${GREEN}Status: READY${NC}"
    echo ""
    echo "  Next steps:"
    echo "  1. Start the backend:  cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    echo "  2. Build the KPZ:      bash scripts/build.sh"
    echo "  3. Upload the KPZ:     Koha Admin → Plugins → Upload Plugin"
    echo "  4. Enable the plugin:  Koha Admin → Plugins → Enable"
else
    echo -e "  ${RED}Status: NOT READY — fix ${ERRORS} error(s) above${NC}"
fi

echo -e "${CYAN}============================================${NC}"
echo ""

exit "${ERRORS}"
