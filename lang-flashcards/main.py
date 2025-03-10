from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPsk-proj-1QPmizVBCZ3E2GkIhMuKXCrsDc-Uq0cvKBTNlHPZt4fpfyc11n2Snjf__0gUZOFAfxTOacVLhgT3BlbkFJvGaCxbu0_tmYdnZjRtv11TketUZzfFakknEHwTR7ccIKOEBj-XhHqQx6RRcI5V_TWZkEWHheIA")

app = FastAPI()

class Vocabulary(BaseModel):
    japanese: str
    english: str

class Flashcard(BaseModel):
    vocabulary: list[Vocabulary]

@app.get("/flashcards/")
async def generate_flashcards():
    # JLPT N5 vocabulary list
    vocabulary_list = [
        {"japanese": "本", "english": "book"},
        {"japanese": "食べる", "english": "eat"},
        {"japanese": "飲む", "english": "drink"},
        {"japanese": "会う", "english": "meet"},
        {"japanese": "車", "english": "car"}
    ]

    # Generate flashcards
    flashcards = []
    for vocab in vocabulary_list:
        # Use OpenAI to find a random picture for the vocabulary
        response = openai.Image.create(
            prompt=f"a picture of {vocab['english']}",
            size="256x256"
        )
        image_url = response["data"][0]["url"]

        # Create a flashcard
        flashcard = {
            "vocabulary": vocab,
            "image_url": image_url
        }
        flashcards.append(flashcard)

    return {"flashcards": flashcards}