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
},

async suggest(query){
const response=await fetch(
`${CONFIG.API_URL.replace("/chat", "")}/suggestions?q=${encodeURIComponent(query)}`
);
if(!response.ok){
return {suggestions:[]};
}
return await response.json();
}
};
