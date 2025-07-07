from uuid import UUID

from pydantic import BaseModel, ConfigDict

from enums.question_type import QuestionType
from schemas.option import OptionResponse


class QuestionResponse(BaseModel):
    id: UUID
    type: QuestionType
    text: str
    options: list[OptionResponse]

    model_config = ConfigDict(from_attributes=True)
