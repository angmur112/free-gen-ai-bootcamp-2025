import gradio as gr
import requests
import random
from PIL import Image
import json

class JapaneseWritingPractice:
    def __init__(self):
        self.current_word = None
        self.current_sentence = ""
        self.words = self.initialize_words()

    def initialize_words(self):
        try:
            response = requests.get("http://localhost:5000/api/groups/1/words/raw")
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        
        # Fallback mock data
        return [
            {"japanese": "本", "english": "book"},
            {"japanese": "食べる", "english": "eat"},
            {"japanese": "飲む", "english": "drink"},
            {"japanese": "会う", "english": "meet"},
            {"japanese": "車", "english": "car"}
        ]

    def generate_sentence(self, word):
        templates = [
            f"I {word['english']} every day.",
            f"She likes to {word['english']} in the morning.",
            f"The {word['english']} is on the table.",
            f"We will {word['english']} tomorrow.",
            f"Yesterday, I {word['english']} with my friend."
        ]
        return random.choice(templates)

    def generate_new_practice(self):
        self.current_word = random.choice(self.words)
        self.current_sentence = self.generate_sentence(self.current_word)
        return (
            self.current_sentence,
            f"Hint: Use the word: {self.current_word['japanese']} ({self.current_word['english']})"
        )

    def grade_submission(self, image):
        if image is None:
            return "Please upload an image first.", "", "", "No Grade", "No feedback available."

        # Mock grading system
        mock_transcriptions = ["これは本です。", "明日、友達に会います。", "昨日、ラーメンを食べました。"]
        transcription = random.choice(mock_transcriptions)
        
        translations = {
            "これは本です。": "This is a book.",
            "明日、友達に会います。": "I will meet my friend tomorrow.",
            "昨日、ラーメンを食べました。": "Yesterday, I ate ramen."
        }
        translation = translations.get(transcription, "I like to study Japanese.")
        
        grades = ["S", "A", "B", "C"]
        grade = random.choice(grades)
        
        feedback_templates = {
            "S": "Excellent! Your handwriting is clear and the sentence is perfectly accurate.",
            "A": "Very good! Your handwriting is readable and the sentence is mostly accurate.",
            "B": "Good effort. Your handwriting needs some work and there are a few grammatical errors.",
            "C": "Keep practicing. Your handwriting is difficult to read and there are several errors."
        }
        
        feedback = feedback_templates[grade]
        
        return (
            self.current_sentence,
            transcription,
            translation,
            f"Grade: {grade}",
            feedback
        )

def create_app():
    app = JapaneseWritingPractice()
    
    with gr.Blocks(title="Japanese Writing Practice") as interface:
        gr.Markdown("# Japanese Writing Practice")
        
        with gr.Row():
            with gr.Column():
                sentence_text = gr.Textbox(label="Sentence to Practice", interactive=False)
                hint_text = gr.Textbox(label="Hint", interactive=False)
                generate_btn = gr.Button("Generate New Sentence")
                
                image_input = gr.Image(label="Upload your handwritten Japanese", type="pil")
                submit_btn = gr.Button("Submit for Review")

            with gr.Column():
                original_sentence = gr.Textbox(label="Original Sentence", interactive=False)
                transcription = gr.Textbox(label="Transcription", interactive=False)
                translation = gr.Textbox(label="Translation", interactive=False)
                grade = gr.Textbox(label="Grade", interactive=False)
                feedback = gr.Textbox(label="Feedback", interactive=False)

        # Event handlers
        generate_btn.click(
            fn=app.generate_new_practice,
            outputs=[sentence_text, hint_text]
        )
        
        submit_btn.click(
            fn=app.grade_submission,
            inputs=[image_input],
            outputs=[original_sentence, transcription, translation, grade, feedback]
        )

        # Generate initial sentence on load
        initial_sentence, initial_hint = app.generate_new_practice()
        sentence_text.value = initial_sentence
        hint_text.value = initial_hint

    return interface

if __name__ == "__main__":
    demo = create_app()
    demo.launch()
