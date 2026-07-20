window.KohaChatPlugin = window.KohaChatPlugin || {};
window.KohaChatPlugin.CONFIG = {
  APP_NAME: "Liberty AI",
  VERSION: "2.0.0",
  API_URL: window.KohaChatPlugin.API_BASE_URL || "http://127.0.0.1:8000/api/chat",
  LOGO_URL: window.KohaChatPlugin.LOGO_URL || "data:image/svg+xml;utf8,<svg width='44' height='44' viewBox='0 0 64 64' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M18 14C18 12.9 18.9 12 20 12H46C47.1 12 48 12.9 48 14V46C48 47.1 47.1 48 46 48H20C18.9 48 18 47.1 18 46V14Z' fill='%234F46E5'/><path d='M24 18H42' stroke='white' stroke-width='2.5' stroke-linecap='round'/><path d='M24 25H42' stroke='white' stroke-width='2.5' stroke-linecap='round'/><path d='M24 32H38' stroke='white' stroke-width='2.5' stroke-linecap='round'/><path d='M18 16C14 16 12 18 12 22V46C12 50 14 52 18 52H46' stroke='%233730A3' stroke-width='2.5' stroke-linecap='round'/></svg>",
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
