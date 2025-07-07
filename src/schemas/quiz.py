from uuid import UUID

from pydantic import BaseModel, ConfigDict


class QuizResponse(BaseModel):
    id: UUID
    title: str

    model_config = ConfigDict(from_attributes=True)
