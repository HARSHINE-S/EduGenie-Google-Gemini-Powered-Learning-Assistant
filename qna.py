from gemini_client import generate_text


def answer_question(question: str) -> str:
    """Return a clear, learner-friendly answer to a question."""
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = (
        "You are a patient and supportive teacher. "
        "Answer the student's question clearly, simply, and in a friendly way. "
        "Use beginner-friendly explanations when needed and avoid unnecessary jargon.\n\n"
        f"Question: {question}"
    )

    return generate_text(prompt)
