import random
import time
from dotenv import load_dotenv

from service.Room import printCustomizeMessage
load_dotenv()
import os
import requests

url = os.environ["URL"]


def callCreateNickName():
    nickName = input("Digite o nick name que deseja usar na sala: ")
    return tryOperation(createNickName,nickName=nickName)

def createNickName(nickName):
    print("Criando nick name, aguarde...", end='', flush=True)
    
    response = requests.post(f"{url}/nick/{nickName}")
    if response.ok:
        printCustomizeMessage("Nick name criado com sucesso", "green")
        return nickName
    else:
        if response.status_code >= 500:
            raise ValueError("Erro no servidor, tentando novamente")
        
        detail = response.json().get("detail", "Ocorreu um erro ao criar nickName, tente novamente")
        printCustomizeMessage(detail, "red")    

def tryOperation(method = None,*args, **kwargs) -> None:
    attempt = 0
    max_retries = 5

    while attempt < max_retries:
        try:
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            pass
    
        time.sleep(calculateJitter(attempt))
        attempt += 1
    
    handleMessageFail(max_retries)

def handleMessageFail(max_retries):
    print(f"Após {max_retries} tentativas o servidor não respondeu, tente novamente")

def calculateJitter(attempt:int) -> float:
    wait_time = (0.5 * (attempt + 1))  
    jitter = random.uniform(0.8, 1.2)
    sleep_for = wait_time * jitter
    return sleep_for