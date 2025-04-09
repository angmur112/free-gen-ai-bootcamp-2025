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
from diffusers import DiffusionPipeline
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
            
            # Check if table exists instead of dropping it
            self.cursor.execute('''
                SELECT count(name) FROM sqlite_master 
                WHERE type='table' AND name='flashcards'
            ''')
            
            # Create table only if it doesn't exist
            if self.cursor.fetchone()[0] == 0:
                print("Creating new flashcards table")
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
            else:
                print("Using existing flashcards table")
                
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

    def check_if_word_exists(self, english_word):
        """Check if the word already exists in the database"""
        try:
            self.cursor.execute("SELECT * FROM flashcards WHERE LOWER(english) = LOWER(?)", (english_word,))
            existing_card = self.cursor.fetchone()
            return existing_card
        except Exception as e:
            print(f"Error checking for existing word: {str(e)}")
            return None

    def create_flashcard(self):
        if self.check_rate_limit():
            english_word = self.word_entry.get().strip()
            if not english_word:
                messagebox.showwarning("Warning", "Please enter an English word")
                return
                
            try:
                # Check if word already exists
                existing_card = self.check_if_word_exists(english_word)
                
                if existing_card:
                    # Word already exists, notify user and show the existing flashcard
                    messagebox.showinfo("Word Exists", f"'{english_word}' already exists in your deck!")
                    
                    # Show the existing flashcard
                    japanese_dict = {
                        'kanji': existing_card[2],
                        'kana': existing_card[3],
                        'romaji': existing_card[4]
                    }
                    image_path = existing_card[5]
                    
                    # Clear entry
                    self.word_entry.delete(0, tk.END)
                    
                    # Show the existing flashcard
                    self.show_existing_flashcard(english_word, japanese_dict, image_path)
                    return
                
                # Continue with creating a new flashcard if the word doesn't exist
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
                
                # Show the newly created flashcard with image
                self.show_new_flashcard(english_word, japanese_dict, image_path)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create flashcard: {str(e)}")
    
    def show_existing_flashcard(self, english, japanese_dict, image_path):
        """Display an existing flashcard with image"""
        # Create new window for the flashcard
        existing_card_window = tk.Toplevel(self.root)
        existing_card_window.title("Existing Flashcard")
        existing_card_window.geometry("550x650")
        
        # Create display frame
        display_frame = ttk.Frame(existing_card_window, padding="20")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Information header
        ttk.Label(
            display_frame, 
            text="Existing Flashcard Found", 
            font=('Arial', 16, 'bold')
        ).pack(pady=(0, 20))
        
        # Image display - same code as show_new_flashcard
        try:
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image.thumbnail((300, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = ttk.Label(display_frame)
                image_label.pack(pady=10)
                image_label.config(image=photo)
                image_label.image = photo  # Keep reference to prevent garbage collection
            else:
                ttk.Label(display_frame, text="Image not available").pack(pady=10)
        except Exception as e:
            print(f"Error displaying image: {str(e)}")
            ttk.Label(display_frame, text="Error displaying image").pack(pady=10)
        
        # Format Japanese text
        japanese_text = (
            f"日本語 (Japanese):\n\n"
            f"漢字: {japanese_dict['kanji']}\n\n"
            f"かな: {japanese_dict['kana']}\n\n"
            f"Romaji: {japanese_dict['romaji']}"
        )
        
        # Word information
        ttk.Label(
            display_frame,
            text=f"English: {english}", 
            font=('Arial Unicode MS', 14, 'bold')
        ).pack(pady=10)
        
        ttk.Label(
            display_frame,
            text=japanese_text,
            font=('Arial Unicode MS', 14),
            justify=tk.LEFT
        ).pack(pady=10)
        
        # Close button
        ttk.Button(
            display_frame, 
            text="Close", 
            command=existing_card_window.destroy
        ).pack(pady=20)

    def show_new_flashcard(self, english, japanese_dict, image_path):
        """Display the newly created flashcard with image"""
        # Create new window for the flashcard
        new_card_window = tk.Toplevel(self.root)
        new_card_window.title("New Flashcard Created")
        new_card_window.geometry("550x650")  # Increased from 500x500 to 550x650
        
        # Create display frame
        display_frame = ttk.Frame(new_card_window, padding="20")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Success header
        ttk.Label(
            display_frame, 
            text="Flashcard Created Successfully!", 
            font=('Arial', 16, 'bold')
        ).pack(pady=(0, 20))
        
        # Image display
        try:
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image.thumbnail((300, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = ttk.Label(display_frame)
                image_label.pack(pady=10)
                image_label.config(image=photo)
                image_label.image = photo  # Keep reference to prevent garbage collection
            else:
                ttk.Label(display_frame, text="Image not available").pack(pady=10)
        except Exception as e:
            print(f"Error displaying image: {str(e)}")
            ttk.Label(display_frame, text="Error displaying image").pack(pady=10)
        
        # Format Japanese text
        japanese_text = (
            f"日本語 (Japanese):\n\n"
            f"漢字: {japanese_dict['kanji']}\n\n"
            f"かな: {japanese_dict['kana']}\n\n"
            f"Romaji: {japanese_dict['romaji']}"
        )
        
        # Word information
        ttk.Label(
            display_frame,
            text=f"English: {english}", 
            font=('Arial Unicode MS', 14, 'bold')
        ).pack(pady=10)
        
        ttk.Label(
            display_frame,
            text=japanese_text,
            font=('Arial Unicode MS', 14),
            justify=tk.LEFT
        ).pack(pady=10)
        
        # Close button
        ttk.Button(
            display_frame, 
            text="Close", 
            command=new_card_window.destroy
        ).pack(pady=20)

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
        """Initialize connection to Hugging Face Inference API with fallback models"""
        try:
            # Your Hugging Face token here
            self.HF_TOKEN = "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"
            
            # Define multiple models to try in order of preference
            self.model_options = [
                "runwayml/stable-diffusion-v1-5",
                "stabilityai/stable-diffusion-2-base",
                "CompVis/stable-diffusion-v1-4",
                "prompthero/openjourney"  # Another good alternative
            ]
            
            self.current_model_index = 0
            self.api_url = f"https://api-inference.huggingface.co/models/{self.model_options[self.current_model_index]}"
            self.headers = {"Authorization": f"Bearer {self.HF_TOKEN}"}
            
            print(f"Hugging Face API connection initialized with model: {self.model_options[self.current_model_index]}")
            
            # Test connection but don't fail if unsuccessful - we'll try others during generation
            try:
                response = requests.post(
                    self.api_url, 
                    headers=self.headers, 
                    json={"inputs": "test"}, 
                    timeout=5  # Short timeout for initial test
                )
                if response.status_code == 200:
                    print("Connection to HF Inference API successful")
                else:
                    print(f"Initial API test returned status code: {response.status_code} (will try other models if needed)")
            except:
                print("Initial API test failed (will try other models during generation)")
                
        except Exception as e:
            print(f"Failed to initialize API connection: {str(e)}")

    def generate_image(self, prompt):
        """Generate image using Hugging Face Inference API with model rotation"""
        try:
            # Add more context to the prompt
            enhanced_prompt = f"high quality photo of {prompt}, professional photography, 4k, detailed"
            
            print(f"Sending prompt to API: {enhanced_prompt}")
            
            # Send request to Hugging Face Inference API
            payload = {
                "inputs": enhanced_prompt,
                "parameters": {
                    "num_inference_steps": 25,
                    "guidance_scale": 7.5
                }
            }
            
            # Try each model in our list
            for model_idx in range(len(self.model_options)):
                # Update to current model in rotation
                self.api_url = f"https://api-inference.huggingface.co/models/{self.model_options[model_idx]}"
                print(f"Trying model: {self.model_options[model_idx]}")
                
                # Implement retry logic with backoff for current model
                max_retries = 3  # Fewer retries per model since we have multiple models
                retry_delay = 2
                
                for attempt in range(max_retries):
                    try:
                        response = requests.post(
                            self.api_url, 
                            headers=self.headers, 
                            json=payload,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            # Process the image from the response
                            image = Image.open(BytesIO(response.content))
                            
                            # Save image
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
                            image_path = os.path.join('images', f"{safe_prompt}_{timestamp}.jpg")
                            
                            # Save the generated image
                            image.save(image_path)
                            print(f"Image successfully generated with model {self.model_options[model_idx]}")
                            print(f"Image saved to: {image_path}")
                            
                            # Update default model for next time if this isn't the first choice
                            if model_idx != self.current_model_index:
                                self.current_model_index = model_idx
                                print(f"Updated default model to: {self.model_options[model_idx]}")
                                
                            return image_path
                        
                        elif response.status_code == 503:
                            print(f"Model {self.model_options[model_idx]} returned 503, attempt {attempt+1}/{max_retries}")
                            time.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                        
                        else:
                            print(f"Model {self.model_options[model_idx]} returned error {response.status_code}, trying next model")
                            break  # Try next model
                            
                    except Exception as e:
                        print(f"Error with model {self.model_options[model_idx]}: {str(e)}")
                        break  # Try next model
            
            # If we get here, all models failed
            print("All models failed, creating text-based fallback image")
            
            # Create a better text-based fallback image
            width, height = 512, 512
            background_color = (245, 245, 245)
            text_color = (0, 0, 0)
            
            # Create image with text
            fallback_img = Image.new('RGB', (width, height), color=background_color)
            
            # Get a drawing context
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(fallback_img)
            
            # Use default font if custom font not available
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                font = ImageFont.load_default()
                
            # Draw word in center of image
            text = prompt
            text_width = draw.textlength(text, font=font)
            text_height = 40  # Approximate height
            
            text_x = (width - text_width) / 2
            text_y = (height - text_height) / 2
            
            draw.text((text_x, text_y), text, fill=text_color, font=font)
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            fallback_path = os.path.join('images', f"fallback_{prompt}_{timestamp}.jpg")
            fallback_img.save(fallback_path)
            
            return fallback_path
            
        except Exception as e:
            print(f"Image generation error: {str(e)}")
            return None

    def save_flashcard(self, english, japanese_dict, image_path):
        try:
            # Use ISO format string instead of datetime object
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
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
                current_time  # Use string instead of datetime object
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
    
    # Create a Flask app in a separate thread
    def run_flask():
        flask_app = Flask(__name__)

        @flask_app.route('/flashcards/<int:card_id>', methods=['GET'])
        def get_flashcard(card_id):
            # Your flashcard retrieval logic here
            return jsonify({"card_id": card_id})

        @flask_app.route('/flashcards/', methods=['POST'])
        def create_flashcard_api():
            # Your flashcard creation logic here
            data = request.get_json()
            return jsonify(data)
        
        flask_app.run(port=5000, debug=False)
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Run the tkinter app in the main thread
    app.run()