from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from rag_agent import chat as chat_logic


app = FastAPI(title='Book Recommender App')

class ChatIn(BaseModel):
    user_prompt: str

class ChatOut(BaseModel):
    chat_response: str



@app.post('/chat', response_model=ChatOut)
def chat(payload: ChatIn):
    return ChatOut(chat_response = chat_logic(payload.user_prompt))