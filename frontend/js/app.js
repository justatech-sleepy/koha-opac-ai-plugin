document.addEventListener("DOMContentLoaded", () => {
  window.KohaChatPlugin.createChatUI();

  const toggle = document.getElementById("koha-chat-toggle");
  const chat = document.getElementById("koha-chat-window");
  const input = document.getElementById("koha-chat-message-input");

  toggle.onclick = () => {
    const isFlex = chat.style.display === "flex";
    chat.style.display = isFlex ? "none" : "flex";
    toggle.setAttribute("aria-expanded", !isFlex);
    chat.setAttribute("aria-hidden", isFlex.toString());
    if (!isFlex) {
      input.focus();
    } else {
      toggle.focus();
    }
  };

  document.addEventListener("keydown", (e) => {
    if (chat.style.display === "flex") {
      if (e.key === "Escape") {
        chat.style.display = "none";
        toggle.setAttribute("aria-expanded", "false");
        chat.setAttribute("aria-hidden", "true");
        toggle.focus();
      } else if (e.key === "Tab") {
        const focusableElements = chat.querySelectorAll(
          'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    }
  });

  window.KohaChatPlugin.addMessage("bot", window.KohaChatPlugin.CONFIG.WELCOME_MESSAGE);

  async function send(textValue) {
    const text = textValue !== undefined ? textValue : input.value.trim();
    if (text === "") return;

    window.KohaChatPlugin.addMessage("user", window.KohaChatPlugin.escapeHTML(text));
    input.value = "";

    document.getElementById("koha-chat-messages").insertAdjacentHTML("beforeend", window.KohaChatPlugin.createSkeleton());
    window.KohaChatPlugin.scrollToBottom();

    await window.KohaChatPlugin.sleep(window.KohaChatPlugin.CONFIG.TYPING_DELAY);

    try {
      const local = window.KohaChatPlugin.localIntent(text);
      window.KohaChatPlugin.removeSkeleton();

      if (local.type === "window.KohaChatPlugin.FAQ") {
        window.KohaChatPlugin.addMessage("bot", local.answer);
        return;
      }

      const result = await window.KohaChatPlugin.API.chat(text);
      window.KohaChatPlugin.addMessage("bot", result.response);
    } catch (e) {
      window.KohaChatPlugin.removeSkeleton();
      if (window.KohaChatPlugin.CONFIG.DEBUG) {
        console.error(e);
      }
      // Assuming addMessage acts as showNotification for the chat context
      window.KohaChatPlugin.addMessage("bot", "Unable to contact the library service.");
    }
  }

  document.getElementById("koha-chat-send-btn").onclick = () => send();
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      send();
    }
  });

  const suggestionsBox = document.getElementById("koha-chat-suggestions-box");

  const handleInput = window.KohaChatPlugin.debounce(async (e) => {
    const query = e.target.value.trim();
    if (query.length < 3) {
      suggestionsBox.style.display = "none";
      return;
    }

    try {
      const data = await window.KohaChatPlugin.API.suggest(query);
      if (data.suggestions && data.suggestions.length > 0) {
        suggestionsBox.innerHTML = data.suggestions.map(s => `<div class="suggestion-item" tabindex="0" role="option">${window.KohaChatPlugin.escapeHTML(s)}</div>`).join('');
        suggestionsBox.style.display = "block";

        document.querySelectorAll('.suggestion-item').forEach(item => {
          item.onclick = () => {
            input.value = item.textContent;
            suggestionsBox.style.display = "none";
            input.focus();
          };
          item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
              input.value = item.textContent;
              suggestionsBox.style.display = "none";
              input.focus();
            }
          });
        });
      } else {
        suggestionsBox.style.display = "none";
      }
    } catch (err) {
      if (window.KohaChatPlugin.CONFIG.DEBUG) {
        console.error(err);
      }
    }
  }, 300);

  input.addEventListener("input", handleInput);

  document.addEventListener("click", (e) => {
    if (e.target !== input && e.target !== suggestionsBox) {
      suggestionsBox.style.display = "none";
    }
  });

  // Event Delegation for quick action buttons
  const chatMessages = document.getElementById('koha-chat-messages');
  chatMessages.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action="quick-search"]');
    if (btn) {
      const query = btn.getAttribute('data-query');
      if (query) {
        input.value = query;
        send(query);
      }
    }
  });

  // Image load event delegation (capturing phase)
  chatMessages.addEventListener('load', (e) => {
    if (e.target.tagName === 'IMG' && e.target.closest('.book-cover')) {
      e.target.classList.add('loaded');
      e.target.parentElement.classList.add('has-loaded-img');
    }
  }, true);

  // MutationObserver for newly added book covers
  const observer = new MutationObserver(mutations => {
    mutations.forEach(m => {
      m.addedNodes.forEach(n => {
        if (n.nodeType === 1) {
          const imgs = n.querySelectorAll ? n.querySelectorAll('.book-cover img:not(.processed)') : [];
          imgs.forEach(img => {
            img.classList.add('processed');
            if (img.complete) {
              img.classList.add('loaded');
              img.parentElement.classList.add('has-loaded-img');
            }
          });
          if (n.tagName === 'IMG' && n.closest('.book-cover') && !n.classList.contains('processed')) {
            n.classList.add('processed');
            if (n.complete) {
              n.classList.add('loaded');
              n.parentElement.classList.add('has-loaded-img');
            }
          }
        }
      });
    });
  });
  observer.observe(chatMessages, { childList: true, subtree: true });

});
