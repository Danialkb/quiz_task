import logging
from uuid import UUID

from db.repositories.question import IQuestionRepository
from db.repositories.user_answer import IUserAnswerRepository
from enums.question_type import QuestionType
from schemas.user_answer import UserAnswerCreateSchema, UserAnswerCreateResponse
from services.base import UseCase
from services.exceptions.base import ServiceException
from services.quiz_session.update import QuizSessionProgressUpdater
from services.user_answer.correct_answer.create import UserAnswerLogger
from services.user_answer.strategies.factory import IAnswerValidationFactory


logger = logging.getLogger(__name__)


class SubmitAnswerCommand(UseCase):
    def __init__(
        self,
        question_repo: IQuestionRepository,
        answer_validation_factory: type[IAnswerValidationFactory],
        quiz_session_updater: QuizSessionProgressUpdater,
        answer_repo: IUserAnswerRepository,
    ):
        self.question_repo = question_repo
        self.answer_validation_factory = answer_validation_factory
        self.quiz_session_updater = quiz_session_updater
        self.answer_repo = answer_repo
        self._answer_logger = UserAnswerLogger(answer_repo)

    async def execute(
        self, data: UserAnswerCreateSchema, user_id: UUID
    ) -> UserAnswerCreateResponse:
        logger.info(f"User<{user_id}> entered {self.__class__.__name__}")
        answer_exists = await self.answer_repo.answer_exists(
            session_id=data.quiz_session_id,
            user_id=user_id,
            question_id=data.question_id,
        )

        question = await self.question_repo.get_by_id(
            data.question_id, include_options=True
        )
        if answer_exists and question.type != QuestionType.MATCHING:
            raise ServiceException("User already answered")

        try:
            strategy = self.answer_validation_factory.get_strategy(question.type)
        except KeyError:
            raise ServiceException(detail="Unknown question type")

        is_correct, correct_options = await strategy.validate(data, question.options)
        if is_correct:
            await self.quiz_session_updater.update_progress(data.quiz_session_id)
        await self._answer_logger.log_answer(
            quiz_session_id=data.quiz_session_id,
            question_id=question.id,
            user_id=user_id,
            is_correct=is_correct,
        )

        logger.info(f"User<{user_id}> exiting {self.__class__.__name__}")
        return UserAnswerCreateResponse(
            question_id=question.id,
            quiz_session_id=data.quiz_session_id,
            is_correct=is_correct,
            selected_options=data.options,
            correct_options=correct_options,
        )
