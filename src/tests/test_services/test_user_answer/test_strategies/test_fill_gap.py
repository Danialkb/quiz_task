from uuid import uuid4

import pytest

from schemas.user_answer import UserAnswerCreateSchema
from services.exceptions.base import ServiceException
from services.user_answer.strategies.fill_gap import FillGapValidation


class TestFillGapValidation:
    async def test_correct_answer(self, correct_option):
        strategy = FillGapValidation()
        user_answer = UserAnswerCreateSchema(
            question_id=uuid4(), quiz_session_id=uuid4(), options=[correct_option.id]
        )
        is_correct, correct_ids = await strategy.validate(user_answer, [correct_option])
        assert is_correct
        assert correct_ids == [correct_option.id]

    async def test_wrong_answer(self, correct_option, wrong_option):
        strategy = FillGapValidation()
        user_answer = UserAnswerCreateSchema(
            question_id=uuid4(), quiz_session_id=uuid4(), options=[wrong_option.id]
        )
        is_correct, correct_ids = await strategy.validate(user_answer, [correct_option])
        assert not is_correct
        assert correct_ids == [correct_option.id]

    async def test_invalid_options_count(self):
        strategy = FillGapValidation()
        user_answer = UserAnswerCreateSchema(
            question_id=uuid4(), quiz_session_id=uuid4(), options=[uuid4(), uuid4()]
        )
        with pytest.raises(ServiceException) as exc:
            await strategy.validate(user_answer, [])
        assert "exactly one option" in str(exc.value)
