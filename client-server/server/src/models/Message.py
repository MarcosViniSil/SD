from pydantic import BaseModel


class Message(BaseModel):
    message: str
    nickName: str 
    messageDate: str
    messageId: str