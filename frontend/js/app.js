document.addEventListener("DOMContentLoaded",()=>{

createChatUI();

const toggle=document.getElementById("koha-chat-toggle");

const chat=document.getElementById("koha-chat-window");

const input=document.getElementById("messageInput");

toggle.onclick=()=>{

chat.style.display=

chat.style.display==="flex"

?"none"

:"flex";

if(chat.style.display==="flex"){

input.focus();

}

};

addMessage("bot",CONFIG.WELCOME_MESSAGE);

async function send(){

const text=input.value.trim();

if(text==="") return;

addMessage("user",escapeHTML(text));

input.value="";

document

.getElementById("chatMessages")

.insertAdjacentHTML(

"beforeend",

createTyping()

);

scrollToBottom();

await sleep(CONFIG.TYPING_DELAY);

try{

const local=localIntent(text);

removeTyping();

if(local.type==="FAQ"){

addMessage("bot",local.answer);

return;

}

const result=await API.chat(text);

addMessage("bot",result.response);

}

catch(e){

removeTyping();

addMessage(

"bot",

"Unable to connect to server."

);

}

}

document

.getElementById("sendBtn")

.onclick=send;

input.addEventListener(

"keydown",

e=>{

if(e.key==="Enter"){

e.preventDefault();

send();

}

}

);

});
