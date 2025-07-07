from uuid import UUID

from db.models import QuizSession
from db.repositories.quiz_session import IQuizSessionRepository
from services.exceptions.not_found import NotFoundException


class QuizSessionProgressUpdater:
    def __init__(self, quiz_session_repo: IQuizSessionRepository):
        self.quiz_session_repo = quiz_session_repo

    async def update_progress(self, quiz_session_id: UUID) -> QuizSession:
        quiz_session = await self.quiz_session_repo.update_progress(quiz_session_id)
        if not quiz_session:
            raise NotFoundException("Quiz session not found")

        return quiz_session
