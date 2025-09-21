from pydantic import BaseModel


class Interaction(BaseModel):
    idemKey: str
    message: str 
    nickName: str
    timestampClient: str