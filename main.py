from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import ask_gemini
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path


app = FastAPI(title="EduGenie Learning Assistant")


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/qa")
async def qa(data: dict):

    question = data.get("question", "")

    answer = ask_gemini(question)

    return {
        "answer": answer
    }


@app.post("/explain")
async def explain(data: dict):

    topic = data.get("topic", "")

    answer = explain_topic(topic)

    return {
        "explanation": answer
    }


@app.post("/quiz")
async def quiz(data: dict):

    topic = data.get("topic", "")

    quiz_data = generate_quiz(topic)

    return quiz_data


@app.post("/summarize")
async def summarize(data: dict):

    text = data.get("text", "")

    summary = summarize_text(text)

    return {
        "summary": summary
    }


@app.post("/learn/recommendations")
async def learning_recommendations(data: dict):

    topic = data.get("topic", "")

    path = recommend_learning_path(topic)

    return {
        "learning_path": path
    }
