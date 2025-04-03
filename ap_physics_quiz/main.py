import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
import random
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, init_db, Question
from app.models import QuestionResponse, AnswerRequest

app = FastAPI(title="AP Physics C Mechanics Quiz")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Store current user's score in memory (would use sessions in production)
user_score = 0
current_question_id = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage with welcome message and start button"""
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request, db: AsyncSession = Depends(get_db)):
    """Get a random question and display it to the user"""
    global user_score, current_question_id
    
    # Get a random question from the database
    questions = await Question.get_all(db)
    if not questions:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": "No questions available in the database."}
        )
    
    question = random.choice(questions)
    current_question_id = question.id
    
    return templates.TemplateResponse(
        "quiz.html", 
        {
            "request": request, 
            "question": question,
            "score": user_score,
            "options": question.options.split("|") if question.options else None
        }
    )

@app.post("/submit", response_class=HTMLResponse)
async def submit_answer(
    request: Request,
    answer: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Check the user's answer and provide feedback"""
    global user_score, current_question_id
    
    if current_question_id is None:
        return RedirectResponse(url="/quiz", status_code=303)
    
    question = await Question.get_by_id(db, current_question_id)
    if not question:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": "Question not found."}
        )
    
    # Simple check for correct answer
    is_correct = answer.strip().lower() == question.correct_answer.strip().lower()
    
    if is_correct:
        user_score += 1
    
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "is_correct": is_correct,
            "question": question,
            "user_answer": answer,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "score": user_score
        }
    )

@app.post("/reset")
async def reset_score():
    """Reset the user's score and start a new quiz"""
    global user_score, current_question_id
    user_score = 0
    current_question_id = None
    return RedirectResponse(url="/quiz", status_code=303)

# API routes for potential frontend integration
@app.get("/api/question", response_model=QuestionResponse)
async def get_random_question(db: AsyncSession = Depends(get_db)):
    """API endpoint to get a random question"""
    questions = await Question.get_all(db)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available")
    
    question = random.choice(questions)
    return QuestionResponse(
        id=question.id,
        text=question.text,
        options=question.options.split("|") if question.options else None
    )

@app.post("/api/answer")
async def check_answer(answer_req: AnswerRequest, db: AsyncSession = Depends(get_db)):
    """API endpoint to check an answer"""
    question = await Question.get_by_id(db, answer_req.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    is_correct = answer_req.answer.strip().lower() == question.correct_answer.strip().lower()
    
    return {
        "correct": is_correct,
        "correct_answer": question.correct_answer if not is_correct else None,
        "explanation": question.explanation if not is_correct else None
    }

@app.get("/api/score")
async def get_score():
    """API endpoint to get the current score"""
    return {"score": user_score}

@app.post("/api/restart")
async def restart_quiz():
    """API endpoint to restart the quiz"""
    global user_score
    user_score = 0
    return {"message": "Quiz restarted", "score": user_score}

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup"""
    await init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 