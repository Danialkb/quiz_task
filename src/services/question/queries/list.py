import logging
from uuid import UUID

from db.repositories.question import IQuestionRepository
from schemas.question import QuestionResponse
from services.base import UseCase


logger = logging.getLogger(__name__)


class ListQuestionsByQuizQuery(UseCase):
    def __init__(self, question_repo: IQuestionRepository):
        self.question_repo = question_repo

    async def execute(self, quiz_id: UUID, language: str, user_id: UUID) -> list[QuestionResponse]:
        logger.info(f"User<{user_id}> entered {self.__class__.__name__}")
        questions = await self.question_repo.get_by_quiz_id(quiz_id, language)
        for question in questions:
            question.text = question.translations[0].text
            for option in question.options:
                option.text = option.translations[0].text
        logger.info(f"User<{user_id}> exiting {self.__class__.__name__}")
        return [QuestionResponse.model_validate(question) for question in questions]
