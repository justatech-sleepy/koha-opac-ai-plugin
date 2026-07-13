function addMessage(type,message){

const messages=document.getElementById("chatMessages");

const row=document.createElement("div");

row.className="message "+type;

const bubble=document.createElement("div");

bubble.className="bubble";

bubble.innerHTML=message;

const time=document.createElement("div");

time.className="message-time";

time.innerText=currentTime();

bubble.appendChild(time);

row.appendChild(bubble);

messages.appendChild(row);

scrollToBottom();

}
