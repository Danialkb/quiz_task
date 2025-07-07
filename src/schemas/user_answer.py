from uuid import UUID

from pydantic import BaseModel


class UserAnswerCreateSchema(BaseModel):
    question_id: UUID
    quiz_session_id: UUID
    options: list[UUID]


class UserAnswerCreateResponse(BaseModel):
    question_id: UUID
    quiz_session_id: UUID
    selected_options: list[UUID]
    correct_options: list[UUID]
    is_correct: bool
