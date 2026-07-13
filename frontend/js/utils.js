window.KohaChatPlugin.escapeHTML = function window.KohaChatPlugin.escapeHTML(text){

const div=document.createElement("div");

div.textContent=text;

return div.innerHTML;

}

window.KohaChatPlugin.scrollToBottom = function window.KohaChatPlugin.scrollToBottom(){

const box=document.getElementById("koha-chat-messages");

if(!box) return;

box.scrollTop=box.scrollHeight;

}

window.KohaChatPlugin.currentTime = function window.KohaChatPlugin.currentTime(){

return new Date().toLocaleTimeString([],{

hour:"2-digit",

minute:"2-digit"

});

}

window.KohaChatPlugin.createSkeleton = function window.KohaChatPlugin.createSkeleton() {
  return `
    <div class="message bot skeleton-message">
      <div class="loading-card" style="width: 260px;">
        <div class="loading-line"></div>
        <div class="loading-line"></div>
        <div class="loading-line"></div>
      </div>
    </div>
  `;
}

window.KohaChatPlugin.removeSkeleton = function window.KohaChatPlugin.removeSkeleton() {
  const skeleton = document.querySelector(".skeleton-message");
  if (skeleton) {
    skeleton.remove();
  }
}

window.KohaChatPlugin.sleep = function window.KohaChatPlugin.sleep(ms){
return new Promise(resolve=>setTimeout(resolve,ms));
}

window.KohaChatPlugin.debounce = function window.KohaChatPlugin.debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
