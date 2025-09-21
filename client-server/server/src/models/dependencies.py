from src.service.RoomService import RoomService
from src.service.NickNameService import NickNameService
from  src.db.connection import ConnectionDB
from src.repository.chatRepository import ChatRepository
from src.service.chatService import ChatService

db = ConnectionDB()
chatRepository = ChatRepository(db)

chatService = ChatService(chatRepository)
nickNameService = NickNameService(chatRepository)
roomService = RoomService(chatRepository)

def getChatService():
    return chatService

def getNickNameService():
    return nickNameService

def getRoomService():
    return roomService