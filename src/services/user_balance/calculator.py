from uuid import UUID

from db.repositories.user_answer import IUserAnswerRepository


class QuizBonusCalculator:
    def __init__(self, answer_repo: IUserAnswerRepository):
        self.answer_repo = answer_repo
        self.POINTS_PER_QUESTION = 100

    async def calculate_bonus(self, quiz_session_id: UUID, user_id: UUID) -> int:
        correct_answers_count = await self.answer_repo.count_unique_correct_answers(
            session_id=quiz_session_id,
            user_id=user_id,
        )
        return correct_answers_count * self.POINTS_PER_QUESTION
