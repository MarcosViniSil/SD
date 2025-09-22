import requests
from dotenv import load_dotenv

from service.Room import callCreateRoom, callGetNameRooms, createRoom, printCustomizeMessage, printRooms
from service.chat import createChat
from service.nickName import callCreateNickName, createNickName
load_dotenv()
import os
import config

url = os.environ["URL"]


while True:
    print("0 --> Sair")
    print("1 --> Criar Sala")
    print("2 --> Listar salas")
    print("3 --> Entrar em sala")
    option = int(input("Digite uma opção: "))
    if option == 0:
        break
    elif option == 1:
        callCreateRoom()
    elif option == 2:
        config.rooms = callGetNameRooms()
        config.alreadyFetchRooms = True
    elif option == 3:
        createChat()
    else:
        printCustomizeMessage("Opção não reconhecida","red")
    

