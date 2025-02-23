import boto3
import json

MODEL_ID = "amazon.nova-micro-v1:0"  # Replace with your desired Bedrock model ID
BEDROCK_REGION = "us-east-1"  # Replace with your Bedrock region

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=BEDROCK_REGION
)

def invoke_bedrock_model(prompt):
    """
    Invokes the Bedrock model with the given prompt.
    """
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 200,
        "temperature": 0.5,
        "top_p": 0.9
    })

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read().decode())
    return response_body["completion"]

def main():
    """
    Main function to run the chatbot.
    """
    print("Welcome to the Bedrock Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        prompt = f"User: {user_input}\nChatbot:"
        response = invoke_bedrock_model(prompt)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
