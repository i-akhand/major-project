from pydantic import BaseModel
from typing import List, Optional

class AnswerBase(BaseModel):
    question: str
    answer: str
    document_id: int

class Answer(AnswerBase):
    id: int

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    filename: str
    filepath: str
    content: str

class Document(DocumentBase):
    id: int
    answers: List[Answer] = []

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    question: str
    document_id: int
