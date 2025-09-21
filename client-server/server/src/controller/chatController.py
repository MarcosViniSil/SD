
from fastapi import APIRouter,Depends,Path
from src.models.dependencies import getChatService, getNickNameService
from src.service.chatService import ChatService
from typing import Annotated

routerChat = APIRouter()

@routerChat.get("/test")
async def test(chatService: ChatService = Depends(getChatService)):
    return chatService.test()
