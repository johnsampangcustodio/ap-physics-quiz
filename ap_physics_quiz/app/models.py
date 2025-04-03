from pydantic import BaseModel
from typing import Optional, List

class QuestionResponse(BaseModel):
    """Response model for a question"""
    id: int
    text: str
    options: Optional[List[str]] = None

class AnswerRequest(BaseModel):
    """Request model for submitting an answer"""
    question_id: int
    answer: str 