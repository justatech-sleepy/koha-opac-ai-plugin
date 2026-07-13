const API={

async chat(message){

const response=await fetch(

CONFIG.API_URL,

{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

message:message

})

}

);

if(!response.ok){

throw new Error("Server Error");

}

return await response.json();

}

};
