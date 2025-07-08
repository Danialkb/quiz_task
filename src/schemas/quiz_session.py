from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from schemas.quiz import QuizResponse


class QuizSessionCreateSchema(BaseModel):
    quiz_id: UUID


class QuizSessionCreateResponse(BaseModel):
    id: UUID
    quiz_id: UUID
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)


class QuizSessionResponse(BaseModel):
    id: UUID
    quiz: QuizResponse
    user_id: UUID
    correct_answers: int
    questions_count: int
    created_at: datetime
    finished_at: Optional[datetime]
    score: float = 0

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("score")
    def serialize_score(self, value: float) -> float:
        try:
            return round(self.correct_answers / self.questions_count, 2) * 100
        except ZeroDivisionError:
            return value


class QuizSessionFinishedResponse(BaseModel):
    id: UUID
    quiz_id: UUID
    user_id: UUID
    correct_answers: int
    questions_count: int
    created_at: datetime
    finished_at: datetime
    score: float = 0
    bonus_points: int = 0

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("score")
    def serialize_score(self, value: float) -> float:
        try:
            return round(self.correct_answers / self.questions_count, 2) * 100
        except ZeroDivisionError:
            return value
