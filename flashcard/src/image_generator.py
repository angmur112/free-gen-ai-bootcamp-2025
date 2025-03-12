import os
import io
import random
import requests
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FreeImageGenerator:
    def __init__(self):
        # API Configurations
        self.huggingface_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
        if not self.huggingface_api_token:
            st.error("""
            ⚠️ Hugging Face API token not found! Please:
            1. Sign up at https://huggingface.co
            2. Go to https://huggingface.co/settings/tokens
            3. Create a new token (READ access is sufficient)
            4. Create/edit .env file in the project root
            5. Add: HUGGINGFACE_API_TOKEN=your_token_here
            """)
        
        # API Endpoints - Using a more reliable model
        self.hf_api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        # Logging and error tracking
        self.api_errors = []

    def generate_image(self, vocab_item):
        """
        Primary image generation method with Hugging Face as primary source
        """
        # Reset error tracking
        self.api_errors = []

        # Try Hugging Face first
        image = self._generate_huggingface_image(vocab_item)
        if image:
            return image

        # Fallback to Unsplash
        image = self._generate_unsplash_image(vocab_item)
        if image:
            return image

        # Final fallback to local placeholder
        return self._generate_local_placeholder(vocab_item)

    def _generate_huggingface_image(self, vocab_item):
        """
        Generate image using Hugging Face Stable Diffusion API
        """
        if not self.huggingface_api_token:
            self.api_errors.append("Missing Hugging Face API token - Check .env file")
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.huggingface_api_token}",
                "Content-Type": "application/json"
            }
            
            prompt = self._create_contextual_prompt(vocab_item)
            
            # Simplified payload for better compatibility
            payload = {
                "inputs": prompt,
            }
            
            st.info("Generating image with Hugging Face API... (this may take a few seconds)")
            response = requests.post(
                self.hf_api_url,
                headers=headers,
                json=payload,
                timeout=30  # Increased timeout
            )

            if response.status_code == 401:
                error_msg = "Invalid Hugging Face API token - Please check your token in .env file"
                self.api_errors.append(error_msg)
                st.error(error_msg)
                return None
            elif response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            else:
                error_msg = f"Hugging Face API error: {response.status_code} - {response.text}"
                self.api_errors.append(error_msg)
                st.warning(error_msg)
                return None

        except Exception as e:
            error_msg = f"Hugging Face API error: {str(e)}"
            self.api_errors.append(error_msg)
            st.error(error_msg)
            return None

    def _generate_dezgo_image(self, vocab_item):
        """
        Generate image using Dezgo API
        """
        if not self.dezgo_api_key:
            st.warning("Dezgo API key not configured")
            return None

        try:
            # Create prompt
            prompt = self._create_contextual_prompt(vocab_item)
            
            # Payload
            payload = {
                "prompt": prompt,
                "negative_prompt": "low quality, bad composition",
                "width": 512,
                "height": 512
            }
            
            # Headers
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {self.dezgo_api_key}"
            }
            
            # Send request
            response = requests.post(
                self.dezgo_api_url, 
                data=payload, 
                headers=headers
            )
            
            # Detailed error handling
            if response.status_code == 401:
                st.error("Dezgo API: Unauthorized. Check your API key.")
                return None
            
            # Check response
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            
            st.warning(f"Dezgo API returned {response.status_code}: {response.text}")
            return None
        
        except Exception as e:
            st.error(f"Dezgo image generation error: {e}")
            return None

    def _generate_unsplash_image(self, vocab_item):
        """
        Fetch a random image from Unsplash
        """
        try:
            # Create better search query
            query = "+".join(vocab_item['keywords'][:2]) if vocab_item.get('keywords') else vocab_item['english']
            query = query.replace(" ", "+")
            
            # Add category context for better results
            if vocab_item.get('category'):
                query += f"+{vocab_item['category']}"
            
            # Unsplash API URL with better parameters
            url = f"https://source.unsplash.com/featured/400x300/?{query}"
            
            st.info(f"Fetching image from Unsplash for: {query}")
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            
            st.warning(f"Unsplash image fetch failed: {response.status_code}")
            return None
            
        except Exception as e:
            st.warning(f"Unsplash error: {str(e)}")
            return None

    def _generate_base64_placeholder(self, vocab_item):
        """
        Generate a base64 encoded placeholder image
        """
        from PIL import Image, ImageDraw, ImageFont
        import io
        import base64

        # Create a blank image
        img = Image.new('RGB', (400, 300), color=(240, 240, 240))
        d = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        # Draw text
        d.text((50, 100), f"Japanese: {vocab_item['japanese']}", fill=(0, 0, 0), font=font)
        d.text((50, 150), f"English: {vocab_item['english']}", fill=(0, 0, 0), font=font)
        d.text((50, 200), "Placeholder Image", fill=(0, 0, 0), font=font)
        
        return img

    def _generate_local_placeholder(self, vocab_item):
        """
        Generate a local placeholder image with vocabulary details
        """
        from PIL import Image, ImageDraw, ImageFont
        
        # Create image
        img = Image.new('RGB', (512, 512), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        
        # Draw vocabulary details
        draw.text((50, 200), f"Japanese: {vocab_item['japanese']}", fill=(0,0,0), font=font)
        draw.text((50, 250), f"English: {vocab_item['english']}", fill=(0,0,0), font=font)
        draw.text((50, 300), "Image Generation Failed", fill=(255,0,0), font=font)
        
        return img

    def _create_contextual_prompt(self, vocab_item):
        """
        Create a detailed, contextual prompt for image generation
        """
        # Prompt generation strategies
        prompt_templates = [
            "A detailed illustration of {english} in a Japanese style, {additional_context}",
            "A vibrant, artistic representation of {english} with Japanese cultural elements, {additional_context}",
            "A photorealistic image of {english} in a traditional Japanese setting, {additional_context}"
        ]

        # Additional contextual elements
        additional_contexts = [
            "with soft watercolor textures",
            "in a minimalist composition",
            "with intricate Japanese design elements",
            "featuring subtle traditional patterns"
        ]

        # Select random template and context
        template = random.choice(prompt_templates)
        additional_context = random.choice(additional_contexts)

        # Format the prompt
        prompt = template.format(
            english=vocab_item['english'],
            additional_context=additional_context
        )

        return prompt

    def get_api_errors(self):
        """
        Retrieve any API errors encountered during image generation
        """
        return self.api_errors