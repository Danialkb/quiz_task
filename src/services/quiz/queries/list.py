import logging
from uuid import UUID

from db.repositories.quiz import IQuizRepository
from schemas.quiz import QuizResponse
from services.base import UseCase


logger = logging.getLogger(__name__)


class ListQuizzesQuery(UseCase):
    def __init__(self, quiz_repo: IQuizRepository):
        self.quiz_repo = quiz_repo

    async def execute(self, user_id: UUID, language: str) -> list[QuizResponse]:
        logger.info(f"User<{user_id}> entered {self.__class__.__name__}")
        quiz_list = await self.quiz_repo.get_all(language)
        logger.info(f"User<{user_id}> exiting {self.__class__.__name__}")
        return [
            QuizResponse(id=q.id, title=q.translations[0].title)
            for q in quiz_list
        ]
