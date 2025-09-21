import requests
from dotenv import load_dotenv

from service.Room import callCreateRoom, callGetNameRooms, createRoom, printCustomizeMessage, printRooms
from service.nickName import callCreateNickName, createNickName
load_dotenv()
import os


global nickName, roomId, rooms, alreadyFetchRooms
nickName = ""
roomId = -1
rooms = []
alreadyFetchRooms = False

url = os.environ["URL"]
def getRoomId(nameRoom):
    global roomId
    for room in rooms:
        if room['roomName'] == nameRoom:
            roomId = room['id']
            return

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
        rooms = callGetNameRooms(not alreadyFetchRooms)
        alreadyFetchRooms = True
    elif option == 3:
        
        if alreadyFetchRooms and len(rooms) == 0:
            printCustomizeMessage("Nenhuma sala disponível.Crie uma!! ","yellow")
            continue
        
        if not alreadyFetchRooms:
            rooms = callGetNameRooms(False)
            alreadyFetchRooms = True

        printRooms(rooms,"SALAS")
        roomName = input("Digite o nome da sala para entrar: ")
        getRoomId(roomName)
        print("aqui  ",roomId)
        while roomId == -1:
            printCustomizeMessage("Sala não encontrada, tente novamente ","red")
            printRooms(rooms,"SALAS")
            roomName = input("Digite o nome da sala para entrar: ")
            getRoomId(roomName)
            
        nickNameR = callCreateNickName()
        while nickNameR is None:
            nickNameR = callCreateNickName()
            print(nickNameR)
        nickName = nickNameR

    else:
        printCustomizeMessage("Opção não reconhecida","red")
    



def make_request(i):
    print(i)
    response = requests.get(url)
    print('Status code:', response.status_code)
    print('Response:', response.text)
