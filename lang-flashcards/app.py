import gradio as gr
import requests

def generate_flashcards():
    response = requests.get("http://localhost:8000/flashcards/")
    flashcards = response.json()["flashcards"]
    return flashcards

def display_flashcard(flashcard):
    return gr.Image(flashcard["image_url"], label=flashcard["vocabulary"]["japanese"])

demo = gr.Interface(
    fn=display_flashcard,
    inputs=["text"],
    outputs=["image"],
    title="Japanese Flashcards",
    description="Study Japanese vocabulary with flashcards",
    article="",
    examples=generate_flashcards()
)

if __name__ == "__main__":
    demo.launch()