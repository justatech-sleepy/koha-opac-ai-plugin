window.KohaChatPlugin = window.KohaChatPlugin || {};
window.KohaChatPlugin.API = {

async chat(message){
  // Check if Gemini Demo Mode is enabled
  if (window.KohaChatPlugin.GEMINI_MODE == 1 && window.KohaChatPlugin.GEMINI_KEY) {
    try {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${window.KohaChatPlugin.GEMINI_KEY}`;
      const geminiResponse = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: "You are a helpful library assistant for COMSATS University Library. Keep answers brief and professional. User says: " + message }] }]
        })
      });
      
      if (!geminiResponse.ok) throw new Error("Gemini API Error");
      
      const data = await geminiResponse.json();
      const answerText = data.candidates?.[0]?.content?.parts?.[0]?.text || "Sorry, I couldn't process that.";
      
      // Return in the format expected by the frontend UI
      return { response: answerText };
    } catch (e) {
      console.error(e);
      return { response: "Oops! The Gemini demo is currently unavailable. Please try again later." };
    }
  }

  // Fallback to standard FastAPI Backend
  const response=await fetch(
    window.KohaChatPlugin.CONFIG.API_URL,
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
`${window.KohaChatPlugin.CONFIG.API_URL.replace("/chat", "")}/suggestions?q=${encodeURIComponent(query)}`
);
if(!response.ok){
return {suggestions:[]};
}
return await response.json();
}
};
