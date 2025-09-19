
from fastapi import APIRouter,Depends
from src.models.dependencies import getChatService
from src.service.chatService import ChatService

routerChat = APIRouter()

@routerChat.get("/test")
async def test(chatService: ChatService = Depends(getChatService)):
    return chatService.test()