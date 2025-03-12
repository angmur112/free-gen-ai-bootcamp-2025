import random
import requests
from PIL import Image
import io
import streamlit as st
import base64

class FreeJapaneseFlashcardGenerator:
    def __init__(self):
        # Comprehensive JLPT N5 Vocabulary with more detailed information
        self.vocabulary = [
            {"japanese": "本", "english": "book", "category": "noun", "example": "この本は面白いです。", "keywords": ["reading", "literature"]},
            {"japanese": "車", "english": "car", "category": "noun", "example": "赤い車が好きです。", "keywords": ["transportation", "vehicle"]},
            {"japanese": "水", "english": "water", "category": "noun", "example": "水を飲みます。", "keywords": ["drink", "liquid"]},
            {"japanese": "食べる", "english": "eat", "category": "verb", "example": "寿司を食べます。", "keywords": ["food", "meal"]},
            {"japanese": "飲む", "english": "drink", "category": "verb", "example": "お茶を飲みます。", "keywords": ["beverage", "drink"]},
        ]

    def get_free_image(self, keyword):
        """
        Robust image fetching with multiple fallback methods
        """
        # List of alternative image sources
        image_sources = [
            f"https://source.unsplash.com/400x300/?{keyword}",
            f"https://picsum.photos/seed/{keyword}/400/300",
        ]

        # Try Pixabay API first (with a public key)
        try:
            # Note: Replace with your Pixabay API key if you have one
            pixabay_url = f"https://pixabay.com/api/?key=40913578-1234567890abcdef&q={keyword}&image_type=photo&per_page=3"
            
            response = requests.get(pixabay_url, timeout=10)
            
            # Check if API request was successful
            if response.status_code == 200:
                images = response.json().get('hits', [])
                if images:
                    selected_image = random.choice(images)
                    image_url = selected_image.get('webformatURL')
                    
                    # Fetch the image
                    image_response = requests.get(image_url, timeout=10)
                    if image_response.status_code == 200:
                        return Image.open(io.BytesIO(image_response.content))
            
            # If Pixabay fails, try alternative sources
            for source in image_sources:
                try:
                    alt_response = requests.get(source, timeout=10)
                    if alt_response.status_code == 200:
                        return Image.open(io.BytesIO(alt_response.content))
                except Exception as alt_error:
                    st.warning(f"Alternative image source failed: {alt_error}")
            
            st.error("Image fetch completely failed")
        
        except Exception as e:
            st.error(f"Image fetch completely failed: {e}")

    def select_random_vocab(self, filtered_vocab):
        """
        Safely select a random vocabulary item
        """
        try:
            return random.choice(filtered_vocab)
        except IndexError:
            st.error("No vocabulary items available")
            return None

    """
    # def _generate_dezgo_image(self, vocab_item):
    #     '''
    #     Generate image using Dezgo API
    #     '''
    #     if not self.dezgo_api_key:
    #         self.api_errors.append("Dezgo API key not found")
    #         return None
    #
    #     try:
    #         headers = {
    #             'X-Dezgo-Key': self.dezgo_api_key,
    #             'Content-Type': 'application/json'
    #         }
    #         
    #         prompt = self._create_contextual_prompt(vocab_item)
    #         
    #         payload = {
    #             "prompt": prompt,
    #             "negative_prompt": "blurry, bad quality, text, watermark",
    #             "model": "stable_diffusion_2.1",
    #             "width": 512,
    #             "height": 512,
    #             "steps": 30,
    #             "guidance": 7.5
    #         }
    #
    #         response = requests.post(
    #             self.dezgo_api_url,
    #             headers=headers,
    #             json=payload
    #         )
    #
    #         if response.status_code == 200:
    #             return Image.open(io.BytesIO(response.content))
    #         else:
    #             self.api_errors.append(f"Dezgo API error: {response.status_code}")
    #             return None
    #
    #     except Exception as e:
    #         self.api_errors.append(f"Dezgo API error: {str(e)}")
    #         return None
    """