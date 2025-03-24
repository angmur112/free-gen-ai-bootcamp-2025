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
from deep_translator import GoogleTranslator  # Remove MicrosoftTranslator
import base64
from io import BytesIO
import time
import pykakasi
from diffusers import StableDiffusionPipeline
import torch

class FlashcardApp:
    def __init__(self):
        self.setup_directories()
        self.setup_database()
        self.setup_ui()
        self.last_request_time = datetime.now()
        self.request_count = 0
        self.current_card_index = 0
        self.cards = []
        self.kakasi = pykakasi.kakasi()
        self.setup_stable_diffusion()
        
    def setup_directories(self):
        try:
            os.makedirs('images', exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create images directory: {str(e)}")

    def setup_database(self):
        try:
            self.conn = sqlite3.connect('flashcards.db')
            self.cursor = self.conn.cursor()
            
            # Drop existing table if it exists
            self.cursor.execute('DROP TABLE IF EXISTS flashcards')
            
            # Create new table with consistent column names
            self.cursor.execute('''
                CREATE TABLE flashcards (
                    id INTEGER PRIMARY KEY,
                    english TEXT,
                    japanese_kanji TEXT,
                    japanese_kana TEXT,
                    japanese_romaji TEXT,
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
        
        # Set font for Japanese text support
        default_font = ('Arial Unicode MS', 12)
        self.root.option_add('*Font', default_font)
        
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
                # Translate text with multiple formats
                japanese_dict = self.translate_text(english_word)
                if not japanese_dict:
                    raise Exception("Translation failed")
                
                # Generate image
                image_path = self.generate_image(english_word)
                if not image_path:
                    messagebox.showwarning("Warning", "Could not generate image, using placeholder")
                    image_path = os.path.join('images', 'placeholder.jpg')
                
                # Save to database
                self.save_flashcard(english_word, japanese_dict, image_path)
                
                # Clear entry
                self.word_entry.delete(0, tk.END)
                
                messagebox.showinfo("Success", 
                    f"Flashcard created successfully!\n"
                    f"English: {english_word}\n"
                    f"漢字: {japanese_dict['kanji']}\n"
                    f"かな: {japanese_dict['kana']}\n"
                    f"Romaji: {japanese_dict['romaji']}")
                    
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

    def translate_text(self, text, from_lang='en', to_lang='ja'):
        """Translate and convert to different Japanese formats"""
        try:
            # Use Google Translate only
            translator = GoogleTranslator(source=from_lang, target=to_lang)
            kanji = translator.translate(text)
            
            if not kanji:
                raise Exception("Translation failed")
            
            # Ensure text is properly encoded
            kanji = kanji.encode('utf-8').decode('utf-8')
            
            # Convert to different Japanese formats using kakasi
            result = self.kakasi.convert(kanji)
            
            if not result or len(result) == 0:
                raise Exception("Failed to convert Japanese text")
            
            # Extract different formats
            kana = result[0]['kana']  # Hiragana/Katakana
            romaji = result[0]['hepburn']  # Romaji
            
            # Debug output
            print(f"Translation results:")
            print(f"Original text: {text}")
            print(f"Kanji: {kanji}")
            print(f"Kana: {kana}")
            print(f"Romaji: {romaji}")
            
            return {
                'kanji': kanji,
                'kana': kana,
                'romaji': romaji
            }
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None

    def setup_stable_diffusion(self):
        """Initialize Stable Diffusion model"""
        try:
            # Use CompVis model which is more accessible
            model_id = "CompVis/stable-diffusion-v1-4"
            
            # Add your Hugging Face token here
            HF_TOKEN = "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"  # Get from huggingface.co/settings/tokens
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float32,
                use_auth_token=HF_TOKEN,
                safety_checker=None  # Disable safety checker if memory is an issue
            )
            
            # Enable CPU offload if memory is limited
            self.pipe.enable_attention_slicing()
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
            else:
                print("CUDA not available, using CPU")
            print("Stable Diffusion initialized successfully")
            
        except Exception as e:
            print(f"Failed to load Stable Diffusion: {str(e)}")
            self.pipe = None

    def generate_image(self, prompt):
        """Generate image using Stable Diffusion"""
        try:
            if not self.pipe:
                print("Stable Diffusion not initialized")
                return None
                
            print(f"Generating image for prompt: {prompt}")
            
            # Add more context to the prompt
            enhanced_prompt = f"high quality photo of {prompt}, professional photography, 4k, detailed"
            
            # Generate image with error handling
            try:
                image = self.pipe(
                    enhanced_prompt,
                    num_inference_steps=20,  # Reduce steps for faster generation
                    guidance_scale=7.5
                ).images[0]
            except Exception as e:
                print(f"Image generation failed: {str(e)}")
                return None
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
            image_path = os.path.join('images', f"{safe_prompt}_{timestamp}.jpg")
            
            # Save the generated image
            image.save(image_path)
            print(f"Image saved to: {image_path}")
            
            return image_path
            
        except Exception as e:
            print(f"Image generation error: {str(e)}")
            return None

    def save_flashcard(self, english, japanese_dict, image_path):
        try:
            self.cursor.execute('''
                INSERT INTO flashcards 
                (english, japanese_kanji, japanese_kana, japanese_romaji, image_path, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                english, 
                japanese_dict['kanji'],
                japanese_dict['kana'],
                japanese_dict['romaji'],
                image_path,
                datetime.now()
            ))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to save to database: {str(e)}")

    def view_deck(self):
        # Create new window for viewing flashcards
        self.deck_window = tk.Toplevel(self.root)
        self.deck_window.title("Japanese Flashcard Deck")
        self.deck_window.geometry("600x600")  # Increased height for better text display

        # Create display area
        self.display_frame = ttk.Frame(self.deck_window, padding="20")
        self.display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Image display
        self.image_label = ttk.Label(self.display_frame)
        self.image_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Word display with more space
        self.english_label = ttk.Label(self.display_frame, text="", font=('Arial', 14))
        self.english_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.japanese_label = ttk.Label(self.display_frame, text="", font=('Arial', 14))
        self.japanese_label.grid(row=2, column=0, columnspan=3, pady=10)

        # Navigation buttons
        ttk.Button(self.display_frame, text="← Previous", 
                  command=self.prev_card).grid(row=3, column=0, pady=20, padx=20)
        ttk.Button(self.display_frame, text="Next →", 
                  command=self.next_card).grid(row=3, column=2, pady=20, padx=20)

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
        # Update English display
        self.english_label.config(
            text=f"English: {card[1]}", 
            font=('Arial Unicode MS', 14, 'bold')
        )
        
        # Format Japanese text
        japanese_text = (
            f"日本語 (Japanese):\n\n"
            f"漢字: {card[2]}\n\n"
            f"かな: {card[3]}\n\n"
            f"Romaji: {card[4]}"
        )
        
        self.japanese_label.config(
            text=japanese_text,
            font=('Arial Unicode MS', 14),
            justify=tk.LEFT
        )

        # Update image handling with older PIL constant
        try:
            image_path = card[5]
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                # Use Image.LANCZOS instead of Image.Resampling.LANCZOS
                image.thumbnail((300, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            else:
                placeholder_path = os.path.join('images', 'placeholder.jpg')
                if os.path.exists(placeholder_path):
                    image = Image.open(placeholder_path)
                    image.thumbnail((300, 200), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
                else:
                    self.image_label.config(text="No image available")
        except Exception as e:
            print(f"Image loading error: {str(e)}")
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
        # Your flashcard creation logic here
        data = request.get_json()
        return jsonify(data)

    app.run()