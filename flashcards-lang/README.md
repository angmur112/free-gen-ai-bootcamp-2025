# Japanese Flashcard Learning App

A simple but powerful flashcard application to help you learn Japanese with auto-translation and image generation!

## Features

- English to Japanese automatic translation
- Automatic image generation using Unsplash API
- Local storage of flashcards in SQLite database
- Image caching for offline review
- Simple and intuitive interface
- Rate limiting to prevent API abuse
- Previous/Next navigation through flashcard deck

## Prerequisites

- Python 3.7+
- Unsplash API key (free tier available)
- Internet connection for translation and image generation

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

2. Required Python Packages (installed via requirements.txt):
   - flask (2.0.1) - Web framework
   - Pillow (8.4.0) - Image processing
   - requests (2.31.0) - HTTP requests
   - deep-translator (1.9.1) - Translation services
   - werkzeug (2.0.1) - WSGI utilities
   - click (8.0.1) - Command line interface
   - itsdangerous (2.0.1) - Security helpers
   - Jinja2 (3.0.1) - Template engine
   - MarkupSafe (2.0.1) - String handling

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd flashcards-lang
   ```

2. Create and activate virtual environment:
   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

   # Verify Python version
   python --version  # Should be 3.7 or higher
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip  # Update pip
   pip install -r requirements.txt
   ```

4. Get Unsplash API Key:
   - Sign up at https://unsplash.com/developers
   - Create a new application
   - Copy your Access Key
   - Replace `UNSPLASH_API_KEY` in `app.py` with your key

5. Create placeholder image:
   ```bash
   mkdir -p images
   curl -o images/placeholder.jpg https://via.placeholder.com/300x200.jpg?text=No+Image
   ```

6. Run the application:
   ```bash
   python app.py
   ```

## Usage

### Creating Flashcards
1. Enter an English word in the input field
2. Click "Create Flashcard"
3. The app will automatically:
   - Translate the word to Japanese
   - Generate a relevant image from Unsplash
   - Save both to your local deck

### Viewing Flashcards
1. Click "View Deck" to open the flashcard viewer
2. Use "Previous" and "Next" buttons to navigate
3. Each card shows:
   - The English word
   - Japanese translation
   - Related image

### Rate Limits
- Maximum 5 flashcard creations per minute
- Unsplash API: 50 requests per hour (free tier)

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

- If images fail to generate, check:
  - Unsplash API key configuration
  - Internet connection
  - Rate limits
- If translations fail:
  - Check internet connection
  - Verify word is in English
- If database errors occur:
  - Ensure write permissions in app directory

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
- Images: Unsplash API
- UI: Tkinter
