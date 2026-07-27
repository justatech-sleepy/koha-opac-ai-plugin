"""
tests/test_plugin.py

Validates the Koha plugin's metadata and Perl module without requiring
a live Koha installation.

Run with:
    pytest tests/test_plugin.py -v
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
METADATA  = REPO_ROOT / "metadata.json"
PM_FILE   = REPO_ROOT / "Koha" / "Plugin" / "OPACChatBot.pm"


# -----------------------------------------------------------------------
# metadata.json tests
# -----------------------------------------------------------------------

class TestMetadata:
    def setup_method(self):
        with open(METADATA) as f:
            self.meta = json.load(f)

    def test_metadata_is_valid_json(self):
        assert isinstance(self.meta, dict)

    def test_required_fields_present(self):
        required = ["name", "author", "canonicalname", "description",
                    "minimum_version", "version"]
        missing = [k for k in required if not self.meta.get(k)]
        assert missing == [], f"Missing fields: {missing}"

    def test_canonicalname_is_koha_plugin(self):
        canonical = self.meta.get("canonicalname", "")
        assert canonical.startswith("Koha::Plugin::"), \
            f"canonicalname must start with 'Koha::Plugin::' — got: {canonical}"

    def test_version_is_semver(self):
        version = self.meta.get("version", "")
        assert re.match(r"^\d+\.\d+\.\d+$", version), \
            f"version must be semver (x.y.z) — got: {version}"

    def test_minimum_version_is_set(self):
        min_ver = self.meta.get("minimum_version", "")
        assert min_ver, "minimum_version must not be empty"

    def test_canonicalname_matches_pm_package(self):
        """metadata.json canonicalname must match the package declaration in OPACChatBot.pm"""
        canonical = self.meta["canonicalname"]
        content   = PM_FILE.read_text(encoding="utf-8")
        expected  = f"package {canonical};"
        assert expected in content, \
            f"'{expected}' not found in OPACChatBot.pm — canonicalname mismatch"


# -----------------------------------------------------------------------
# OPACChatBot.pm structure tests
# -----------------------------------------------------------------------

class TestPluginModule:
    def setup_method(self):
        self.content = PM_FILE.read_text(encoding="utf-8")

    def test_pm_file_exists(self):
        assert PM_FILE.exists(), f"Plugin module not found: {PM_FILE}"

    def test_package_declaration(self):
        assert "package Koha::Plugin::OPACChatBot;" in self.content

    def test_uses_koha_plugins_base(self):
        assert "use base qw(Koha::Plugins::Base)" in self.content

    def test_metadata_hash_exists(self):
        assert "our $metadata" in self.content

    def test_has_new_constructor(self):
        assert "sub new" in self.content

    def test_has_install_hook(self):
        assert "sub install" in self.content, \
            "Plugin must implement install() lifecycle hook"

    def test_has_upgrade_hook(self):
        assert "sub upgrade" in self.content, \
            "Plugin must implement upgrade() lifecycle hook"

    def test_has_uninstall_hook(self):
        assert "sub uninstall" in self.content, \
            "Plugin must implement uninstall() lifecycle hook"

    def test_has_opac_head(self):
        assert "sub opac_head" in self.content

    def test_has_opac_js(self):
        assert "sub opac_js" in self.content

    def test_ends_with_one(self):
        # Perl modules must end with 1;
        assert self.content.strip().endswith("1;"), \
            "OPACChatBot.pm must end with '1;'"

    def test_no_hardcoded_api_calls(self):
        # The .pm may store a default URL in retrieve_data/store_data as a fallback.
        # What we MUST NOT have is a direct HTTP call (LWP, curl, etc.) to a hardcoded host.
        # The API URL must always come from retrieve_data('api_base_url').
        import re
        # Detect LWP::UserAgent->get("http://...") or similar patterns
        pattern = r"""LWP|HTTP::Request|http_get|curl.*127\.0\.0\.1"""
        match = re.search(pattern, self.content)
        assert match is None, \
            f"Found hardcoded HTTP call in OPACChatBot.pm — use retrieve_data('api_base_url') instead"


    def test_uses_koha_logger(self):
        assert "Koha::Logger" in self.content, \
            "Plugin should use Koha::Logger for proper logging"

    def test_perl_syntax(self):
        """Run 'perl -c' if perl is available."""
        if sys.platform == "win32":
            return  # skip on Windows CI
        result = subprocess.run(
            ["perl", "-I/usr/share/koha/lib", "-c", str(PM_FILE)],
            capture_output=True, text=True
        )
        # Exit code 0 = syntax OK, but Koha modules may not be installed locally
        # We consider it a pass if there are only "Can't locate" errors (missing Koha runtime)
        if result.returncode != 0:
            errors = result.stderr
            koha_only_errors = all(
                "Can't locate" in line or "syntax OK" in line
                for line in errors.splitlines() if line.strip()
            )
            assert koha_only_errors, \
                f"Perl syntax errors in OPACChatBot.pm:\n{errors}"


# -----------------------------------------------------------------------
# KPZ package tests
# -----------------------------------------------------------------------

class TestKpzPackage:
    def setup_method(self):
        kpz_files = list(REPO_ROOT.glob("*.kpz"))
        self.kpz = kpz_files[0] if kpz_files else None

    def test_kpz_exists(self):
        assert self.kpz is not None, \
            "No .kpz file found — run: bash scripts/build.sh"

    def test_kpz_contains_pm(self):
        if self.kpz is None:
            return
        result = subprocess.run(
            ["unzip", "-l", str(self.kpz)], capture_output=True, text=True
        )
        assert "Koha/Plugin/OPACChatBot.pm" in result.stdout, \
            "KPZ does not contain Koha/Plugin/OPACChatBot.pm"

    def test_kpz_has_unix_paths(self):
        if self.kpz is None:
            return
        result = subprocess.run(
            ["unzip", "-l", str(self.kpz)], capture_output=True, text=True
        )
        assert "\\" not in result.stdout, \
            "KPZ contains Windows backslash paths — this will break Koha on Linux"

    def test_kpz_contains_css(self):
        if self.kpz is None:
            return
        result = subprocess.run(
            ["unzip", "-l", str(self.kpz)], capture_output=True, text=True
        )
        assert "Koha/Plugin/OPACChatBot/css/" in result.stdout, "KPZ does not contain Koha/Plugin/OPACChatBot/css/ directory"

    def test_kpz_contains_js(self):
        if self.kpz is None:
            return
        result = subprocess.run(
            ["unzip", "-l", str(self.kpz)], capture_output=True, text=True
        )
        assert "Koha/Plugin/OPACChatBot/js/" in result.stdout, "KPZ does not contain Koha/Plugin/OPACChatBot/js/ directory"

    def test_kpz_metadata_canonicalname(self):
        if self.kpz is None:
            return
        result = subprocess.run(
            ["unzip", "-p", str(self.kpz), "metadata.json"],
            capture_output=True, text=True
        )
        meta = json.loads(result.stdout)
        assert meta.get("canonicalname") == "Koha::Plugin::OPACChatBot", \
            f"KPZ metadata.json has wrong canonicalname: {meta.get('canonicalname')}"
