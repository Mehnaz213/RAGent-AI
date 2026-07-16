# Import json module
import json

# Import LLM
from chatbot.llm import generate_response

# Import planner prompt
from chatbot.agent.prompts import (
    PLANNER_SYSTEM_PROMPT
)


# Generate execution plan
def classify_intent(
    user_query: str
):

    # Ask LLM to generate plan
    response = generate_response(

        PLANNER_SYSTEM_PROMPT,

        user_query

    )

    try:

        # Convert JSON string to Python object
        plan = json.loads(response)

        return plan

    except Exception:

        # Fallback

        return [

            {
                "step":1,
                "tool":"knowledge_search"
            }

        ]