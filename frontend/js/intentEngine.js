window.KohaChatPlugin.localIntent = function window.KohaChatPlugin.localIntent(message){

const text=message.toLowerCase().trim();

if(

text.includes("hour")||

text.includes("time")||

text.includes("open")||

text.includes("close")

){

return{

type:"window.KohaChatPlugin.FAQ",

answer:window.KohaChatPlugin.KNOWLEDGE.library.hours

};

}

if(

text.includes("membership")||

text.includes("member")

){

return{

type:"window.KohaChatPlugin.FAQ",

answer:window.KohaChatPlugin.KNOWLEDGE.library.membership

};

}

for(const item of window.KohaChatPlugin.FAQ){

if(text.includes(item.question)){

return{

type:"window.KohaChatPlugin.FAQ",

answer:item.answer

};

}

}

return{

type:"SERVER"

};

}
