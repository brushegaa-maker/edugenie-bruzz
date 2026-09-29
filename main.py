from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from schemas import (
    InputRequest,
    QuizResponse,
    TextResponse,
    HealthResponse,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "EduGenie"},
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", service="EduGenie")


@app.post("/qa", response_model=TextResponse)
async def qa(payload: InputRequest):
    try:
        return TextResponse(result=answer_question(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/explain", response_model=TextResponse)
async def explain(payload: InputRequest):
    try:
        return TextResponse(result=explain_concept(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: InputRequest):
    try:
        return generate_quiz(payload.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/summarize", response_model=TextResponse)
async def summarize(payload: InputRequest):
    try:
        return TextResponse(result=summarize_text(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/learn/recommendations", response_model=TextResponse)
async def learning_recommendations(payload: InputRequest):
    try:
        return TextResponse(result=get_learning_recommendations(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
