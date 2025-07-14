from abc import ABC, abstractmethod
from uuid import UUID

from db.models import Option
from schemas.user_answer import UserAnswerCreateSchema


class AnswerValidationStrategy(ABC):
    @abstractmethod
    async def validate(
        self, user_answer: UserAnswerCreateSchema, options: list[Option]
    ) -> tuple[bool, list[UUID]]:
        ...
