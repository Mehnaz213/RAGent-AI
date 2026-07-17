from chatbot.rag import generate_rag_answer

print("=" * 60)
print("Enterprise AI Knowledge Assistant (Ollama)")
print("Type 'exit' to quit")
print("=" * 60)

conversation_messages = []

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    answer, sources = generate_rag_answer(
        question=question,
        conversation_messages=conversation_messages
    )

    print("\nAssistant:")
    print(answer)

    conversation_messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    conversation_messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    if sources:

        print("\nSources:")

        unique_sources = []

        for source in sources:

            filename = source.get("source", "Unknown")

            if filename not in unique_sources:
                unique_sources.append(filename)

        for filename in unique_sources:
            print(f"- {filename}")