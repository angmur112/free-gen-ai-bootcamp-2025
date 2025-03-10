# Japanese Flashcard Generator

## Overview
This application is a Japanese language learning tool that generates random Japanese vocabulary flashcards using OpenAI and provides a user-friendly interface with Gradio.

## Features
- Generate random Japanese vocabulary words (JLPT N5 level)
- Translate words to English
- Simple web interface for interaction

## Prerequisites
- Python 3.8+
- OpenAI API Key
- Internet Connection

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/japanese-flashcard-app.git
cd japanese-flashcard-app
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up OpenAI API Key
You need to set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```

### 5. Running the Application
Start the FastAPI Backend:
```bash
uvicorn main:app --reload
```

Start the Gradio Frontend:
```bash
python ui.py
```

## Usage
1. Once the application is running, navigate to http://127.0.0.1:7860 in your web browser
2. The Gradio interface will be displayed
3. Click the "Run" button to generate a new Japanese flashcard

## Troubleshooting
- Ensure you have a valid OpenAI API key
- Check that all dependencies are correctly installed
- Verify your internet connection

## Technologies Used
- Python
- FastAPI
- Gradio
- OpenAI API