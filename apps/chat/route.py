from fastapi import APIRouter, HTTPException, Request
from schema import ChatRequest
from .utils import process_chat

router = APIRouter()

@router.post("/ask")
async def ask_question(chat_request: ChatRequest, request: Request):
    try:
        response = await process_chat(chat_request, request)
        return {"message": "AI Response", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))