# 🇯🇵 Japanese Vocabulary Flashcard Generator

## 📘 Project Overview

An AI-powered Streamlit application designed to help Japanese language learners practice vocabulary through interactive flashcards. The app generates AI-created images for JLPT N5 level Japanese words using multiple image generation services.

## ✨ Key Features

- 🎴 Interactive Japanese Vocabulary Flashcards
- 🖼️ AI Image Generation via Hugging Face Stable Diffusion
- 🔄 Multiple Image Generation Fallbacks (Unsplash, Local Placeholder)
- 📊 Basic Spaced Repetition System
- 🔍 Category-based Vocabulary Filtering
- 📱 Responsive Streamlit Interface

## 🛠 Technical Architecture

### Core Components
- **app.py**: Main Streamlit application interface
- **flashcard_generator.py**: Japanese vocabulary management
- **image_generator.py**: Multi-source image generation handling
- **utils.py**: Spaced repetition and utility functions

### Technology Stack
- **Frontend Framework**: Streamlit
- **Programming Language**: Python 3.8+
- **Image Generation**: Hugging Face Stable Diffusion API
- **Fallback Services**: Unsplash API
- **Environment Management**: python-dotenv

### External APIs
- Hugging Face Stable Diffusion
- Unsplash Image Service
- (Optional) Dezgo API Integration

## 📋 Prerequisites

- Python 3.8 or higher
- Hugging Face API token
- 2GB RAM minimum
- Internet connection for API services

## 🚀 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/japanese-flashcard-generator.git
cd flashcard
```

2. **Set Up Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
Create a `.env` file:
```
HUGGINGFACE_API_TOKEN=your_token_here
```

## 🖥️ Usage

1. **Start the Application**
```bash
streamlit run app.py
```

2. **Using the Flashcard System**
- Select vocabulary categories from the sidebar
- Click "Generate Flashcard" for new cards
- View AI-generated images and vocabulary details
- Track your learning progress with the spaced repetition system

## 🔧 Configuration

### Image Generation Priority
1. Hugging Face Stable Diffusion API
2. Unsplash Image Service
3. Local Placeholder Generation

### Vocabulary Categories
- Nouns
- Verbs
- (Add more categories as needed)

## 🤝 Acknowledgments

- Hugging Face for AI image generation
- Unsplash for backup image service
- Streamlit for the web framework
- JLPT N5 vocabulary resources