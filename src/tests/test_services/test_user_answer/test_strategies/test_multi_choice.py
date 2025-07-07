from uuid import uuid4

import pytest

from schemas.user_answer import UserAnswerCreateSchema
from services.user_answer.strategies.multi_choice import MultiChoiceValidation


class TestMultiChoiceValidation:
    @pytest.mark.asyncio
    async def test_correct_answer(self, correct_option, wrong_option):
        strategy = MultiChoiceValidation()
        user_answer = UserAnswerCreateSchema(
            question_id=uuid4(), quiz_session_id=uuid4(), options=[correct_option.id]
        )
        is_correct, correct_ids = await strategy.validate(
            user_answer, [correct_option, wrong_option]
        )
        assert is_correct
        assert correct_ids == [correct_option.id]

    @pytest.mark.asyncio
    async def test_partial_answer(self, correct_option, wrong_option):
        strategy = MultiChoiceValidation()
        user_answer = UserAnswerCreateSchema(
            question_id=uuid4(),
            quiz_session_id=uuid4(),
            options=[correct_option.id, wrong_option.id],
        )
        is_correct, correct_ids = await strategy.validate(
            user_answer, [correct_option, wrong_option]
        )
        assert not is_correct
        assert correct_ids == [correct_option.id]
