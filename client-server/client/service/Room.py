import random
import time
import requests
from dotenv import load_dotenv
load_dotenv()
import os
from rich import print
import config
url = os.environ["URL"]

def callCreateRoom():
    roomName = input("Digite o nome da sala que deseja criar: ")
    tryOperation(method=createRoom,roomName=roomName)

def callGetNameRooms():
    return tryOperation(method=getRooms)

def getRooms():
     print("Buscando salas, aguarde...", end='\n', flush=True)
     
     response = requests.get(f"{url}/groups/")
     if response.ok:
        rooms = response.json()
        config.rooms = rooms

        printRooms(config.rooms,"SALAS")
        return rooms
     else:
        if response.status_code >= 500:
            raise ValueError("Erro no servidor, tentando novamente")
        
        detail = response.json().get("detail", "Ocorreu um erro ao criar sala, tente novamente")
        printCustomizeMessage(detail, "red")

def createRoom(roomName):
    print("Criando sala, aguarde...", end='', flush=True)
    
    response = requests.post(f"{url}/groups/{roomName}")
    if response.ok:
        printCustomizeMessage("Sala criada com sucesso", "green")
    else:
        if response.status_code >= 500:
            raise ValueError("Erro no servidor, tentando novamente")
        
        detail = response.json().get("detail", "Ocorreu um erro ao criar sala, tente novamente")
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

def printRooms(rooms,message):
    print(f"[yellow]----------------------- {message} -----------------------")
    for i,room in enumerate(rooms):
        color = "green" if i % 2 == 0  else "yellow"
        print(f"[{color}] {room['id']} - {room['roomName']}")
    print()

def printCustomizeMessage(message, color):
    print("\n--------------------------------------------------")
    print(f"[{color}] {message}")
    print("--------------------------------------------------")