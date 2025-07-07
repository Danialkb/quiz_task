import logging
from uuid import UUID

from db.repositories.quiz_session import IQuizSessionRepository
from schemas.quiz_session import QuizSessionResponse
from services.base import UseCase


logger = logging.getLogger(__name__)


class ListQuizSessionsQuery(UseCase):
    def __init__(self, quiz_session_repo: IQuizSessionRepository):
        self.quiz_session_repo = quiz_session_repo

    async def execute(self, user_id: UUID, language: str) -> list[QuizSessionResponse]:
        logger.info(f"User<{user_id}> entered {self.__class__.__name__}")

        quiz_sessions = await self.quiz_session_repo.get_all(user_id, language)
        for session in quiz_sessions:
            session.quiz.title = session.quiz.translations[0].title

        logger.info(f"User<{user_id}> exiting {self.__class__.__name__}")
        return [
            QuizSessionResponse.model_validate(quiz_session)
            for quiz_session in quiz_sessions
        ]
