from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from handler.handler import (
    generate_post_handler,
    post_handler,
    history_handler
)

from repository.repository import init_db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
init_db()

# Expose generated images as static files
app.mount("/generated", StaticFiles(directory="."), name="generated")


# Request Model
class GeneratePostRequest(BaseModel):
    topic: str
    tone: str


# 1. Generate Post API
@app.post("/generate-post")
def generate_post(request: GeneratePostRequest):
    response = generate_post_handler(request.topic, request.tone)

    if response.get("image_url"):
        response["image_url"] = f"generated/{response['image_url']}"

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
