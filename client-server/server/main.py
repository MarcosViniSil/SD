from datetime import date
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller.chatController import routerChat
from src.controller.NickNameController import routerNickName
from src.controller.RoomNameController import routerRoomName
import uvicorn
import os

os.makedirs("./logs", exist_ok=True)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "working"}


app.include_router(routerChat)
app.include_router(routerNickName)
app.include_router(routerRoomName)

#ifconfig | grep "inet" | head -n 1 | awk '{print $2}'
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


def configureFileLog():
    dateActual = date.today()
    log_path = f"./logs/{dateActual}.log"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    file_handler = logging.FileHandler(log_path, mode='a')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    print(f"Log configurado para o arquivo {log_path}")    

configureFileLog()