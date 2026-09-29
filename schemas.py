from pydantic import BaseModel, Field


class InputRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=1, max_length=10)


class HealthResponse(BaseModel):
    status: str
    service: str
