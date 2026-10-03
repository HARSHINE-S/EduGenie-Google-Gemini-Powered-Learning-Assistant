from gemini_client import generate_text


def summarize_text(text: str, focus: str = "main idea") -> str:
    """Return a concise, student-friendly summary of the given text."""
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    prompt = (
        "You are a clear and helpful teacher. Summarize the text below for a student. "
        "Keep the summary concise, accurate, and easy to follow. "
        "Highlight the most important ideas and focus on the requested emphasis.\n\n"
        f"Focus: {focus or 'main idea'}\n\n"
        f"Text to summarize:\n{text}"
    )

    return generate_text(prompt)
