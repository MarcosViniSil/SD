import logging
import random
import time
from src.repository.chatRepository import ChatRepository
from fastapi import HTTPException, status

class RoomService:

    def __init__(self,chatRepository:ChatRepository):
        self.chatRepository = chatRepository;


    def registerRoomName(self,roomName:str) -> dict:
        logging.info(f"Requisição do tipo POST recebida para criação de uma sala de nome {roomName}")

        start_time = time.perf_counter()
        
        self.verifyLength(roomName)

        self.handleInsertRoomName(roomName)

        end_time = time.perf_counter()
        operationTime = str(round((end_time - start_time)*1000,2))
        
        logging.info(f"Latência: {operationTime}ms")

        return {"message":"Sala criada com sucesso"}    


    def getRoomNames(self) -> dict:
        logging.info(f"Requisição do tipo GET recebida para listagem das salas criadas")

        start_time = time.perf_counter()

        names = self.getNames()  

        end_time = time.perf_counter()
        operationTime = str(round((end_time - start_time)*1000,2))
        
        logging.info(f"Latência: {operationTime}ms")

        return names 

    def getNames(self) -> dict: 
        try:
            rows = self.chatRepository.getAllRooms()
            return self.convertDictToArray(rows)
        except Exception as e:
            logging.error(f"O seguinte erro ocorreu ao buscar os nomes das salas {e}")   
        
        
    def convertDictToArray(self,data:dict) -> dict:
        try:
            result = []
            for row in data:
                name = row[0]
                id = row[1]
                if row is not None and name is not None and id is not None:
                    result.append({
                        "roomName":name,
                        "id":id
                    })
            return result
        except Exception as e:
            logging.error(f"O seguinte erro ocorreu na tentativa de converter os nomes das salas para o uma lista de dict: {e}")   
            raise ValueError("Erro ao converter dados para lista")


    def handleInsertRoomName(self,roomName:str) -> None:

        self.verifyRoomName(roomName)
        
        try:
            self.chatRepository.insertRoomName(roomName)
            logging.info(f"Sala de nome {roomName} criado com sucesso")
            return
        except Exception as e:
            logging.error(f"Ocorreu um erro ao inserir nome da sala {e}")   
            raise ValueError("Ocorreu um erro ao criar sala, tente novamente")
        

    def verifyRoomName(self,roomName:str) -> None:
        try:
            if self.chatRepository.isRoomNameAlreadyTaken(roomName):
                self.handleRoomNameAlreadyTaken(roomName)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logging.error(f"Falha ao verificar se nome de sala {roomName} existe")

    def handleRoomNameAlreadyTaken(self,roomName:str) -> None:
        logging.error(f"Nome de sala {roomName} já solicitada")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"A sala {roomName} já foi escolhida")

    def verifyLength(self,toCompare:str) -> None:
        if len(toCompare) < 3 or len(toCompare) > 30:
            logging.error(f"Solicitação de nome de sala de de tamanho {len(toCompare)} inválida")
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="O nome deve ser maior que 3 e menor que 30")
        
    def calculateJitter(self,attempt:int) -> float:
        wait_time = (0.5 * (attempt + 1))  
        jitter = random.uniform(0.8, 1.2)
        sleep_for = wait_time * jitter
        return sleep_for
    
    
    def handleMessageFail(self,max_retries:int):
        logging.error(f"Falha ao tentar operar maniulação de sala {max_retries} tentativas")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Após algumas tentativas não foi possível executar a operação.Tente novamente")
