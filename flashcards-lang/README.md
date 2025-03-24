# Japanese Flashcard Learning App

A simple but powerful flashcard application to help you learn Japanese with auto-translation and AI image generation!

## Features

- English to Japanese automatic translation with multiple formats:
  - Kanji (漢字)
  - Kana (かな)
  - Romaji
- AI-powered image generation using Stable Diffusion
- Local storage of flashcards in SQLite database
- Image caching for offline review
- Simple and intuitive interface
- Rate limiting to prevent API abuse
- Previous/Next navigation through flashcard deck

## Prerequisites

- Python 3.7+
- Hugging Face account and API token
- Internet connection for translation and image generation
- At least 4GB RAM for Stable Diffusion (CPU mode)

## Python Environment Setup

1. Required System Packages:
   ```bash
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3-tk python3-pip python3-venv

   # For macOS
   brew install python3 python-tk

   # For Windows
   # Python and tkinter are usually bundled together
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install PyTorch (CPU version):
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

4. Install other dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Hugging Face Setup

1. Create account at huggingface.co
2. Get access token from huggingface.co/settings/tokens
3. Login via CLI:
   ```bash
   huggingface-cli login
   # Enter your token when prompted
   ```
4. Replace `HF_TOKEN` in app.py with your token

## Usage

### Creating Flashcards
1. Enter an English word in the input field
2. Click "Create Flashcard"
3. The app will automatically:
   - Translate the word to Japanese (Kanji, Kana, and Romaji)
   - Generate an AI image using Stable Diffusion
   - Save both to your local deck

### Viewing Flashcards
1. Click "View Deck" to open the flashcard viewer
2. Use "Previous" and "Next" buttons to navigate
3. Each card shows:
   - The English word
   - Japanese translations in three formats
   - AI-generated image

### Rate Limits
- Maximum 5 flashcard creations per minute
- Image generation may take 15-30 seconds on CPU

## File Structure

```
flashcards-lang/
├── app.py              # Main application code
├── flashcards.db       # SQLite database (auto-created)
├── images/            # Generated images directory
│   └── placeholder.jpg # Fallback image
└── requirements.txt    # Python dependencies
```

## Troubleshooting

- If Stable Diffusion fails:
  - Verify Hugging Face token is correct
  - Ensure enough RAM is available
  - Check internet connection
  
- If Japanese text doesn't display:
  - Install Japanese fonts:
    ```bash
    # Ubuntu/Debian
    sudo apt-get install fonts-noto-cjk
    ```
  - Try alternative fonts in app.py:
    - 'Noto Sans CJK JP'
    - 'MS Gothic'
    - 'TakaoGothic'
    - 'IPAGothic'

- For memory issues:
  - Use smaller Stable Diffusion model
  - Reduce inference steps
  - Enable CPU offloading

- If tkinter is not found:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  
  # macOS
  brew install python-tk@3.9  # Replace 3.9 with your Python version
  ```

- If pip install fails:
  - Try updating pip: `pip install --upgrade pip`
  - Install packages individually: `pip install package-name==version`
  - Check Python version compatibility

- If module not found errors occur:
  - Verify virtual environment is activated
  - Confirm all requirements are installed: `pip list`
  - Try reinstalling requirements: `pip install -r requirements.txt --force-reinstall`

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License.

## Credits

- Translation: Google Translate API via deep-translator
- Image Generation: Stable Diffusion via Hugging Face
- Japanese Text Processing: pykakasi
- UI: Tkinter
