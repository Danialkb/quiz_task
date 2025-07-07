from uuid import UUID

from db.models import Option
from schemas.user_answer import UserAnswerCreateSchema
from services.user_answer.strategies.base import AnswerValidationStrategy


class MultiChoiceValidation(AnswerValidationStrategy):
    async def validate(
        self, user_answer: UserAnswerCreateSchema, options: list[Option]
    ) -> tuple[bool, list[UUID]]:
        selected = set(user_answer.options)
        correct_ids = {opt.id for opt in options if opt.is_correct}

        is_correct = selected == correct_ids and len(selected) == len(correct_ids)
        return is_correct, [opt.id for opt in options if opt.is_correct]
