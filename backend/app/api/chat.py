from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse

from app.intents.engine import IntentEngine

router = APIRouter()

engine = IntentEngine()

@router.post("/chat", response_model=ChatResponse)

def chat(request: ChatRequest):

    result = engine.detect(request.message)

    return ChatResponse(**result)
