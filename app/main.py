import asyncio
from datetime import time
from pathlib import Path

from fastapi import FastAPI

#싱글톤 객체로 생성
app = FastAPI()

#Path(__file__).resolve()가 현재 파일의 경로
#즉 BASE_DIR은 현재 경로의 상위 경로, 이 경우 app 폴더
BASE_DIR = Path(__file__).resolve().parent

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/movie/{name}")
async def say_hello(name: str):



    return {"message": f"Hello {name}"}
