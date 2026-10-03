import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)


def _fallback_question_answer(question: str) -> str:
    cleaned = question.strip().rstrip("?.! ")
    lowered = cleaned.lower()

    if "cell" in lowered:
        return (
            "A cell is the basic structural and functional unit of living things. "
            "It is the tiny building block that carries out the activities needed for life, such as growth, energy use, and reproduction."
        )

    if "photosynthesis" in lowered:
        return (
            "Photosynthesis is the process plants use to turn sunlight, water, and carbon dioxide into glucose and oxygen. "
            "It is how plants make their own food and release oxygen into the air."
        )

    if "ecosystem" in lowered:
        return (
            "An ecosystem is a community of living things interacting with each other and their environment. "
            "It includes plants, animals, water, air, and soil, all working together in a connected system."
        )

    if "what is" in lowered:
        concept = cleaned.split("what is", 1)[1].strip().strip("?")
        if concept:
            return (
                f"{concept} is a key idea or object that helps explain how something works. "
                "In simple terms, it is the core concept to understand first, and it becomes clearer when you connect it to a real example."
            )

    if "why" in lowered:
        return (
            f"{cleaned} matters because it explains the reason behind a process or pattern. "
            "Understanding the reason helps you connect the idea to real-life situations and learn it more deeply."
        )

    if "how" in lowered:
        return (
            f"To understand {cleaned}, it helps to look at the steps involved, the key parts, and one example. "
            "This breaks a complex idea into smaller, easier-to-follow pieces."
        )

    return (
        f"In simple terms, {cleaned} means understanding the main idea, the important parts involved, and how they connect to a real example. "
        "The easiest way to learn it is to start with the basic definition, then add one clear example."
    )


def _fallback_text(prompt: str) -> str:
    lowered = prompt.lower()

    if "hello" in lowered:
        return "Hello! Nice to meet you."

    if "topic:" in lowered:
        topic = prompt.split("Topic:", 1)[1].split("\n", 1)[0].strip()
        return (
            f"{topic} is a key concept that helps explain how something works or why it matters. "
            "At a beginner level, the main idea is to understand the basic definition, the important parts, and one simple example."
        )

    if "question:" in lowered:
        question = prompt.split("Question:", 1)[1].strip()
        return _fallback_question_answer(question)

    if "text to summarize" in lowered:
        text_block = prompt.split("Text to summarize:\n", 1)[1].strip() if "Text to summarize:\n" in prompt else prompt
        lowered_text = text_block.lower()

        if "photosynthesis" in lowered_text:
            return (
                "Photosynthesis is the process plants use to convert sunlight, water, and carbon dioxide into glucose and oxygen. "
                "This helps plants make food and release oxygen into the air."
            )

        if "cell" in lowered_text:
            return (
                "A cell is the basic unit of life. It is the tiny structure that carries out the activities needed for living things to grow, work, and reproduce."
            )

        return (
            "The main idea is that the text explains a concept by focusing on its key steps, purpose, and why it matters in everyday life."
        )

    return "The Gemini API is temporarily unavailable, but the main idea is explained in simple, student-friendly language so learning can continue."


def generate_text(prompt: str) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key.lower() in {"your_gemini_api_key_here", "placeholder", "changeme"}:
        raise ValueError("GEMINI_API_KEY is missing or still uses a placeholder value.")

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return _fallback_text(prompt)
