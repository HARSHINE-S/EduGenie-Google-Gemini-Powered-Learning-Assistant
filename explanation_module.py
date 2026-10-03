from gemini_client import generate_text


def explain_topic(topic: str, level: str = "beginner") -> str:
    """Return a clear, beginner-friendly explanation for a topic."""
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    prompt = (
        "You are a patient, encouraging teacher. "
        "Explain the topic clearly for a learner at the requested level. "
        "Use simple language, concrete examples, and short paragraphs. "
        "Do not use heavy jargon unless you explain it.\n\n"
        f"Topic: {topic}\n"
        f"Learning level: {level or 'beginner'}\n\n"
        "Please provide a friendly explanation that helps the student understand the idea, why it matters, and a simple example."
    )

    return generate_text(prompt)
