
from src.repository.chatRepository import ChatRepository


class ChatService:

    def __init__(self,chatRepository:ChatRepository):
        self.chatRepository = chatRepository

    def test(self):
        return "teste"