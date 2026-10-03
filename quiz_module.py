import json
import re

from gemini_client import generate_text


def _build_local_quiz(topic: str, num_questions: int) -> dict:
    safe_topic = topic.strip()
    prompts = [
        (
            f"What is the main idea of {safe_topic}?",
            [
                "The main process or concept behind the topic",
                "A random unrelated fact",
                "A summary of a completely different subject",
                "A list of all vocabulary words",
            ],
            "The main process or concept behind the topic",
        ),
        (
            f"Which statement best describes {safe_topic}?",
            [
                "It connects basic ideas to a larger concept or process",
                "It is unrelated to learning",
                "It only applies to writing assignments",
                "It is a rule that must be memorized without understanding",
            ],
            "It connects basic ideas to a larger concept or process",
        ),
        (
            f"Why is understanding {safe_topic} useful?",
            [
                "It helps explain how things work in a clear, practical way",
                "It makes education unnecessary",
                "It only helps in advanced research papers",
                "It replaces all other learning methods",
            ],
            "It helps explain how things work in a clear, practical way",
        ),
        (
            f"Which answer best matches a learner-friendly explanation of {safe_topic}?",
            [
                "A simple explanation that connects the idea to everyday understanding",
                "A fully technical explanation without context",
                "A sentence with no meaning",
                "A step-by-step guide unrelated to the topic",
            ],
            "A simple explanation that connects the idea to everyday understanding",
        ),
        (
            f"What should a helpful explanation of {safe_topic} include?",
            [
                "A clear idea, an example, and a simple connection to meaning",
                "Only a definition with no explanation",
                "Only a random fact",
                "A list of unrelated terms",
            ],
            "A clear idea, an example, and a simple connection to meaning",
        ),
    ]

    questions = []
    for index in range(min(num_questions, len(prompts))):
        question, options, answer = prompts[index]
        questions.append({
            "question": question,
            "options": options,
            "answer": answer,
        })

    return {"topic": safe_topic, "questions": questions}


def generate_quiz(topic: str, num_questions: int = 5) -> dict:
    """Generate a small structured quiz for a topic, with a Gemini-first attempt and a local fallback."""
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if num_questions <= 0:
        raise ValueError("Number of questions must be greater than zero.")

    safe_topic = topic.strip()
    prompt = (
        "Generate a quiz about the topic below. Return valid JSON only with this structure: "
        "{\"topic\": \"\", \"questions\": [{\"question\": \"\", \"options\": [\"\", \"\", \"\", \"\"], \"answer\": \"\"}]}\n\n"
        f"Topic: {safe_topic}\n"
        f"Number of questions: {num_questions}"
    )

    try:
        raw_text = generate_text(prompt)
        cleaned = re.sub(r"```json\s*|```\s*", "", raw_text, flags=re.IGNORECASE).strip()
        data = json.loads(cleaned)
        if isinstance(data, dict) and "questions" in data and isinstance(data["questions"], list) and data["questions"]:
            data["topic"] = safe_topic
            return data
    except Exception:
        pass

    return _build_local_quiz(safe_topic, num_questions)
