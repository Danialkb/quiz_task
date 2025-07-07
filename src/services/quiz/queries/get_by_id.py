import logging
from uuid import UUID

from db.repositories.quiz import IQuizRepository
from schemas.quiz import QuizResponse
from services.base import UseCase
from services.exceptions.not_found import NotFoundException


logger = logging.getLogger(__name__)


class GetQuizQuery(UseCase):
    def __init__(self, quiz_repo: IQuizRepository):
        self.quiz_repo = quiz_repo

    async def execute(
        self, instance_id: UUID, language: str, user_id: UUID
    ) -> QuizResponse | None:
        logger.info(f"User<{user_id}> entered {self.__class__.__name__}")
        quiz = await self.quiz_repo.get_by_id(instance_id, language=language)
        logger.info(f"User<{user_id}> exiting {self.__class__.__name__}")
        if quiz is None:
            raise NotFoundException("Quiz not found")
        return QuizResponse(id=quiz.id, title=quiz.translations[0].title)
