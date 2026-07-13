document.addEventListener("DOMContentLoaded", () => {
  createChatUI();

  const toggle = document.getElementById("koha-chat-toggle");
  const chat = document.getElementById("koha-chat-window");
  const input = document.getElementById("messageInput");

  toggle.onclick = () => {
    const isFlex = chat.style.display === "flex";
    chat.style.display = isFlex ? "none" : "flex";
    toggle.setAttribute("aria-expanded", !isFlex);
    chat.setAttribute("aria-hidden", isFlex.toString());
    if (!isFlex) {
      input.focus();
    }
  };

  addMessage("bot", CONFIG.WELCOME_MESSAGE);

  async function send(textValue) {
    const text = textValue !== undefined ? textValue : input.value.trim();
    if (text === "") return;

    addMessage("user", escapeHTML(text));
    input.value = "";

    document.getElementById("chatMessages").insertAdjacentHTML("beforeend", createSkeleton());
    scrollToBottom();

    await sleep(CONFIG.TYPING_DELAY);

    try {
      const local = localIntent(text);
      removeSkeleton();

      if (local.type === "FAQ") {
        addMessage("bot", local.answer);
        return;
      }

      const result = await API.chat(text);
      addMessage("bot", result.response);
    } catch (e) {
      removeSkeleton();
      addMessage("bot", "Unable to connect to server.");
    }
  }

  document.getElementById("sendBtn").onclick = () => send();
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      send();
    }
  });

  const suggestionsBox = document.getElementById("suggestions-box");

  const handleInput = debounce(async (e) => {
    const query = e.target.value.trim();
    if (query.length < 3) {
      suggestionsBox.style.display = "none";
      return;
    }

    try {
      const data = await API.suggest(query);
      if (data.suggestions && data.suggestions.length > 0) {
        suggestionsBox.innerHTML = data.suggestions.map(s => `<div class="suggestion-item" tabindex="0" role="option">${escapeHTML(s)}</div>`).join('');
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
      console.error(err);
    }
  }, 300);

  input.addEventListener("input", handleInput);

  document.addEventListener("click", (e) => {
    if (e.target !== input && e.target !== suggestionsBox) {
      suggestionsBox.style.display = "none";
    }
  });

  // Event Delegation for quick action buttons
  document.getElementById('chatMessages').addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action="quick-search"]');
    if (btn) {
      const query = btn.getAttribute('data-query');
      if (query) {
        input.value = query;
        send(query);
      }
    }
  });

});
