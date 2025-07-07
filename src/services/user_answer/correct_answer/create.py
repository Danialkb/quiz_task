from uuid import UUID

from db.repositories.user_answer import IUserAnswerRepository


class UserAnswerLogger:
    def __init__(self, answer_repo: IUserAnswerRepository):
        self.answer_repo = answer_repo

    async def log_answer(
        self, quiz_session_id: UUID, question_id: UUID, user_id: UUID, is_correct: bool
    ):
        await self.answer_repo.create(
            quiz_session_id=quiz_session_id,
            question_id=question_id,
            user_id=user_id,
            is_correct=is_correct,
        )
