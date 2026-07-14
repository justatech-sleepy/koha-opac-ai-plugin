package Koha::Plugin::OPACChatBot;

# OPAC AI Assistant — Koha Plugin
# Injects a floating AI chatbot into the Koha OPAC.
#
# Hooks implemented:
#   opac_head  — injects CSS <link> tags into every OPAC page <head>
#   opac_js    — injects JS <script> tags before </body> on every OPAC page
#   configure  — settings page in Koha Staff admin (backend URL, debug, etc.)
#   install    — sets sensible defaults on first install
#   upgrade    — placeholder for future migrations

use Modern::Perl;
use base qw(Koha::Plugins::Base);
use CGI qw(-utf8);

our $metadata = {
    name            => 'OPAC AI Assistant',
    author          => 'Hasnat Khan',
    description     => 'AI-powered floating chatbot for Koha OPAC — searches catalog by title, author, ISBN, publisher, language, year, and more.',
    date_authored   => '2026-07-05',
    date_updated    => '2026-07-14',
    minimum_version => '26.05',
    maximum_version => undef,
    version         => '2.0.0',
};

# ─── Constructor ────────────────────────────────────────────────────────────────

sub new {
    my ( $class, $args ) = @_;
    $args->{metadata} = $metadata;
    return $class->SUPER::new($args);
}

# ─── Lifecycle Hooks ────────────────────────────────────────────────────────────

sub install {
    my ( $self, $args ) = @_;
    $self->store_data({
        api_url      => 'http://127.0.0.1:8000',
        debug        => '0',
        typing_delay => '500',
        enabled      => '1',
    });
    return 1;
}

sub upgrade {
    my ( $self, $args ) = @_;
    # Future: add data-migration logic here when the schema changes.
    return 1;
}

sub uninstall {
    my ( $self, $args ) = @_;
    return 1;
}

# ─── Admin Configuration Page ───────────────────────────────────────────────────

sub configure {
    my ( $self, $args ) = @_;
    my $cgi = $self->{cgi};

    # Save posted settings
    if ( scalar $cgi->param('save') ) {
        my $api_url = scalar $cgi->param('api_url') || 'http://127.0.0.1:8000';
        $api_url =~ s{/+$}{};    # strip trailing slash

        $self->store_data({
            api_url      => $api_url,
            debug        => ( scalar $cgi->param('debug')   ? '1' : '0' ),
            typing_delay => ( scalar $cgi->param('typing_delay') || '500' ),
            enabled      => ( scalar $cgi->param('enabled') ? '1' : '0' ),
        });
    }

    # Read current values
    my $api_url      = $self->retrieve_data('api_url')      || 'http://127.0.0.1:8000';
    my $debug        = $self->retrieve_data('debug')        // '0';
    my $typing_delay = $self->retrieve_data('typing_delay') || '500';
    my $enabled      = $self->retrieve_data('enabled')      // '1';

    my $plugin_path  = $self->get_plugin_http_path();
    my $self_url     = $self->{cgi}->url( -absolute => 1 );

    my $checked_enabled = $enabled      ? 'checked' : '';
    my $checked_debug   = $debug        ? 'checked' : '';

    # Print the configuration page (no external template needed)
    print $cgi->header( -charset => 'utf-8' );
    print <<HTML;
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>OPAC AI Assistant — Configuration</title>
  <link rel="stylesheet" href="/intranet-tmpl/prog/css/staff-global.css">
  <style>
    body { font-family: system-ui, sans-serif; background: #f5f5f5; }
    .ai-config { max-width: 680px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,.08); padding: 32px 36px; }
    .ai-config h1 { font-size: 1.4rem; margin: 0 0 6px; color: #1a1a2e; }
    .ai-config .subtitle { color: #666; font-size: .9rem; margin-bottom: 28px; }
    .field { margin-bottom: 22px; }
    .field label { display: block; font-weight: 600; margin-bottom: 6px; color: #333; font-size: .92rem; }
    .field input[type=text], .field input[type=number] { width: 100%; padding: 9px 12px; border: 1.5px solid #ddd; border-radius: 6px; font-size: .95rem; box-sizing: border-box; transition: border .2s; }
    .field input[type=text]:focus, .field input[type=number]:focus { border-color: #4361ee; outline: none; }
    .field .hint { font-size: .8rem; color: #888; margin-top: 4px; }
    .toggle-row { display: flex; align-items: center; gap: 10px; }
    .toggle-row label { margin: 0; font-weight: 600; color: #333; font-size: .92rem; }
    .btn-save { background: #4361ee; color: #fff; border: none; padding: 11px 28px; border-radius: 7px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: background .2s; }
    .btn-save:hover { background: #3451d1; }
    .badge { display: inline-block; background: #e8f4fd; color: #1565c0; border-radius: 4px; padding: 2px 8px; font-size: .75rem; font-weight: 600; margin-left: 8px; }
    hr { border: none; border-top: 1px solid #eee; margin: 28px 0; }
    .status-box { background: #f0fdf4; border-left: 4px solid #22c55e; padding: 10px 14px; border-radius: 4px; font-size: .88rem; color: #166534; margin-bottom: 20px; }
  </style>
</head>
<body>
<div class="ai-config">
  <h1>&#129302; OPAC AI Assistant <span class="badge">v2.0.0</span></h1>
  <p class="subtitle">Configure the AI chatbot injected into every Koha OPAC page.</p>

  <form method="post" action="$self_url">
    <input type="hidden" name="class"  value="Koha::Plugin::OPACChatBot">
    <input type="hidden" name="method" value="configure">

    <div class="field">
      <div class="toggle-row">
        <input type="checkbox" id="enabled" name="enabled" value="1" $checked_enabled>
        <label for="enabled">Enable OPAC AI Assistant</label>
      </div>
      <p class="hint">Uncheck to hide the chatbot from all OPAC pages without uninstalling.</p>
    </div>

    <hr>

    <div class="field">
      <label for="api_url">Backend API URL</label>
      <input type="text" id="api_url" name="api_url" value="$api_url" placeholder="http://127.0.0.1:8000">
      <p class="hint">The FastAPI server URL. Include protocol and port, no trailing slash. Example: <code>http://192.168.1.10:8000</code></p>
    </div>

    <div class="field">
      <label for="typing_delay">Typing Simulation Delay (ms)</label>
      <input type="number" id="typing_delay" name="typing_delay" value="$typing_delay" min="0" max="3000" step="50">
      <p class="hint">Milliseconds the bot "thinks" before replying. Set to 0 to disable. Recommended: 400–600.</p>
    </div>

    <div class="field">
      <div class="toggle-row">
        <input type="checkbox" id="debug" name="debug" value="1" $checked_debug>
        <label for="debug">Enable Debug Mode</label>
      </div>
      <p class="hint">Logs API calls and errors to the browser console. Disable in production.</p>
    </div>

    <button type="submit" name="save" value="1" class="btn-save">&#10003; Save Settings</button>
  </form>

  <hr>
  <p style="font-size:.8rem;color:#999;text-align:center;">
    OPAC AI Assistant &mdash; by <a href="https://github.com/justatech-sleepy" target="_blank">Hasnat Khan</a>
  </p>
</div>
</body>
</html>
HTML
}

# ─── OPAC Injection: CSS ────────────────────────────────────────────────────────

sub opac_head {
    my ($self) = @_;

    return '' unless ( $self->retrieve_data('enabled') // '1' );

    my $p = $self->get_plugin_http_path();

    return <<HTML;
<!-- OPAC AI Assistant: CSS -->
<link rel="stylesheet" href="$p/css/variables.css">
<link rel="stylesheet" href="$p/css/animations.css">
<link rel="stylesheet" href="$p/css/theme.css">
<link rel="stylesheet" href="$p/css/components.css">
<link rel="stylesheet" href="$p/css/chatbot.css">
<link rel="stylesheet" href="$p/css/responsive.css">
<!-- End OPAC AI Assistant: CSS -->
HTML
}

# ─── OPAC Injection: JavaScript ─────────────────────────────────────────────────

sub opac_js {
    my ($self) = @_;

    return '' unless ( $self->retrieve_data('enabled') // '1' );

    my $p     = $self->get_plugin_http_path();
    my $api   = $self->retrieve_data('api_url')      || 'http://127.0.0.1:8000';
    my $debug = $self->retrieve_data('debug')        || '0';
    my $delay = $self->retrieve_data('typing_delay') || '500';

    # Sanitise values before embedding in HTML
    $api   =~ s/[<>"']//g;
    $debug = $debug ? 'true' : 'false';
    $delay =~ s/[^0-9]//g;

    return <<JS;
<!-- OPAC AI Assistant: JS -->
<script>
  window.KohaChatPlugin                   = window.KohaChatPlugin || {};
  window.KohaChatPlugin.API_BASE_URL      = "$api/api/chat";
  window.KohaChatPlugin.LOGO_URL          = "$p/assets/logo.svg";
  window.KohaChatPlugin.PLUGIN_PATH       = "$p";
  window.KohaChatPlugin._overrideDebug    = $debug;
  window.KohaChatPlugin._overrideDelay    = $delay;
</script>
<script src="$p/js/icons.js"></script>
<script src="$p/js/config.js"></script>
<script src="$p/js/utils.js"></script>
<script src="$p/js/ui.js"></script>
<script src="$p/js/faq.js"></script>
<script src="$p/js/knowledgeBase.js"></script>
<script src="$p/js/intentEngine.js"></script>
<script src="$p/js/chatController.js"></script>
<script src="$p/js/api.js"></script>
<script src="$p/js/app.js"></script>
<!-- End OPAC AI Assistant: JS -->
JS
}

1;
