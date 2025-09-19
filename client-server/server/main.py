from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller.chatController import routerChat
import uvicorn
import os

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

#ifconfig | grep "inet" | head -n 1 | awk '{print $2}'
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)