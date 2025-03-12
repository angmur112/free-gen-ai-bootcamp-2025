import streamlit as st
import sys
import traceback
import random

# Import your custom modules
from src.flashcard_generator import FreeJapaneseFlashcardGenerator
from src.image_generator import FreeImageGenerator

def safe_main():
    try:
        # Streamlit Page Configuration
        st.set_page_config(
            page_title="AI Japanese Vocabulary Flashcard Generator", 
            page_icon="🇯🇵",
            layout="wide"
        )

        # Initialize Generators
        vocab_generator = FreeJapaneseFlashcardGenerator()
        image_generator = FreeImageGenerator()

        # Page Title and Description
        st.title("🇯🇵 AI-Powered Japanese Vocabulary Flashcard Generator")
        st.markdown("Generate unique AI images for Japanese vocabulary!")

        # Sidebar Filters
        st.sidebar.header("🔍 Flashcard Filters")
        
        # Category Selection
        selected_categories = st.sidebar.multiselect(
            "Select Vocabulary Categories",
            options=list(set(item['category'] for item in vocab_generator.vocabulary)),
            default=list(set(item['category'] for item in vocab_generator.vocabulary))
        )

        # Main Flashcard Generation Area
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🖼️ AI Generated Image")
            image_placeholder = st.empty()

        with col2:
            st.subheader("📝 Vocabulary Details")
            japanese_placeholder = st.empty()
            english_placeholder = st.empty()
            example_placeholder = st.empty()

        # Generate Flashcard Button
        if st.button("Generate Flashcard", type="primary"):
            # Validate category selection
            if not selected_categories:
                st.warning("Please select at least one category")
                return

            # Filter vocabulary based on selected categories
            filtered_vocab = [
                item for item in vocab_generator.vocabulary 
                if item['category'] in selected_categories
            ]

            if not filtered_vocab:
                st.error("No vocabulary found in selected categories")
                return

            # Select random vocabulary
            vocab_item = random.choice(filtered_vocab)

            # Generate Image
            image = image_generator.generate_image(vocab_item)
            
            if image:
                # Display Image 
                image_placeholder.image(image, use_container_width=True)

                # Display Vocabulary Details
                japanese_placeholder.markdown(f"**Japanese:** {vocab_item['japanese']}")
                english_placeholder.markdown(f"**English:** {vocab_item['english']}")
                example_placeholder.markdown(f"**Example:** {vocab_item['example']}")
                
                # Check and display any API errors
                api_errors = image_generator.get_api_errors()
                if api_errors:
                    st.warning("⚠️ Some image generation methods failed:")
                    for error in api_errors:
                        st.warning(error)
            else:
                st.error("Could not generate an image for this vocabulary item.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.error(traceback.format_exc())

def main():
    try:
        safe_main()
    except Exception as e:
        print(f"Critical error: {e}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()