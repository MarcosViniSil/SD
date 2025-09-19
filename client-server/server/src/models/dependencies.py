from  src.db.connection import ConnectionDB
from src.repository.chatRepository import ChatRepository
from src.service.chatService import ChatService

db = ConnectionDB()
chatRepository = ChatRepository(db)

chatService = ChatService(chatRepository)

def getChatService():
    return chatService