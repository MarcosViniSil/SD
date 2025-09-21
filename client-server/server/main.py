from datetime import date
import logging
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from src.controller.chatController import routerChat
from src.controller.NickNameController import routerNickName
from src.controller.RoomNameController import routerRoomName
import uvicorn
import os
import asyncio
from fastapi.responses import JSONResponse

os.makedirs("./logs", exist_ok=True)

app = FastAPI()

MAX_CONCURRENT_REQUESTS = 5
current_requests = 0
lock = asyncio.Lock() 

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    await asyncio.sleep(10)
    return {"message": "working"}


app.include_router(routerChat)
app.include_router(routerNickName)
app.include_router(routerRoomName)

@app.middleware("http")
async def limitRequests(request: Request, call_next):
    global current_requests
    async with lock:
        if current_requests >= MAX_CONCURRENT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"detail": "Muitas pessoas conectadas, tente novamente mais tarde"}
            )
        current_requests += 1

    try:
        response = await call_next(request)
        return response
    finally:
        async with lock:
            current_requests -= 1

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