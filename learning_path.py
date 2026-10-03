from gemini_client import generate_text


def generate_learning_path(student_level: str, subject: str) -> dict:
    """Return a clear beginner-to-advanced learning path for a subject."""
    if not subject or not subject.strip():
        raise ValueError("Subject cannot be empty.")

    safe_subject = subject.strip()
    safe_level = (student_level or "beginner").strip() or "beginner"

    prompt = (
        "Create a structured learning path for a student. "
        "Return valid JSON only with this exact structure: "
        "{\"subject\": \"\", \"student_level\": \"\", \"steps\": [\"step 1\", \"step 2\", \"step 3\"]}\n\n"
        f"Subject: {safe_subject}\n"
        f"Student level: {safe_level}\n\n"
        "Give a short beginner-to-advanced sequence with clear learning milestones."
    )

    try:
        response = generate_text(prompt)
        if response:
            import json
            import re

            cleaned = re.sub(r"```json\s*|```\s*", "", response, flags=re.IGNORECASE).strip()
            data = json.loads(cleaned)
            if isinstance(data, dict) and "steps" in data and isinstance(data["steps"], list) and data["steps"]:
                data["subject"] = safe_subject
                data["student_level"] = safe_level
                return data
    except Exception:
        pass

    steps = [
        f"Start with the basic definition of {safe_subject}.",
        f"Learn the key parts or processes involved in {safe_subject}.",
        f"Practice using simple examples and questions about {safe_subject}.",
        f"Apply {safe_subject} in a real scenario or challenge.",
        f"Move to deeper analysis, comparisons, and advanced applications of {safe_subject}.",
    ]

    return {"subject": safe_subject, "student_level": safe_level, "steps": steps[:3] if safe_level.lower() == "beginner" else steps}


def generate_learning_recommendations(student_level: str, subject: str) -> dict:
    """Return a short list of study recommendations for a subject."""
    if not subject or not subject.strip():
        raise ValueError("Subject cannot be empty.")

    safe_subject = subject.strip()
    safe_level = (student_level or "beginner").strip() or "beginner"

    recommendations = [
        f"Start by reviewing the main idea behind {safe_subject} in simple terms.",
        f"Practice with 3 short questions or examples that use {safe_subject} in context.",
        f"Summarize what you learned in your own words to check understanding.",
        f"Ask one deeper question about how {safe_subject} connects to real life or another topic.",
    ]

    if safe_level.lower() in {"advanced", "expert"}:
        recommendations = [
            f"Compare {safe_subject} with a related concept to strengthen your understanding.",
            f"Apply {safe_subject} to a real problem and explain your reasoning clearly.",
            f"Challenge yourself with higher-level questions and scenarios involving {safe_subject}.",
            f"Teach the idea of {safe_subject} to someone else to check mastery.",
        ]

    return {"subject": safe_subject, "student_level": safe_level, "recommendations": recommendations}
