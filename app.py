from openai import OpenAI
from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()
# Read the API key from the .env file
api_key=os.getenv("OPENROUTER_API_KEY")
# Read the model name from the .env file
model = os.getenv("OPENROUTER_MODEL")
# Create the OpenAI client object
client=OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
    )
# Store the complete conversation history &
# Initialize the conversation with system instructions
chat_history = [
    {
        "role": "system",
        "content": (
            "You are an Enterprise AI Knowledge Assistant. "
            "Provide professional and helpful responses. "
            "If you don't know the answer, clearly say so instead of making up information."
        )
    }
]
# Keep the chatbot running until the user exits
while True:

    # Take a question from the user
    user_input = input("YOU: ")

    # Exit the chatbot if the user types 'exit'
    if user_input.lower() == "exit":
        print("Goodbye! 👋")
        break

    # Add the user's message to the conversation history
    chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Send the conversation history to the AI model
    response = client.chat.completions.create(
        model=model,
        messages=chat_history #retrives the chat history and sends it to the model for context
    )

    # Store the AI's response
    ai_response = response.choices[0].message.content

    # Add the AI's response to the conversation history
    chat_history.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    # Display the AI's response
    print(ai_response)