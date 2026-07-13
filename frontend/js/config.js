window.KohaChatPlugin = window.KohaChatPlugin || {};
window.KohaChatPlugin.CONFIG = {
  APP_NAME: "Liberty AI",
  VERSION: "2.0.0",
  API_URL: window.KohaChatPlugin.API_BASE_URL || "/api/chat",
  LOGO_URL: window.KohaChatPlugin.LOGO_URL || "/opac-tmpl/bootstrap/assets/logo.svg",
  DEBUG: false,
  SEARCH_LIMIT: 20,
  SUGGESTION_LIMIT: 7,
  REQUEST_TIMEOUT: 10000,
  MAX_HISTORY: 50,
  ENABLE_RECOMMENDATIONS: true,
  ENABLE_SUGGESTIONS: true,
  ENABLE_ANALYTICS: false,
  WELCOME_MESSAGE: `
    <div class="welcome-card">
      <div class="welcome-icon">
        ${window.KohaChatPlugin.ICONS.book}
      </div>
      <h2>Welcome to the Library</h2>
      <p>Search the catalog by title, author, ISBN, subject, or browse collections.</p>
      <div class="welcome-section-label">Quick searches</div>
      <div class="quick-actions">
        <button class="quick-btn" data-action="quick-search" data-query="Python books" tabindex="0">
          ${window.KohaChatPlugin.ICONS.search} Python Books
        </button>
        <button class="quick-btn" data-action="quick-search" data-query="Artificial Intelligence" tabindex="0">
          ${window.KohaChatPlugin.ICONS.search} Artificial Intelligence
        </button>
        <button class="quick-btn" data-action="quick-search" data-query="Machine Learning" tabindex="0">
          ${window.KohaChatPlugin.ICONS.search} Machine Learning
        </button>
        <button class="quick-btn" data-action="quick-search" data-query="Library Hours" tabindex="0">
          ${window.KohaChatPlugin.ICONS.clock} Library Hours
        </button>
        <button class="quick-btn" data-action="quick-search" data-query="Membership" tabindex="0">
          ${window.KohaChatPlugin.ICONS.user} Membership
        </button>
      </div>
      <div class="welcome-tips">
        <strong>Tips:</strong> Try "books by Eric Matthes", an ISBN like "9781593279288", or "publisher O'Reilly".
      </div>
    </div>
  `,
  TYPING_DELAY: 500,
  THEME: "light"
};
