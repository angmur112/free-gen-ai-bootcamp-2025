import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import requests
import json
from datetime import datetime, timedelta
import threading
from flask import Flask, jsonify, request
from deep_translator import GoogleTranslator

class FlashcardApp:
    def __init__(self):
        self.setup_directories()
        self.setup_database()
        self.setup_ui()
        self.last_request_time = datetime.now()
        self.request_count = 0
        self.current_card_index = 0
        self.cards = []
        
    def setup_directories(self):
        try:
            os.makedirs('images', exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create images directory: {str(e)}")

    def setup_database(self):
        try:
            self.conn = sqlite3.connect('flashcards.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY,
                    english TEXT,
                    japanese TEXT,
                    image_path TEXT,
                    created_at TIMESTAMP
                )
            ''')
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Japanese Flashcard App")
        
        # Input frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(input_frame, text="Enter English word:").grid(row=0, column=0)
        self.word_entry = ttk.Entry(input_frame)
        self.word_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(input_frame, text="Create Flashcard", 
                  command=self.create_flashcard).grid(row=0, column=2)
        ttk.Button(input_frame, text="View Deck", 
                  command=self.view_deck).grid(row=0, column=3)

    def create_flashcard(self):
        if self.check_rate_limit():
            english_word = self.word_entry.get().strip()
            if not english_word:
                messagebox.showwarning("Warning", "Please enter an English word")
                return
                
            try:
                # Translate text
                translator = GoogleTranslator(source='en', target='ja')
                japanese_text = translator.translate(english_word)
                
                # Generate and save image
                image_path = self.generate_image(english_word)
                
                # Save to database
                self.save_flashcard(english_word, japanese_text, image_path)
                
                messagebox.showinfo("Success", "Flashcard created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create flashcard: {str(e)}")

    def check_rate_limit(self):
        current_time = datetime.now()
        if (current_time - self.last_request_time).seconds < 60:
            if self.request_count >= 5:
                messagebox.showwarning("Rate Limit", "Please wait before creating more flashcards")
                return False
            self.request_count += 1
        else:
            self.last_request_time = current_time
            self.request_count = 1
        return True

    def generate_image(self, prompt):
        # Implementation using a free AI image generation API
        # This is a placeholder - you'll need to implement with your chosen API
        pass

    def save_flashcard(self, english, japanese, image_path):
        try:
            self.cursor.execute('''
                INSERT INTO flashcards (english, japanese, image_path, created_at)
                VALUES (?, ?, ?, ?)
            ''', (english, japanese, image_path, datetime.now()))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to save to database: {str(e)}")

    def view_deck(self):
        # Create new window for viewing flashcards
        self.deck_window = tk.Toplevel(self.root)
        self.deck_window.title("Flashcard Deck")
        self.deck_window.geometry("600x400")

        # Create display area
        self.display_frame = ttk.Frame(self.deck_window, padding="10")
        self.display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Image display
        self.image_label = ttk.Label(self.display_frame)
        self.image_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Word display
        self.english_label = ttk.Label(self.display_frame, text="", font=('Arial', 14))
        self.english_label.grid(row=1, column=0, columnspan=3)
        self.japanese_label = ttk.Label(self.display_frame, text="", font=('Arial', 14))
        self.japanese_label.grid(row=2, column=0, columnspan=3)

        # Navigation buttons
        ttk.Button(self.display_frame, text="Previous", 
                  command=self.prev_card).grid(row=3, column=0, pady=20)
        ttk.Button(self.display_frame, text="Next", 
                  command=self.next_card).grid(row=3, column=2, pady=20)

        # Load cards
        try:
            self.cursor.execute("SELECT * FROM flashcards ORDER BY created_at DESC")
            self.cards = self.cursor.fetchall()
            if self.cards:
                self.show_current_card()
            else:
                messagebox.showinfo("Empty Deck", "No flashcards in your deck yet!")
                self.deck_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flashcards: {str(e)}")
            self.deck_window.destroy()

    def show_current_card(self):
        if not self.cards:
            return
        
        card = self.cards[self.current_card_index]
        self.english_label.config(text=f"English: {card[1]}")
        self.japanese_label.config(text=f"Japanese: {card[2]}")

        # Load and display image
        try:
            image_path = card[3]
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((300, 200))  # Resize for display
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep reference
            else:
                self.image_label.config(text="Image not found")
        except Exception as e:
            self.image_label.config(text="Error loading image")

    def next_card(self):
        if self.cards:
            self.current_card_index = (self.current_card_index + 1) % len(self.cards)
            self.show_current_card()

    def prev_card(self):
        if self.cards:
            self.current_card_index = (self.current_card_index - 1) % len(self.cards)
            self.show_current_card()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FlashcardApp()
    app.run()

flask_app = Flask(__name__)

@flask_app.route('/flashcards/<int:card_id>', methods=['GET'])
def get_flashcard(card_id):
    # Your flashcard retrieval logic here
    return jsonify({"card_id": card_id})

@flask_app.route('/flashcards/', methods=['POST'])
def create_flashcard():
    data = request.get_json()
    # Your flashcard creation logic here
    return jsonify(data)
