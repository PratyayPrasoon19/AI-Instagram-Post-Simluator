from fastapi import FastAPI
from pydantic import BaseModel

from handler.handler import (
    generate_post_handler,
    post_handler,
    history_handler
)

from repository.repository import init_db


app = FastAPI()

# Initialize Database
init_db()


# Request Model
class GeneratePostRequest(BaseModel):
    topic: str
    tone: str


# 1. Generate Post API
@app.post("/generate-post")
def generate_post(request: GeneratePostRequest):
    response = generate_post_handler(request.topic, request.tone)
    return response


# 2. Post to Instagram (Simulated)
@app.post("/post/{post_id}")
def post_to_instagram(post_id: str):
    response = post_handler(post_id)
    return response


# 3. Get All Posts History
@app.get("/history")
def get_history():
    response = history_handler()
    return response