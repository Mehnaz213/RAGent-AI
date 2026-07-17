from chatbot.retriever import retrieve_context
from chatbot.text_cleaner import clean_context
from chatbot.llm import generate_response
from chatbot.agent.prompts import KNOWLEDGE_SYSTEM_PROMPT


def generate_rag_answer(
    question: str,
    conversation_messages: list
):
    """
    Hybrid RAG Pipeline

    Returns:
        answer
        sources
    """

    # ----------------------------
    # Retrieve Context
    # ----------------------------

    context, sources = retrieve_context(question)

    context = clean_context(context)

    has_context = bool(context.strip())

    history = ""

    for message in conversation_messages[-6:]:

        history += (
            f'{message["role"]}: '
            f'{message["content"]}\n'
        )

    # ----------------------------
    # Context Available
    # ----------------------------

    if has_context:

        user_prompt = f"""
RETRIEVED DOCUMENTS

{context}

--------------------------------------------------

CONVERSATION

{history}

--------------------------------------------------

CURRENT QUESTION

{question}
"""

        system_prompt = """
You are an Enterprise AI Knowledge Assistant.

Your primary knowledge source is the retrieved documents.

Rules:

1. Read every retrieved document carefully.

2. If the answer exists in the documents,
answer directly.

3. Do NOT say
"The information was not found"
unless it truly does not exist.

4. If multiple retrieved documents contain
useful information,
combine them naturally.

5. Never invent company policies.

6. If the documents only partially answer
the question,

first answer using the documents,

then write:

## Additional General Information

and provide general knowledge.

7. Clearly separate
document knowledge
from general knowledge.

8. Use Markdown.

9. Be concise.

10. Never mention embeddings,
retrieval,
vector database,
or internal system details.
"""

    # ----------------------------
    # No Context Found
    # ----------------------------

    else:

        user_prompt = f"""
Conversation

{history}

Question

{question}
"""

        system_prompt = """
You are an AI Assistant.

No uploaded document contains the answer.

Inform the user politely.

Then provide a helpful general answer.

Begin with:

"The requested information was not found in the uploaded documents."

Then continue with:

## General Information

Never pretend the answer came from uploaded files.
"""

    try:

        answer = generate_response(

            system_prompt,

            user_prompt

        )

    except Exception as e:

        print(e)

        answer = (
            "An error occurred while generating the response."
        )

    return answer, sources