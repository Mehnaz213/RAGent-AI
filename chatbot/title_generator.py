from chatbot.llm import generate_response


def generate_title(first_message: str) -> str:
    """
    Generates a short conversation title.
    """

    system_prompt = """
You generate short chat titles.

Rules:
- Maximum 5 words.
- No quotation marks.
- No punctuation at the end.
- Return only the title.
"""

    try:
        title = generate_response(
            system_prompt=system_prompt,
            user_prompt=first_message
        )

        return title.strip()

    except Exception:
        return first_message[:40]