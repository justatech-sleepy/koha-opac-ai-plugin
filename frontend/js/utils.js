function escapeHTML(text){

const div=document.createElement("div");

div.textContent=text;

return div.innerHTML;

}

function scrollToBottom(){

const box=document.getElementById("chatMessages");

if(!box) return;

box.scrollTop=box.scrollHeight;

}

function currentTime(){

return new Date().toLocaleTimeString([],{

hour:"2-digit",

minute:"2-digit"

});

}

function createTyping(){

return `
<div class="message bot typing-message">

<div class="bubble">

<div class="typing">

<span></span>

<span></span>

<span></span>

</div>

</div>

</div>
`;

}

function removeTyping(){

const typing=document.querySelector(".typing-message");

if(typing){

typing.remove();

}

}

function sleep(ms){

return new Promise(resolve=>setTimeout(resolve,ms));

}
