from unittest.mock import patch, AsyncMock
from uuid import uuid4

import pytest

from schemas.user_answer import UserAnswerCreateSchema
from services.user_answer.strategies.matching import MatchingValidation


class TestMatchingValidation:
    @pytest.mark.asyncio
    async def test_correct_matching(self, left_option, right_option):
        strategy = MatchingValidation()

        with patch.object(
            strategy,
            "_fetch_correct_pair",
            new_callable=AsyncMock,
            return_value=[
                AsyncMock(
                    left_option_id=left_option.id, right_option_id=right_option.id
                )
            ],
        ):
            user_answer = UserAnswerCreateSchema(
                question_id=uuid4(),
                quiz_session_id=uuid4(),
                options=[left_option.id, right_option.id],
            )

            is_correct, correct_ids = await strategy.validate(
                user_answer, [left_option, right_option]
            )

        assert is_correct
        assert correct_ids == [left_option.id, right_option.id]

    @pytest.mark.asyncio
    async def test_wrong_matching(self, left_option, right_option):
        strategy = MatchingValidation()

        correct_right_id = uuid4()

        with patch.object(
            strategy,
            "_fetch_correct_pair",
            new_callable=AsyncMock,
            return_value=[
                AsyncMock(
                    left_option_id=left_option.id, right_option_id=correct_right_id
                )
            ],
        ):
            user_answer = UserAnswerCreateSchema(
                question_id=uuid4(),
                quiz_session_id=uuid4(),
                options=[left_option.id, right_option.id],
            )

            is_correct, correct_ids = await strategy.validate(
                user_answer, [left_option, right_option]
            )

        assert not is_correct
        assert correct_ids == [left_option.id, correct_right_id]

    @pytest.mark.asyncio
    async def test_invalid_options_count(self):
        strategy = MatchingValidation()
        user_answer = UserAnswerCreateSchema(
            question_id=uuid4(), quiz_session_id=uuid4(), options=[uuid4()]
        )
        with pytest.raises(Exception) as exc:
            await strategy.validate(user_answer, [])
        assert "exactly two options" in str(exc.value)
