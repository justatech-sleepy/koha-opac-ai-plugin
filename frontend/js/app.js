document.addEventListener("DOMContentLoaded", () => {
  // Load puter.js dynamically
  const puterScript = document.createElement("script");
  puterScript.src = "https://js.puter.com/v2/";
  document.head.appendChild(puterScript);

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

  const conversationHistory = [];

  async function send(textValue) {
    const text = textValue !== undefined ? textValue : input.value.trim();
    if (text === "") return;

    window.KohaChatPlugin.addMessage("user", window.KohaChatPlugin.escapeHTML(text));
    input.value = "";

    // Snapshot history BEFORE the current question — correct context for backend
    const historyToSend = [...conversationHistory];

    document.getElementById("koha-chat-messages").insertAdjacentHTML("beforeend", window.KohaChatPlugin.createSkeleton());
    window.KohaChatPlugin.scrollToBottom();

    // Capture element AFTER it is in the DOM
    const statusPhrases = [
        "Mining diamonds...",
        "Dusting off ancient tomes...",
        "Consulting the library archives...",
        "Decoding the scrolls...",
        "Searching the catalog...",
        "Connecting to knowledge base...",
        "Analyzing your request...",
        "Sifting through shelves...",
        "Brewing the answer...",
        "Unlocking the vault..."
    ];

    // Show first phrase immediately
    const statusTextEl = document.getElementById("koha-chat-status-text");
    if (statusTextEl) statusTextEl.innerText = statusPhrases[Math.floor(Math.random() * statusPhrases.length)];

    // Rotate phrases every 1.8s — re-query element each tick so it always finds it
    const statusInterval = setInterval(() => {
        const el = document.getElementById("koha-chat-status-text");
        if (el) el.innerText = statusPhrases[Math.floor(Math.random() * statusPhrases.length)];
    }, 1800);

    try {
      const local = window.KohaChatPlugin.localIntent(text);

      if (local.type === "FAQ") {
        clearInterval(statusInterval);
        window.KohaChatPlugin.removeSkeleton();
        window.KohaChatPlugin.addMessage("bot", local.answer);
        conversationHistory.push({ role: "user", content: text });
        conversationHistory.push({ role: "bot", content: local.answer });
        while (conversationHistory.length > 8) conversationHistory.shift();
        return;
      }

      const result = await window.KohaChatPlugin.API.chat(text, historyToSend);
      clearInterval(statusInterval);
      window.KohaChatPlugin.removeSkeleton();
      window.KohaChatPlugin.addMessage("bot", result.response);

      // Push user + bot AFTER we have the response — history is always in sync
      conversationHistory.push({ role: "user", content: text });
      if (result.raw_text) {
          let cleanText = result.raw_text.replace(/<thought>[\s\S]*?<\/thought>/gi, '').trim();
          conversationHistory.push({ role: "bot", content: cleanText });
      }
      while (conversationHistory.length > 8) conversationHistory.shift();
    } catch (e) {
      clearInterval(statusInterval);
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

  // --- VOICE AND VISION LOGIC ---
  const micBtn = document.getElementById("koha-chat-mic-btn");
  const cameraBtn = document.getElementById("koha-chat-camera-btn");
  const fileInput = document.getElementById("koha-chat-file-input");

  // Voice Input (Web Speech API as fallback, Puter if possible, but Web Speech is instant)
  let recognition;
  if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = function() {
      micBtn.classList.add("recording");
      input.placeholder = "Listening...";
    };
    
    recognition.onresult = function(event) {
      const text = event.results[0][0].transcript;
      input.value = text;
      send();
    };
    
    recognition.onerror = function(event) {
      console.error("Speech recognition error", event.error);
      micBtn.classList.remove("recording");
      input.placeholder = "Search books, authors, ISBN...";
    };
    
    recognition.onend = function() {
      micBtn.classList.remove("recording");
      input.placeholder = "Search books, authors, ISBN...";
    };
  }

  micBtn.onclick = () => {
    if (recognition) {
      recognition.start();
    } else {
      alert("Voice input is not supported in this browser.");
    }
  };

  // Vision Input (Camera)
  cameraBtn.onclick = () => {
    fileInput.click();
  };

  fileInput.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    input.value = "Scanning image...";
    input.disabled = true;
    cameraBtn.classList.add("scanning");

    try {
      // Use puter.js to extract text
      if (typeof puter !== 'undefined' && puter.ai) {
         const prompt = `Extract the main book title, author, ISBN, or Barcode from this image. If this image is clearly NOT a book, a barcode, or a library item, reply with the exact word 'NOT_A_BOOK'. Otherwise, only return the extracted text, nothing else.`;
         const text = await puter.ai.txt2txt(prompt, file);
         
         const cleanText = text.trim();
         
         if (cleanText.includes("NOT_A_BOOK")) {
            input.value = "";
            input.disabled = false;
            cameraBtn.classList.remove("scanning");
            window.KohaChatPlugin.addMessage("bot", "This image doesn't appear to be a book, barcode, or library item.");
            return;
         }
         
         input.value = cleanText;
         input.disabled = false;
         cameraBtn.classList.remove("scanning");
         send();
      } else {
         throw new Error("Puter is not loaded");
      }
    } catch (err) {
      console.error("Vision error:", err);
      input.value = "";
      input.disabled = false;
      cameraBtn.classList.remove("scanning");
      window.KohaChatPlugin.addMessage("bot", "Sorry, I couldn't read that image.");
    }
    fileInput.value = ""; // Reset
  };

  // Text-to-Speech Output
  window.KohaChatPlugin.speak = async function(text) {
    try {
      if (typeof puter !== 'undefined' && puter.ai) {
        const audio = await puter.ai.txt2speech(text);
        audio.play();
      } else {
        // Fallback to Web Speech API
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
      }
    } catch (e) {
      console.error("Speech error", e);
    }
  };
  // ------------------------------

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

  // Event Delegation for quick action buttons and backend results
  const chatMessages = document.getElementById('koha-chat-messages');
  chatMessages.addEventListener('click', (e) => {
    // Quick search buttons
    const btn = e.target.closest('[data-action="quick-search"]');
    if (btn) {
      const query = btn.getAttribute('data-query');
      if (query) {
        input.value = query;
        send(query);
      }
      return;
    }

    // Backend result buttons (View Details / Reserve)
    const actionEl = e.target.closest('button, a, .result-btn, [class*="btn"]');
    if (actionEl) {
      let id = actionEl.getAttribute('data-id') || actionEl.getAttribute('data-biblionumber');
      
      // Fallback: search the parent card's HTML for a biblionumber if it's missing on the button
      const card = actionEl.closest('.book-card, .book-result, .bubble');
      if (!id && card) {
        const match = card.innerHTML.match(/biblionumber=(\d+)/i) || card.innerHTML.match(/id=(\d+)/i);
        if (match) id = match[1];
      }

      const text = actionEl.textContent.toLowerCase();
      const isView = text.includes('view') || text.includes('detail') || text.includes('detil') || actionEl.getAttribute('data-action') === 'view';
      const isReserve = text.includes('reserve') || text.includes('reserce') || text.includes('place hold') || actionEl.getAttribute('data-action') === 'reserve';

      if (id) {
        if (isView) {
          e.preventDefault(); e.stopPropagation();
          window.location.href = `/cgi-bin/koha/opac-detail.pl?biblionumber=${id}`;
        } else if (isReserve) {
          e.preventDefault(); e.stopPropagation();
          window.location.href = `/cgi-bin/koha/opac-reserve.pl?biblionumber=${id}`;
        }
      } else if (card && (isView || isReserve)) {
        // THE BACKEND PROVIDED NO ID! Do an AJAX search to find the biblionumber instantly!
        const titleEl = card.querySelector('.book-title, h3, h2, h4, strong, .title');
        if (titleEl) {
           e.preventDefault(); e.stopPropagation();
           const originalText = actionEl.innerHTML;
           actionEl.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';
           actionEl.style.pointerEvents = 'none';
           actionEl.style.opacity = '0.7';
           
           const title = encodeURIComponent(titleEl.textContent.trim());
           const searchUrl = `/cgi-bin/koha/opac-search.pl?q=${title}`;
           
           const fetchPromise = fetch(searchUrl).then(res => res.text());
           const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 1500));
           
           Promise.race([fetchPromise, timeoutPromise])
             .then(html => {
                const doc = new DOMParser().parseFromString(html, 'text/html');
                const idInput = doc.querySelector('input[name="biblionumber"], a.title[href*="biblionumber="]');
                let foundId = null;
                if (idInput) {
                   if (idInput.tagName === 'INPUT') foundId = idInput.value;
                   else {
                      const m = idInput.href.match(/biblionumber=(\d+)/);
                      if (m) foundId = m[1];
                   }
                }
                if (foundId) {
                   window.location.href = isView ? `/cgi-bin/koha/opac-detail.pl?biblionumber=${foundId}` : `/cgi-bin/koha/opac-reserve.pl?biblionumber=${foundId}`;
                } else {
                   window.location.href = searchUrl;
                }
             })
             .catch(() => {
                window.location.href = searchUrl;
             });
        }
      }
    }
  }, true); // Use capturing phase for clicks to ensure we intercept before any backend inline scripts!

  // Image load event delegation (capturing phase)
  chatMessages.addEventListener('load', (e) => {
    if (e.target.tagName === 'IMG' && e.target.closest('.book-cover')) {
      if (e.target.naturalWidth <= 1) {
        // OpenLibrary returns 1x1 blank pixel for missing images!
        e.target.style.display = 'none';
      } else {
        e.target.classList.add('loaded');
      }
      e.target.parentElement.classList.add('has-loaded-img');
    }
  }, true);

  // Image error event delegation for broken covers
  chatMessages.addEventListener('error', (e) => {
    if (e.target.tagName === 'IMG' && e.target.closest('.book-cover')) {
      e.target.style.display = 'none'; // Hide broken image to show the generic SVG background
      e.target.parentElement.classList.add('has-loaded-img'); // Stop shimmering
    }
  }, true);

  // MutationObserver for newly added book covers
  const observer = new MutationObserver(mutations => {
    mutations.forEach(m => {
      m.addedNodes.forEach(n => {
        if (n.nodeType === 1) {
          
          // 0. Aggressively strip "disabled" attributes so demo buttons always work
          const disabledBtns = n.querySelectorAll ? n.querySelectorAll('button[disabled], .disabled, [disabled]') : [];
          disabledBtns.forEach(btn => {
            btn.removeAttribute('disabled');
            btn.classList.remove('disabled');
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
            btn.style.pointerEvents = 'auto';
          });
          if (n.hasAttribute && n.hasAttribute('disabled')) {
            n.removeAttribute('disabled');
            n.style.pointerEvents = 'auto';
          }

          // 0.5 Strip inline onerror handlers injected by backend that rely on external placeholders
          const badImgs = n.querySelectorAll ? n.querySelectorAll('img[onerror]') : [];
          badImgs.forEach(img => {
             img.removeAttribute('onerror');
             img.onerror = null;
          });
          if (n.hasAttribute && n.hasAttribute('onerror')) {
             n.removeAttribute('onerror');
             n.onerror = null;
          }

          // 1. Fix missing image tags completely (shimmer never stops otherwise)
          const covers = n.querySelectorAll ? n.querySelectorAll('.book-cover') : [];
          covers.forEach(cover => {
            if (!cover.querySelector('img')) {
              cover.classList.add('has-loaded-img');
            }
          });
          if (n.classList && n.classList.contains('book-cover') && !n.querySelector('img')) {
            n.classList.add('has-loaded-img');
          }

          // 2. Handle image tags that are present
          const imgs = n.querySelectorAll ? n.querySelectorAll('.book-cover img:not(.processed)') : [];
          imgs.forEach(img => {
            img.classList.add('processed');
            if (img.complete) {
              if (img.naturalWidth <= 1) { // Catch 1x1 pixels
                 img.style.display = 'none';
              } else {
                 img.classList.add('loaded');
              }
              img.parentElement.classList.add('has-loaded-img');
            }
          });
          
          if (n.tagName === 'IMG' && n.closest('.book-cover') && !n.classList.contains('processed')) {
            n.classList.add('processed');
            if (n.complete) {
              if (n.naturalWidth <= 1) {
                 n.style.display = 'none';
              } else {
                 n.classList.add('loaded');
              }
              n.parentElement.classList.add('has-loaded-img');
            }
          }
        }
      });
    });
  });
  observer.observe(chatMessages, { childList: true, subtree: true });

});
