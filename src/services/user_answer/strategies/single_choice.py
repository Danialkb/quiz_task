from uuid import UUID

from db.models import Option
from schemas.user_answer import UserAnswerCreateSchema
from services.exceptions.base import ServiceException
from services.user_answer.strategies.base import AnswerValidationStrategy


class SingleChoiceValidation(AnswerValidationStrategy):
    async def validate(self, user_answer: UserAnswerCreateSchema, options: list[Option]) -> tuple[bool, list[UUID]]:
        if len(user_answer.options) != 1:
            raise ServiceException("Single choice question should contain exactly one option")

        selected = user_answer.options[0]
        is_correct = any(
            option.id == selected and option.is_correct
            for option in options
        )
        return is_correct, [opt.id for opt in options if opt.is_correct]
