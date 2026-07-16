# Import planner
from chatbot.agent.planner import classify_intent

# Import tools
from chatbot.agent.tools import (
    knowledge_search_tool,
    leave_application_tool,
    email_generation_tool,
    summarization_tool,
    rewrite_tool,
    comparison_tool
)


# Process user request
def process_user_request(

    user_query: str,

    previous_output: str | None = None

):

    # Agent reasoning steps
    steps = []

    # Generate execution plan
    plan = classify_intent(user_query)

    # Store results
    current_output = None

    steps.append("Analyzing request...")

    for item in plan:

        tool = item["tool"]


        # Knowledge Search
        if tool == "knowledge_search":

            steps.append("Searching Knowledge Base")

            current_output=knowledge_search_tool(
                user_query,

               previous_output=current_output or previous_output

            )

        # Leave Generator
        elif tool == "leave_application":

            steps.append("Generating Leave Application")

            current_output = leave_application_tool(

               user_query,

               previous_output=current_output or previous_output

            )

        # Email Generator
        elif tool == "email_generation":

            steps.append("Generating Email")

            current_output= email_generation_tool(
                user_query,

               previous_output=current_output or previous_output

            )

        # Summary
        elif tool == "summarization":

            steps.append("Summarizing Content")

            current_output= summarization_tool(
                user_query,

               previous_output=current_output or previous_output

            )

        # Rewrite
        elif tool == "rewrite":

            steps.append("Rewriting Text")

            current_output= rewrite_tool(
                user_query,

               previous_output=current_output or previous_output

            )

        # Comparison
        elif tool == "comparison":

            steps.append("Comparing Policies")

            current_output = comparison_tool(
                user_query,

               previous_output=current_output or previous_output

            )

    return {

      "tools": [

        item["tool"]

        for item in plan

      ],

      "steps": steps,

      "result": current_output

    }