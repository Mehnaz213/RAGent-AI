# Import LLM response generator
from chatbot.llm import generate_response

# Import prompts
from chatbot.agent.prompts import (
    LEAVE_SYSTEM_PROMPT,
    EMAIL_TEMPLATE_PROMPT,
    COMPARISON_SYSTEM_PROMPT,
    SUMMARY_SYSTEM_PROMPT,
    REWRITE_SYSTEM_PROMPT,
    LETTER_SYSTEM_PROMPT,
    REPORT_SYSTEM_PROMPT,
    NOTICE_SYSTEM_PROMPT,
    PROPOSAL_SYSTEM_PROMPT,
)


# Build prompt using previous tool output
def build_prompt(
    user_query: str,
    previous_output: str | None,
    task: str
):

    if previous_output:

        return f"""
User Request:

{user_query}

Context:

{previous_output}

Task:

{task}
"""

    return user_query


# -----------------------------
# Knowledge Search Tool
# -----------------------------
def knowledge_search_tool(
    user_query: str,
    previous_output=None
):

    # Existing RAG pipeline will handle this.
    return user_query


# -----------------------------
# Leave Application Tool
# -----------------------------
def leave_application_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the leave application."
    )

    return generate_response(
        LEAVE_SYSTEM_PROMPT,
        prompt
    )


# -----------------------------
# Email Generator Tool
# -----------------------------
def email_generation_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the email."
    )

    return generate_response(
        EMAIL_TEMPLATE_PROMPT,
        prompt
    )


# -----------------------------
# Summarization Tool
# -----------------------------
def summarization_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the summary."
    )

    return generate_response(
        SUMMARY_SYSTEM_PROMPT,
        prompt
    )


# -----------------------------
# Rewrite Tool
# -----------------------------
def rewrite_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Rewrite the text professionally."
    )

    return generate_response(
        REWRITE_SYSTEM_PROMPT,
        prompt
    )


# -----------------------------
# Comparison Tool
# -----------------------------
def comparison_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the comparison."
    )

    return generate_response(
        COMPARISON_SYSTEM_PROMPT,
        prompt
    )


# -----------------------------
# Letter Generation Tool
# -----------------------------
def letter_generation_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the letter."
    )

    return generate_response(
        LETTER_SYSTEM_PROMPT,
        prompt
    )


# -----------------------------
# Report Generation Tool
# -----------------------------
def report_generation_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the report."
    )

    return generate_response(
        REPORT_SYSTEM_PROMPT,
        prompt
    )


# -----------------------------
# Notice Generation Tool
# -----------------------------
def notice_generation_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the notice."
    )

    return generate_response(
        NOTICE_SYSTEM_PROMPT,
        prompt
    )


# -----------------------------
# Proposal Generation Tool
# -----------------------------
def proposal_generation_tool(
    user_query: str,
    previous_output=None
):

    prompt = build_prompt(
        user_query,
        previous_output,
        "Generate ONLY the proposal."
    )

    return generate_response(
        PROPOSAL_SYSTEM_PROMPT,
        prompt
    )