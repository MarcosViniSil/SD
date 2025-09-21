from datetime import datetime,timezone
from src.models.Message import Message
from src.models.Interaction import Interaction
from src.repository.chatRepository import ChatRepository
from fastapi import HTTPException, status,Response
import logging
import time,random

class ChatService:

    def __init__(self,chatRepository:ChatRepository):
        self.chatRepository = chatRepository
    
    def registerMessage(self,roomId:int,interaction : Interaction) -> dict:
        logging.info(f"Requisição do tipo POST recebida para criação de uma interação")
        
        start_time = time.perf_counter()

        self.verifyLengthMessage(interaction.message)
        self.isValidTimesTamp(interaction.timestampClient)

        self.callVerifyRoomExists(roomId)
        
        nickNameId = self.callVerifyIfNickNameExists(interaction.nickName)
        if nickNameId == -1:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="O nickName não existe")
        
        self.callVerifyIdemKey(interaction.idemKey)

        self.callCreateInteraction(interaction,nickNameId,roomId)

        end_time = time.perf_counter()
        operationTime = str(round((end_time - start_time)*1000,2))
        
        logging.info(f"Latência: {operationTime}ms")

        return {"content":"Mensagem salva com sucesso"}

    def callGetMessages(self,timesTamp:int,roomId:int,lastId:int,limit:int) -> dict:
        time.sleep(10)
        logging.info(f"Requisição do tipo GET recebida para leitura das mensagens")
        
        start_time = time.perf_counter()
        self.callVerifyRoomExists(roomId)

        rows = self.tryOperation(method=self.getMessages, timesTamp=timesTamp,roomId=roomId,lastId=lastId,limit=limit)
        data =  self.convertDictToArray(rows)
        
        end_time = time.perf_counter()
        operationTime = str(round((end_time - start_time)*1000,2))
        
        logging.info(f"Latência: {operationTime}ms")

        return data

    def getMessages(self,timesTamp:int,roomId:int,lastId:int,limit:int) -> Message:
        try:
            return self.chatRepository.getMessages(timesTamp,lastId,roomId,limit)
        except Exception as e:
            logging.error(f"O seguinte erro ocorreu na tentativa de obter as mensagens do chat {e}")

    def callVerifyRoomExists(self,roomId:int) -> None:
        self.tryOperation(method=self.verifyIfRoomExists, roomId=roomId)

    def callVerifyIfNickNameExists(self,nickName:str) -> int:
        return self.tryOperation(method=self.verifyIfNickNameExists, nickName=nickName)

    def callVerifyIdemKey(self,idemKey:str) -> None:
        self.tryOperation(method=self.verifyIdemKey, idemKey=idemKey)

    def callCreateInteraction(self,interaction : Interaction,nickNameId:int,roomId:int) -> None:
        self.tryOperation(method=self.createInteraction, interaction=interaction,nickNameId=nickNameId,roomId=roomId)

    def createInteraction(self,interaction : Interaction,nickNameId:int,roomId:int) -> None:
        timesTamp = int(time.time() * 1000)
        self.chatRepository.createInteraction(interaction,nickNameId,roomId,timesTamp)

    def verifyIdemKey(self,idemKey:str) -> None:
        if self.chatRepository.isIdemKeyAlreadyExists(idemKey):
            raise HTTPException(status_code=status.HTTP_200_OK,detail="Mensagem salva com sucesso")
    
    def verifyIfNickNameExists(self,nickName:str) -> None:
        nickNameId = self.chatRepository.getNickNameId(nickName)
        if nickNameId is None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="O nickName não existe")
        return nickNameId

    def verifyIfRoomExists(self,roomId:int) -> None:
        if not self.chatRepository.isRoomExists(roomId):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="A sala informada não existe")

    def convertDictToArray(self,data:dict) -> dict:
        try:
            result = []
            for row in data:
                print(row)
                message = row[0]
                nickName = row[1]
                messageDate = row[2]
                messageId = row[3]
                lastTimesTamp = row[4]
                if row is not None and message is not None and nickName is not None and messageDate is not None and messageId is not None:
                    result.append({
                        "message":message,
                        "nickName":nickName,
                        "date":self.convertTimesTampToDate(messageDate),
                        "messageId":messageId,
                        "timesTamp":lastTimesTamp
                    })
            return result
        except Exception as e:
            logging.error(f"O seguinte erro ocorreu na tentativa de converter mensagens do chat para o uma lista de dict: {e}")   
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Ocorreu um erro ao realzizar operação, tente novamente")

    def tryOperation(self,method = None,*args, **kwargs) -> None:
        try:
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logging.error(f"ao tentar executar o método {method} o seguinte erro ocorreu {e}")   
    
    def calculateJitter(self,attempt:int) -> float:
        wait_time = (0.5 * (attempt + 1))  
        jitter = random.uniform(0.8, 1.2)
        sleep_for = wait_time * jitter
        return sleep_for
    
    def handleMessageFail(self,max_retries:int):
        logging.error(f"Falha ao tentar ler/inserir mensagem após {max_retries} tentativas")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Após algumas tentativas não foi possível executar a operação.Tente novamente")
    
    def verifyLengthMessage(self, message:str) -> None:
        if len(message.strip()) == 0 or len(message) < 3 or len(message) > 200:
            logging.error(f"A mensagem {message} é inválida por conta do seu tamanho")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Mensagens devem conter no mínimo 3 e no máximo 200 caracteres")

    def isValidTimesTamp(self,value, milliseconds=False):
        try:
            ts = float(value)
            if milliseconds:
                ts /= 1000 
            datetime.fromtimestamp(ts, tz=timezone.utc)
            return True
        except (ValueError, OSError, OverflowError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"O timestamp informado não é válido")
        
    def convertTimesTampToDate(self,timesTamp:int) -> str:
        self.isValidTimesTamp(timesTamp)
        timesTamp = float(timesTamp)
        date = datetime.fromtimestamp(timesTamp / 1e3)
        print(date.strftime("%d/%m/%Y %H:%M"))
        return date.strftime("%d/%m/%Y %H:%M")