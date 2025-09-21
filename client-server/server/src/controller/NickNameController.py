from fastapi import APIRouter,Depends,Path
from src.service.NickNameService import NickNameService
from src.models.dependencies import getNickNameService

routerNickName = APIRouter()

@routerNickName.post("/nick/{name}")
async def createNickName(name: str,nickNameService: NickNameService = Depends(getNickNameService)):
    return nickNameService.registerNickName(name)