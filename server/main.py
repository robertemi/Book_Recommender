from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
from contextlib import asynccontextmanager
from rag_agent import chat as chat_logic
from embeddings import embedd_and_persist

@asynccontextmanager
async def lifespan(app: FastAPI):
    await embedd_and_persist()
    yield


app = FastAPI(title='Book Recommender App', lifespan=lifespan)

class ChatIn(BaseModel):
    user_prompt: str

class ChatOut(BaseModel):
    chat_response: str


@app.get('/')
async def base():
    return {'message': 'Hello World!'}


@app.post('/chat', response_model=ChatOut)
async def chat(payload: ChatIn):
    return ChatOut(chat_response = await chat_logic(payload.user_prompt))