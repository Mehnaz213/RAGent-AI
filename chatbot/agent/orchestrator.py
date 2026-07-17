# Import planner
from chatbot.agent.planner import classify_intent

from chatbot.agent.reflection import reflect_response
from chatbot.llm import generate_response

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

    conversation_messages: list | None = None,

    previous_output: str | None = None

):

    # Agent reasoning steps
    steps = []

    # Generate execution plan
    plan = classify_intent(

       user_query=user_query,

       conversation_messages=conversation_messages or []

    )

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

            )

        # Leave Generator
        elif tool == "leave_application":

            steps.append("Generating Leave Application")

            current_output = leave_application_tool(

               user_query,

            )

        # Email Generator
        elif tool == "email_generation":

            steps.append("Generating Email")

            current_output= email_generation_tool(
                user_query,

            )

        # Summary
        elif tool == "summarization":

            steps.append("Summarizing Content")

            current_output= summarization_tool(
                user_query,

            )

        # Rewrite
        elif tool == "rewrite":

            steps.append("Rewriting Text")

            current_output= rewrite_tool(
                user_query,

            )

        # Comparison
        elif tool == "comparison":

            steps.append("Comparing Policies")

            current_output = comparison_tool(
                user_query,


            )
        
        elif tool == "general_chat":

            steps.append("Generating Response")

            current_output = generate_response(
               "You are a helpful AI assistant.",
               user_query
            )

    reflection = reflect_response(
    tools=[item["tool"] for item in plan],
    result=current_output
    )
    print("Reflection:", reflection)
    steps.append(
       reflection.get(
        "message",
        "Reflection completed."
       )
    )
    if reflection.get("needs_followup", False):

       return {

          "tools": [
            item["tool"]
            for item in plan
           ],

          "steps": steps,

          "result": reflection.get("followup_question", "")

       }
    
    return {

      "tools": [

        item["tool"]

        for item in plan

      ],

      "steps": steps,

      "result": current_output

    }
