import threading
import time
import requests
import os
import config
from datetime import datetime
from dotenv import load_dotenv
import uuid
from service.Room import callGetNameRooms, printCustomizeMessage, printRooms
from service.nickName import callCreateNickName, tryOperation
import readline
import sys


load_dotenv()
url = os.environ["URL"]

def createChat():
    if getGroup() == -1:
        return
    getNickName()
    getMessages()

    threading.Thread(target=callInputUser, daemon=True).start()
    threading.Thread(target=poll_messages, daemon=True).start()

    while True:
        time.sleep(1)

def callInputUser():
    tryOperation(listen_user)

def listen_user():
    while True:
        print()
        msg = input("Digite sua mensagem: ")
        if msg.strip().lower() == "sair":
            print("Saindo do chat...")
            os._exit(0)  
        response = requests.post(f"{url}/groups/{config.roomId}/messages",
                json={"nickName": config.nickName, "message": msg,"idemKey":generateHash(),"timestampClient":str(getTimesTamp())})
            
        if response.ok:
            printCustomizeMessage("Mensagem enviada com sucesso", "green")
        else:
            printCustomizeMessage("Falha ao enviar mensagem", "red")

def poll_messages():
    while True:
        time.sleep(15)
        try:
            tryOperation(getMessages)
        except Exception as e:
            printCustomizeMessage(f"Erro ao buscar mensagens: {e}", "red")

def getMessages():
    currentTimesTamp = getTimesTamp() if config.lastTimesTamp == 0 else config.lastTimesTamp
    printCustomizeMessage("Buscando novas mensagens...", "yellow")
    
    stringUrl = f"{url}/groups/{config.roomId}/messages?timesTamp={currentTimesTamp}&lastId={config.lastId}&limit=10"
    response = requests.get(stringUrl)

    if response.ok:
        config.messages += response.json()
        printMessages(config.messages)
        getLastData(config.messages)
    else:
        detail = response.json().get("detail", "Erro ao buscar mensagens")
        printCustomizeMessage(detail, "red")

def getGroup():
    if config.alreadyFetchRooms and len(config.rooms) == 0:
        printCustomizeMessage("Nenhuma sala disponível. Crie uma!", "yellow")
        return -1 

    if not config.alreadyFetchRooms:
        config.rooms = callGetNameRooms()
        config.alreadyFetchRooms = True
    
    printRooms(config.rooms,"SALAS")
    roomName = input("Digite o nome da sala para entrar: ")
    if roomName == '0':
        return -1
    getRoomId(roomName)
    while config.roomId == -1:
        printCustomizeMessage("Sala não encontrada, tente novamente", "red")
        printRooms(config.rooms,"SALAS")
        roomName = input("Digite o nome da sala para entrar: ")
        if roomName == '0':
            return -1
        getRoomId(roomName)

def getNickName():
    nickNameR = callCreateNickName()
    while nickNameR is None:
        nickNameR = callCreateNickName()
    config.nickName = nickNameR

def getRoomId(nameRoom):
    for room in config.rooms:
        if room['roomName'] == nameRoom:
            config.roomId = room['id']
            return

def getTimesTamp():
    current_datetime = datetime.now()
    return int(current_datetime.timestamp())

def printMessages(messages):
    sys.stdout.write("\r")  
    sys.stdout.flush()

    for message in messages:
        print(f"{message['date']} - {message['nickName']} -> {message['message']}")

    buffer = readline.get_line_buffer()
    sys.stdout.write("Digite sua mensagem: " + buffer)
    sys.stdout.flush()

def getLastData(messages):
   lastId = 0
   lastTimesTamp = 0
   for message in messages:  
       if message['messageId'] > lastId:
           lastId = message['messageId']
           lastTimesTamp = message['timesTamp']
    
   config.lastId = lastId
   config.lastTimesTamp = lastTimesTamp

def generateHash():
    my_uuid = uuid.uuid4()
    return str(my_uuid)
