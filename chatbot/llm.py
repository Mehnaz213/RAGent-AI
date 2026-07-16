# Import OpenAI client
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv

# Import os module
import os

# Read the .env file
load_dotenv()

# Read OpenRouter API Key
api_key = os.getenv("OPENROUTER_API_KEY")

# Read OpenRouter model name
model = os.getenv("OPENROUTER_MODEL")

# Create OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Generate AI Response
def generate_response(
    system_prompt: str,
    user_prompt: str
):
    """
    Sends a prompt to the LLM
    and returns the generated response.
    """

    # Generate response using OpenRouter
    response = client.chat.completions.create(

        # AI Model
        model=model,

        # Lower temperature for consistent responses
        temperature=0,

        # Conversation messages
        messages=[

            # System Prompt
            {
                "role": "system",
                "content": system_prompt
            },

            # User Prompt
            {
                "role": "user",
                "content": user_prompt
            }

        ]
    )

    # Return only the generated text
    return response.choices[0].message.content