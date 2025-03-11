import gradio as gr
import requests
from requests.exceptions import RequestException
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_backend():
    try:
        response = requests.get("http://localhost:8001/")
        return response.status_code == 200
    except:
        return False

def generate_flashcard():
    if not check_backend():
        logger.error("Backend is not running")
        return gr.Image(value=None, label="Error: Backend is not running. Start it with 'uvicorn main:app --reload'")

    try:
        logger.debug("Attempting to connect to backend API...")
        response = requests.get("http://localhost:8001/flashcards/")
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        
        if response.status_code != 200:
            logger.error(f"Backend API error: {response.status_code}")
            return gr.Image(value=None, label=f"Backend error: {response.status_code}")
        
        data = response.json()
        logger.debug(f"Parsed JSON data: {data}")
        
        if "status" not in data or data["status"] != "success":
            logger.error("Invalid response format")
            return gr.Image(value=None, label="Invalid response from backend")
        
        flashcard = data["flashcard"]
        return gr.Image(value=flashcard["image_url"], label=flashcard["vocabulary"]["japanese"])
    
    except requests.ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        return gr.Image(value=None, label="Could not connect to backend")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return gr.Image(value=None, label=f"Error: {str(e)}")

demo = gr.Interface(
    fn=generate_flashcard,
    inputs=None,
    outputs=gr.Image(type="filepath"),
    title="Japanese Flashcards",
    description="Study Japanese vocabulary with flashcards",
    refresh=True
)

if __name__ == "__main__":
    logger.info("Starting Gradio interface...")
    demo.launch(show_api=False)