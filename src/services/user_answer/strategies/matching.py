from typing import Iterable
from uuid import UUID

from sqlalchemy.ext.asyncio import async_sessionmaker

from db.models import Option, MatchingOptionCorrectPair
from db.repositories.matching_option_pair import MatchingOptionPairRepository
from db.session import engine
from schemas.user_answer import UserAnswerCreateSchema
from services.exceptions.base import ServiceException
from services.user_answer.strategies.base import AnswerValidationStrategy


class MatchingValidation(AnswerValidationStrategy):
    def __init__(self):
        self._session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def validate(self, user_answer: UserAnswerCreateSchema, options: list[Option]) -> tuple[bool, list[UUID]]:
        user_choices = user_answer.options
        if len(user_choices) != 2:
            raise ServiceException("Matching question should contain exactly two options")

        left_choices = [opt.id for opt in options if opt.is_left]

        user_left_choice, user_right_choice = self._identify_left_right_choice(
            user_choices, left_choices,
        )
        correct_pairs = await self._fetch_correct_pair(user_answer.question_id)
        correct_pair = next(filter(lambda opt: opt.left_option_id == user_left_choice, correct_pairs))
        is_correct = (
                user_left_choice == correct_pair.left_option_id
                and user_right_choice == correct_pair.right_option_id
        )
        return is_correct, [correct_pair.left_option_id, correct_pair.right_option_id]

    async def _fetch_correct_pair(self, question_id: UUID) -> Iterable[MatchingOptionCorrectPair]:
        async with self._session_factory() as session:
            repo = MatchingOptionPairRepository(session)
            return await repo.get_correct_pairs(question_id)

    def _identify_left_right_choice(
            self,
            user_choices: list[UUID],
            left_choices: list[UUID],
    ) -> tuple[UUID, UUID]:
        if user_choices[0] in left_choices:
            return user_choices[0], user_choices[1]
        return user_choices[1], user_choices[0]

