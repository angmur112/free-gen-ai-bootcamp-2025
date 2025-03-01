"""
JLPT Listening Practice Generator
--------------------------------
This app helps users practice JLPT listening comprehension by generating questions from YouTube videos
and providing AI-assisted understanding.

How to run:
1. Install requirements:
   pip install streamlit google-cloud-aiplatform langchain openai

2. Set up environment variables:
   export OPENAI_API_KEY=your_key
   export GOOGLE_APPLICATION_CREDENTIALS=path_to_credentials.json

3. Run the app:
   streamlit run main.py

The app will be available at http://localhost:8501
"""

# Standard library imports
import streamlit as st
import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set streamlit server settings for headless environment
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

# Debug logging
logger.debug("Starting application...")

# Add backend path to system path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.get_transcript import YouTubeTranscriptDownloader
from backend.structured_data import TranscriptParser
from backend.vector_store import QuestionStore
from backend.chat import BedrockChat

# Initialize session state variables for maintaining state between reruns
if "questions" not in st.session_state:
    st.session_state.questions = {}  # Stores all loaded questions
if "current_question" not in st.session_state:
    st.session_state.current_question = None  # Currently displayed question
if "feedback" not in st.session_state:
    st.session_state.feedback = None  # Feedback from AI assistant

def load_questions(filepath: str = "questions.json") -> Dict[str, Any]:
    """
    Load previously stored questions from JSON file
    Returns empty dict if file doesn't exist
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_question(question: Dict[str, Any], filepath: str = "questions.json"):
    """
    Save a new question to JSON file
    Generates unique ID based on timestamp
    Returns the generated question ID
    """
    questions = load_questions(filepath)
    question_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    questions[question_id] = question
    with open(filepath, 'w') as f:
        json.dump(questions, f, indent=2)
    return question_id

def render_sidebar():
    """
    Renders the sidebar containing:
    1. YouTube URL input for generating new questions
    2. Question search functionality using vector store
    3. Question selection interface
    """
    st.sidebar.title("Question Management")
    
    # YouTube URL input
    youtube_url = st.sidebar.text_input("YouTube URL")
    if youtube_url:
        if st.sidebar.button("Generate Questions from Video"):
            with st.spinner("Downloading transcript..."):
                downloader = YouTubeTranscriptDownloader()
                transcript = downloader.get_transcript(youtube_url)
                if transcript:
                    parser = TranscriptParser()
                    questions = parser.parse_transcript("\n".join([t['text'] for t in transcript]))
                    for q in questions:
                        save_question(q.to_dict())
                    st.sidebar.success(f"Generated {len(questions)} questions!")

    # Question search
    st.sidebar.subheader("Search Questions")
    search_query = st.sidebar.text_input("Search by topic or content")
    if search_query:
        store = QuestionStore()
        similar_questions = store.find_similar_questions(search_query)
        if similar_questions:
            selected = st.sidebar.selectbox(
                "Similar questions found:",
                [q.question for q in similar_questions]
            )
            if selected:
                question = next(q for q in similar_questions if q.question == selected)
                st.session_state.current_question = question

def render_main_content():
    """
    Renders the main content area containing:
    1. Current question display (if selected)
    2. Question components (introduction, conversation, question)
    3. AI assistant interface for help understanding
    """
    st.title("JLPT Listening Practice Generator")
    
    # Display current question if exists
    if st.session_state.current_question:
        question = st.session_state.current_question
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Question")
            st.write("Introduction:")
            st.write(question.introduction)
            st.write("Conversation:")
            st.write(question.conversation)
            st.write("Question:")
            st.write(question.question)
            
        with col2:
            st.subheader("AI Assistant")
            if st.button("Get Help Understanding"):
                chat = BedrockChat()
                help_prompt = f"""Help me understand this JLPT listening question:
                Introduction: {question.introduction}
                Conversation: {question.conversation}
                Question: {question.question}
                
                Please explain:
                1. Key vocabulary
                2. Main points of the conversation
                3. What the question is asking for
                """
                response = chat.generate_response(help_prompt)
                if response:
                    st.write(response)
    
    else:
        st.info("Select or generate a question to begin practice!")

def main():
    """
    Main application entry point
    Sets up page configuration and creates required directories
    Orchestrates sidebar and main content rendering
    """
    try:
        # Page config
        st.set_page_config(
            page_title="JLPT Listening Practice",
            page_icon="🎌",
            layout="wide"
        )
        
        # Create folders if they don't exist
        Path("transcripts").mkdir(exist_ok=True)
        Path("parsed_questions").mkdir(exist_ok=True)
        
        # Render sidebar and main content
        render_sidebar()
        render_main_content()
        
        logger.debug("Application running at http://localhost:8501")
        
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}", exc_info=True)
        st.error("An error occurred while starting the application")

if __name__ == "__main__":
    main()
