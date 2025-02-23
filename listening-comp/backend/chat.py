import boto3
import json
import streamlit as st
from typing import Optional, Dict, Any

MODEL_ID = "amazon.nova-lite-v1:0"  # Replace with your desired Bedrock model ID
BEDROCK_REGION = "us-east-1"  # Replace with your Bedrock region

class BedrockChat:
    def __init__(self, model_id: str = MODEL_ID):
        """Initialize Bedrock chat client"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)
        self.model_id = model_id

    def generate_response(self, message: str, inference_config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Generate a response using Amazon Bedrock"""
        if not message:
            st.error("Error: Message cannot be empty.")
            return None

        if inference_config is None:
            inference_config = {"temperature": 0.7}

        messages = [{
            "role": "user",
            "content": [{"text": message}]
        }]

        try:
            print(f"Sending request to Bedrock with model ID: {self.model_id}, message: {message}")  # Debugging statement
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            print(f"Received response from Bedrock: {response}")  # Debugging statement
            return response['output']['message']['content'][0]['text']
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}, type: {type(e)}")
            return None

def main():
    """
    Main function to run the chatbot using Streamlit.
    """
    st.title("Bedrock Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What's up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get the chatbot's response
        chat = BedrockChat()
        try:
            response = chat.generate_response(prompt)
        except Exception as e:
            st.error(f"Failed to generate response: {e}")
            response = None

        if response:
            # Add chatbot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Display the chatbot's response
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.warning("No response received from the chatbot.")

if __name__ == "__main__":
    main()
