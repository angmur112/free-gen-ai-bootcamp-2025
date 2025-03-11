from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import random  # added import

load_dotenv()

openai.api_key = os.getenv("OPsk-proj-1QPmizVBCZ3E2GkIhMuKXCrsDc-Uq0cvKBTNlHPZt4fpfyc11n2Snjf__0gUZOFAfxTOacVLhgT3BlbkFJvGaCxbu0_tmYdnZjRtv11TketUZzfFakknEHwTR7ccIKOEBj-XhHqQx6RRcI5V_TWZkEWHheIA")

app = FastAPI()

# New health-check route
@app.get("/")
async def health_check():
    return {"status": "success"}
    
class Vocabulary(BaseModel):
    japanese: str
    english: str

class Flashcard(BaseModel):
    vocabulary: list[Vocabulary]

# Updated /flashcards/ endpoint to return a single flashcard
@app.get("/flashcards/")
async def generate_flashcards():
    vocabulary_list = [
        {"japanese": "本", "english": "book"},
        {"japanese": "食べる", "english": "eat"},
        {"japanese": "飲む", "english": "drink"},
        {"japanese": "会う", "english": "meet"},
        {"japanese": "車", "english": "car"}
    ]
    # Select a random vocabulary entry
    vocab = random.choice(vocabulary_list)
    response = openai.Image.create(
        prompt=f"a picture of {vocab['english']}",
        size="256x256"
    )
    image_url = response["data"][0]["url"]
    flashcard = {
        "vocabulary": vocab,
        "image_url": image_url
    }
    return {"status": "success", "flashcard": flashcard}