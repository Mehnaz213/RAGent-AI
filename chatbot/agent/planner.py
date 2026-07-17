import json

from chatbot.llm import generate_response


PLANNER_SYSTEM_PROMPT = """
You are an AI Planner.

Your job is ONLY to decide which tool should handle the user's request.

Available tools:

1. knowledge_search
   - Employee handbook
   - HR policies
   - Company rules
   - Benefits
   - Leave policy
   - Work from home
   - Payroll
   - Insurance
   - Holidays

2. leave_application
   - Write leave application
   - Sick leave letter
   - Casual leave letter
   - Leave request

3. email_generation
   - Professional emails
   - Reply emails
   - Formal emails

4. summarization
   - Summarize text
   - Summarize paragraph
   - Summarize article

5. rewrite
   - Rewrite sentence
   - Improve writing
   - Grammar correction

6. comparison
   - Compare two policies
   - Compare documents
   - Difference between X and Y

7. general_chat
   - Greetings
   - Small talk
   - Thank you
   - Goodbye
   - General AI questions
   - Questions unrelated to uploaded documents

Rules:

Return ONLY JSON.

Example:

[
    {
        "step": 1,
        "tool": "knowledge_search"
    }
]
"""


def classify_intent(
    user_query: str,
    conversation_messages: list | None = None
):

    history = ""

    if conversation_messages:

        for message in conversation_messages[-6:]:

            history += (
                f'{message["role"]}: '
                f'{message["content"]}\n'
            )

    prompt = f"""
Conversation

{history}

Current User Request

{user_query}
"""

    try:

        response = generate_response(
            PLANNER_SYSTEM_PROMPT,
            prompt
        )

        plan = json.loads(response)

        return plan

    except Exception:

        return [
            {
                "step": 1,
                "tool": "general_chat"
            }
        ]