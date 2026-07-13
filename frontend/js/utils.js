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

function createSkeleton() {
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

function removeSkeleton() {
  const skeleton = document.querySelector(".skeleton-message");
  if (skeleton) {
    skeleton.remove();
  }
}

function sleep(ms){
return new Promise(resolve=>setTimeout(resolve,ms));
}

function debounce(func, wait) {
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
