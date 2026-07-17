from chatbot.llm import generate_response


def rewrite_query(
    question: str,
    conversation_messages: list
):
    """
    Rewrites ambiguous questions by using previous
    conversation only for resolving references.
    """

    if len(conversation_messages) == 0:
        return question

    history = ""

    for message in conversation_messages[-6:]:

        history += (
            f'{message["role"]}: '
            f'{message["content"]}\n'
        )

    system_prompt = """
You are a Query Rewriter.

Your ONLY job is to rewrite ambiguous user questions.

Examples:

User:
How many days?

Rewrite:
How many days of annual leave are provided?

----------------------------

User:
What about maternity leave?

Rewrite:
What is the maternity leave policy?

----------------------------

Rules:

1. NEVER answer the question.

2. NEVER ask follow-up questions.

3. NEVER explain anything.

4. NEVER add information.

5. ONLY resolve references like:

- it
- this
- that
- they
- those
- him
- her

6. If the question is already clear,
return it unchanged.

Return ONLY the rewritten question.
"""

    prompt = f"""
Conversation History

{history}

Current Question

{question}
"""

    rewritten = generate_response(
        system_prompt,
        prompt
    )

    rewritten = rewritten.strip()

    if len(rewritten) == 0:
        return question

    return rewritten