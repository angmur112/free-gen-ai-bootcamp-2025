# Japanese Flashcard Learning App

Hey there! This is my Japanese learning app that creates flashcards using AI. I built it to help myself learn Japanese vocabulary with visual aids that actually make sense.

## What it does

This app takes English words you enter, translates them to Japanese, and creates flashcards with AI-generated images. The cards are saved locally so you can review them anytime, even offline.

## Features

- Automatic English → Japanese translation showing:
  - Proper Japanese characters (漢字)
  - Phonetic kana (かな) so you know how to pronounce it
  - Romanized text so absolute beginners can read it too
- Cool AI images for each word using Hugging Face's Stable Diffusion models
- Smart handling of duplicate words (shows you the existing card instead of creating duplicates)
- Local storage so your flashcards don't disappear when you close the app
- Simple interface that doesn't get in your way
- Deck viewer with next/previous navigation

## What You'll Need

- Python 3.7+ installed on your computer
- A free Hugging Face account for the image generation API
- Internet connection (for translation and generating new images)
- About 4GB of free RAM if running Stable Diffusion locally

## Setting Things Up

1. First, install these system packages:
   ```bash
   # Ubuntu/Debian users
   sudo apt-get update
   sudo apt-get install python3-tk python3-pip python3-venv

   # Mac users
   brew install python3 python-tk

   # Windows users - you probably already have what you need if Python is installed
   ```

2. Set up a virtual environment (keeps things clean):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows folks: venv\Scripts\activate
   ```

3. Install PyTorch (the lightweight CPU version):
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

4. Install everything else needed:
   ```bash
   pip install -r requirements.txt
   ```

5. Hugging Face setup:
   - Create an account at huggingface.co if you don't have one
   - Go to huggingface.co/settings/tokens and create a new token
   - Run `huggingface-cli login` and paste your token when asked
   - Open app.py and replace the HF_TOKEN value with your token

## Using the App

Once you're all set up, it's pretty straightforward:

### Making New Flashcards
1. Type an English word in the box
2. Hit "Create Flashcard"
3. Wait a few seconds while the app:
   - Translates your word to Japanese
   - Creates an image that represents the word
   - Saves everything to your collection

### Looking Through Your Cards
1. Click "View Deck" to see all your cards
2. Use the "Previous" and "Next" buttons to flip through them
3. Each card shows you:
   - The English word
   - The Japanese translations in all three formats
   - The AI-generated image to help you remember

### Good to Know
- You can only create 5 cards per minute (to avoid API abuse)
- Images might take 15-30 seconds to generate, especially on the first run
- If you enter a word you've already created a card for, the app will show you the existing card

## Files and Folders

```
flashcards-lang/
├── app.py              # The main program code
├── flashcards.db       # Where your cards get saved
├── images/             # Folder with all the generated images
│   └── placeholder.jpg # Backup image if generation fails
└── requirements.txt    # List of Python packages needed
```

## Troubleshooting

If something's not working right, check these common issues:

- **Images aren't generating:** Make sure your Hugging Face token is working and you have a good internet connection

- **Japanese text looks like boxes:** You need Japanese fonts installed:
  ```bash
  sudo apt-get install fonts-noto-cjk  # For Ubuntu/Debian
  ```

- **App crashes or freezes:** You might be low on memory. Try using a smaller model or closing other applications

- **Can't find tkinter:** Install it with:
  ```bash
  sudo apt-get install python3-tk  # Ubuntu/Debian
  brew install python-tk@3.9       # Mac (match your Python version)
  ```

- **Weird package errors:** Try updating pip and reinstalling:
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt --force-reinstall
  ```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License.

## Credits

- Translation: Google Translate API via deep-translator
- Image Generation: Stable Diffusion via Hugging Face
- Japanese Text Processing: pykakasi
- UI: Tkinter
