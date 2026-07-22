# modules/llm.py

def build_prompt(context, question):
    return f"""
    You are RepoPilot, an AI assistant specialized in understanding GitHub repositories.

    Instructions:
    - Answer ONLY using the provided repository context.
    - If the answer is not present, say:
      "I couldn't find that information in the repository."
    - Mention relevant file names whenever possible.
    - Do not invent code or functionality.

    Repository Context:
    {context}

    User Question:
    {question}

    Answer:
    """

import ollama


def generate_answer(context_chunks, question):
    """
    Generate answer using LLM
    """

    # Combine context
    context = "\n\n".join(
        [f"{chunk['metadata'].get('file_path', '')}:\n{chunk['content']}"
         for chunk in context_chunks]
    )

    prompt = build_prompt(context, question)

    response = ollama.chat(
        model="llama3.2:latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]