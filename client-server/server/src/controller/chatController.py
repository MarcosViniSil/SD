
from fastapi import APIRouter,Depends,Form
from src.models.Interaction import Interaction
from src.models.dependencies import getChatService, getNickNameService
from src.service.chatService import ChatService
from typing import Annotated

routerChat = APIRouter()

@routerChat.post("/groups/{id}/messages")
async def test(id: int,interaction : Interaction,chatService: ChatService = Depends(getChatService)):
    return chatService.registerMessage(id,interaction)


@routerChat.get("/groups/{id}/messages")
async def test(timesTamp:int, roomId:int,lastId:int,limit:int,chatService: ChatService = Depends(getChatService)):
    return chatService.callGetMessages(timesTamp,roomId,lastId,limit)
