import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gemini-flash-latest")
print("MODEL =", MODEL)

client = genai.Client(api_key=API_KEY)


def generate_response(
    system_prompt: str,
    user_prompt: str
):
    """
    Generates a response using Google Gemini.
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"""
SYSTEM INSTRUCTIONS

{system_prompt}

----------------------------------------

USER REQUEST

{user_prompt}
"""
        )

        return response.text.strip()

    except ClientError as e:
        print("Gemini API Error:", e)

        return (
            "⚠️ The AI service is temporarily unavailable because the API quota "
            "has been reached. Please try again after a short while."
        )

    except Exception as e:
        print("Unexpected Error:", e)

        return (
            "⚠️ An unexpected error occurred while generating the response."
        )