import logging
from uuid import UUID

from db.repositories.quiz import IQuizRepository
from db.repositories.quiz_session import IQuizSessionRepository
from schemas.quiz_session import QuizSessionCreateSchema, QuizSessionCreateResponse
from services.base import UseCase
from services.exceptions.not_found import NotFoundException

logger = logging.getLogger(__name__)


class CreateQuizSessionCommand(UseCase):
    def __init__(
        self, quiz_session_repo: IQuizSessionRepository, quiz_repo: IQuizRepository
    ):
        self.quiz_session_repo = quiz_session_repo
        self.quiz_repo = quiz_repo

    async def execute(
        self, quiz_session_data: QuizSessionCreateSchema, user_id: UUID
    ) -> QuizSessionCreateResponse:
        logger.info(f"User<{user_id}> entered {self.__class__.__name__}")

        data = quiz_session_data.model_dump()
        quiz_exists = await self.quiz_repo.get_by_id(quiz_session_data.quiz_id)
        if not quiz_exists:
            raise NotFoundException(detail="Quiz not found")

        data["user_id"] = user_id
        data["questions_count"] = await self.quiz_repo.get_question_count(
            quiz_session_data.quiz_id
        )
        quiz_session = await self.quiz_session_repo.create(data)

        logger.info(f"User<{user_id}> exiting {self.__class__.__name__}")
        return QuizSessionCreateResponse.model_validate(quiz_session)
