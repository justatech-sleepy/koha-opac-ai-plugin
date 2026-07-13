function createChatUI() {
  document.body.insertAdjacentHTML("beforeend", `
    <button id="koha-chat-toggle" aria-label="Open Library Assistant" aria-expanded="false" aria-controls="koha-chat-window" tabindex="0">
      <span class="toggle-icon">${ICONS.chat}</span>
    </button>
    <div id="koha-chat-window" role="dialog" aria-modal="false" aria-labelledby="chat-title" aria-hidden="true">
      <div id="koha-chat-header">
        <div class="header-left">
          <img src="/opac-tmpl/bootstrap/logo.svg" class="header-logo" alt="Library Logo">
          <div class="header-info">
            <h2 class="title" id="chat-title">${CONFIG.APP_NAME}</h2>
            <div class="subtitle">Digital Library Assistant</div>
            <div class="status" aria-live="polite">
              <span class="status-dot"></span>
              <span class="status-text">Online</span>
            </div>
          </div>
        </div>
        <button id="closeChatBtn" aria-label="Close Assistant" tabindex="0">
          ${ICONS.close}
        </button>
      </div>
      <div id="chatMessages" aria-live="polite" role="log" tabindex="0"></div>
      <div id="chatInputArea">
        <div id="suggestions-box" class="suggestions-dropdown" style="display:none;" role="listbox"></div>
        <input id="messageInput" placeholder="Search books, authors, ISBN..." autocomplete="off" aria-label="Search query" tabindex="0">
        <button id="sendBtn" aria-label="Send message" tabindex="0">
          ${ICONS.send}
        </button>
      </div>
    </div>
  `);

  document.getElementById("closeChatBtn").onclick = () => {
    const windowEl = document.getElementById("koha-chat-window");
    const toggleEl = document.getElementById("koha-chat-toggle");
    windowEl.style.display = "none";
    windowEl.setAttribute("aria-hidden", "true");
    toggleEl.setAttribute("aria-expanded", "false");
    toggleEl.focus();
  };
}
