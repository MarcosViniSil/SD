from fastapi import APIRouter,Depends,Path
from src.service.RoomService import RoomService
from src.models.dependencies import getRoomService

routerRoomName = APIRouter()

@routerRoomName.post("/groups/{name}")
async def test(name: str,roomService: RoomService = Depends(getRoomService)):
    return roomService.registerRoomName(name)

@routerRoomName.get("/groups")
async def test(roomService: RoomService = Depends(getRoomService)):
    return roomService.getRoomNames()