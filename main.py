from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from gemini_client import generate_text
from explanation_module import explain_topic
from learning_path import generate_learning_path, generate_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summarization_module import summarize_text

app = FastAPI(title="EduGenie", version="0.1.0")

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


class GeminiPromptRequest(BaseModel):
    prompt: str


class QNARequest(BaseModel):
    question: str | None = None
    input: str | None = None

    @property
    def question_text(self) -> str:
        return (self.question or self.input or "").strip()


class ExplanationRequest(BaseModel):
    topic: str | None = None
    input: str | None = None
    level: str = "beginner"

    @property
    def topic_text(self) -> str:
        return (self.topic or self.input or "").strip()


class SummaryRequest(BaseModel):
    text: str | None = None
    input: str | None = None
    focus: str = "main idea"

    @property
    def text_content(self) -> str:
        return (self.text or self.input or "").strip()


class QuizRequest(BaseModel):
    topic: str | None = None
    input: str | None = None
    num_questions: int = 3

    @property
    def topic_text(self) -> str:
        return (self.topic or self.input or "").strip()


class LearningPathRequest(BaseModel):
    subject: str | None = None
    input: str | None = None
    student_level: str = "beginner"

    @property
    def subject_text(self) -> str:
        return (self.subject or self.input or "").strip()


@app.get("/")
def index():
    return FileResponse(str(BASE_DIR / "templates" / "index.html"))


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "EduGenie"}


@app.post("/api/gemini-test")
def gemini_test(payload: GeminiPromptRequest):
    try:
        response = generate_text(payload.prompt)
        return {"response": response}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - backend guard for API failures
        raise HTTPException(status_code=500, detail="Gemini API request failed.") from exc


@app.post("/api/qna")
def qna_endpoint(payload: QNARequest):
    try:
        answer = answer_question(payload.question_text)
        return {"answer": answer}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - backend guard for API failures
        raise HTTPException(status_code=500, detail="Gemini API request failed.") from exc


@app.post("/api/explain")
def explain_endpoint(payload: ExplanationRequest):
    try:
        explanation = explain_topic(payload.topic_text, payload.level)
        return {"explanation": explanation}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - backend guard for API failures
        raise HTTPException(status_code=500, detail="Gemini API request failed.") from exc


@app.post("/api/summarize")
def summarize_endpoint(payload: SummaryRequest):
    try:
        summary = summarize_text(payload.text_content, payload.focus)
        return {"summary": summary}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - backend guard for API failures
        raise HTTPException(status_code=500, detail="Gemini API request failed.") from exc


@app.post("/api/quiz")
def quiz_endpoint(payload: QuizRequest):
    try:
        quiz = generate_quiz(payload.topic_text, payload.num_questions)
        return quiz
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - backend guard for API failures
        raise HTTPException(status_code=500, detail="Gemini API request failed.") from exc


@app.post("/api/learning-path")
def learning_path_endpoint(payload: LearningPathRequest):
    try:
        path = generate_learning_path(payload.student_level, payload.subject_text)
        return path
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - backend guard for API failures
        raise HTTPException(status_code=500, detail="Gemini API request failed.") from exc


@app.post("/api/recommendations")
def recommendations_endpoint(payload: LearningPathRequest):
    try:
        recs = generate_learning_recommendations(payload.student_level, payload.subject_text)
        return recs
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - backend guard for API failures
        raise HTTPException(status_code=500, detail="Gemini API request failed.") from exc
