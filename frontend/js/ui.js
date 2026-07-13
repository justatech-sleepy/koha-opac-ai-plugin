function createChatUI(){

document.body.insertAdjacentHTML("beforeend",`

<button id="koha-chat-toggle">

<img
src="/opac-tmpl/bootstrap/logo.svg"
class="assistant-logo"
alt="AI">

</button>

<div id="koha-chat-window">

<div id="koha-chat-header">

<div class="header-left">

<img
src="/opac-tmpl/bootstrap/logo.svg"
class="header-logo"
alt="AI">

<div>

<div class="title">

${CONFIG.APP_NAME}

</div>

<div class="subtitle">

Digital Library Assistant

</div>

</div>

</div>

<button id="closeChatBtn">

✕

</button>

</div>

<div id="chatMessages">

</div>

<div id="chatInputArea">

<input

id="messageInput"

placeholder="Search books, authors or ISBN..."

autocomplete="off"

>

<button id="sendBtn">

➜

</button>

</div>

</div>

`);

document

.getElementById("closeChatBtn")

.onclick=()=>{

document.getElementById("koha-chat-window").style.display="none";

};

}
