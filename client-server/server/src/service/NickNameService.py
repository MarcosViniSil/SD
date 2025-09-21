from src.repository.chatRepository import ChatRepository
from fastapi import HTTPException, status
import logging
import time,random

class NickNameService:

    def __init__(self,chatRepository:ChatRepository):
        self.chatRepository = chatRepository


    def registerNickName(self,name:str) -> dict:
        logging.info(f"Requisição do tipo POST recebida para criação do nick name {name}")

        self.verifyLength(name)
        
        start_time = time.perf_counter()

        self.handleInsertNickName(name)

        end_time = time.perf_counter()
        operationTime = str(round((end_time - start_time)*1000,2))
        
        logging.info(f"Latência: {operationTime}ms")

        return {"message":"Nick name criado com sucesso"}     
    
    def handleInsertNickName(self,name:str) -> None:
        attempt = 0
        max_retries = 5

        while attempt < max_retries:
            self.verifyNickName(name)
            
            try:
                self.chatRepository.insertNickName(nickName=name)
                logging.info(f"Nick name {name} criado com sucesso")
                return
            except Exception as e:
                logging.error(f"Na tentativa {attempt} o seguinte erro ocorreu {e}")   
        
            time.sleep(self.calculateJitter(attempt))
            attempt += 1
        
        self.handleMessageFail(max_retries)

    def handleNickAlreadyTaken(self,name:str) -> None:
        logging.error(f"Nick name {name} já solicitado")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"O nickName {name} já foi escolhido")

    def handleMessageFail(self,max_retries:int):
        logging.error(f"Falha ao tentar salvar nick name após {max_retries} tentativas")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Após algumas tentativas não foi possível executar a operação.Tente novamente")

    def verifyNickName(self,name:str) -> None:
        try:
            if self.chatRepository.isNameAlreadyTaken(name):
                self.handleNickAlreadyTaken(name)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logging.error(f"Falha ao verificar se nick name {name} existe")

    def verifyLength(self,toCompare:str) -> None:
        if len(toCompare) < 3 or len(toCompare) > 30:
            logging.error(f"Solicitação de nick name de de tamanho {len(toCompare)} inválida")
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="O nome deve ser maior que 3 e menor que 30")
        
    def calculateJitter(self,attempt:int) -> float:
        wait_time = (0.5 * (attempt + 1))  
        jitter = random.uniform(0.8, 1.2)
        sleep_for = wait_time * jitter
        return sleep_for


