# Import the OpenAI client from the openai package
from openai import OpenAI
# Import dotenv to load environment variables
from dotenv import load_dotenv
# Import the os module to read environment variables
import os
# Import the function used to retrieve relevant document context
from chatbot.retriever import retrieve_context

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
            "You are an Enterprise AI Knowledge Assistant.\n"
            "Answer the user's question only using the provided context.\n"
            "If the answer is not present in the context, clearly state that the information is not available in the provided document.\n"
            "Do not make up or assume information.\n"
            "Provide clear, professional, and concise responses."
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
    # Retrieve context only from the HR Policy Manual
    context, retrieved_metadata = retrieve_context(
       user_input,
       source="HR_Policy_Manual.pdf"
    )
    # Add the user's question along with the retrieved context
    chat_history.append(
        {
        "role": "user",
        "content": (
            f"""Context:
    {context}
    Question:
    {user_input}
    """
           )
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
    # Get all unique source documents
    sources = {
        item["source"]
        for item in retrieved_metadata
    }
    # Display the source documents used to answer the question
    print("\n📄 Sources:")

    for source in sources:
        print(f"- {source}")