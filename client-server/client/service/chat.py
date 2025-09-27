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
    response = requests.get(f"{url}/server-time")
    if response.ok:
        config.lastTimesTamp = response.json()["serverTime"]
    else:
        config.lastTimesTamp = getTimesTamp()  
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

        if len(msg) < 3 or len(msg) > 200:
              printCustomizeMessage("Mensagens devem conter no mínimo 3 e no máximo 200 caracteres", "red")
              continue
        response = requests.post(f"{url}/groups/{config.roomId}/messages",
                json={"nickName": config.nickName, "message": msg,"idemKey":generateHash(),"timestampClient":str(getTimesTamp())})
            
        if response.ok:
            printCustomizeMessage("Mensagem enviada com sucesso", "green")
        else:
            printCustomizeMessage("Falha ao enviar mensagem", "red")

def poll_messages():
    while True:
        time.sleep(10)
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
    config.rooms = callGetNameRooms()
    if len(config.rooms) == 0:
        printCustomizeMessage("Nenhuma sala disponível. Crie uma!", "yellow")
        return -1
    config.alreadyFetchRooms = True
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
    return int(current_datetime.timestamp() * 1000)

def printMessages(messages):
    for message in messages:
        print(f"{message['date']} - {message['nickName']} -> {message['message']}")
    
    buffer = readline.get_line_buffer()
    sys.stdout.write("Digite sua mensagem: " + buffer)
    sys.stdout.flush()

def getLastData(messages):
    lastId = 0
    lastTimesTamp = 0
    for message in messages:
        if int(message['messageId']) > lastId:
            lastId = int(message['messageId'])
            lastTimesTamp = int(message['timesTamp']) 

    if lastId > 0 and lastTimesTamp > 0:
        config.lastId = lastId
        config.lastTimesTamp = lastTimesTamp

def generateHash():
    my_uuid = uuid.uuid4()
    return str(my_uuid)