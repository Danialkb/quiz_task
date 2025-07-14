import logging
from datetime import datetime
from uuid import UUID

from db.repositories.quiz_session import IQuizSessionRepository
from schemas.quiz_session import QuizSessionFinishedResponse
from services.base import UseCase
from services.exceptions.not_found import NotFoundException
from services.quiz.statistics import QuizStatsService
from services.user_balance.bonus_adder import BonusAdder

logger = logging.getLogger(__name__)


class FinishQuizSessionCommand(UseCase):
    def __init__(
        self,
        quiz_session_repo: IQuizSessionRepository,
        bonus_adder: BonusAdder,
        quiz_stats_service: QuizStatsService,
    ):
        self.quiz_session_repo = quiz_session_repo
        self.bonus_adder = bonus_adder
        self.quiz_stats_service = quiz_stats_service

    async def execute(
        self, quiz_session_id: UUID, user_id: UUID
    ) -> QuizSessionFinishedResponse:
        logger.info(f"User<{user_id}> entered {self.__class__.__name__}")
        now = datetime.now()

        quiz_session = await self.quiz_session_repo.get_by_id(quiz_session_id)
        if not quiz_session:
            raise NotFoundException("Quiz session not found")
        # if quiz_session.finished_at is not None:
        #     raise ServiceException("Quiz already finished")

        bonus_points = await self.bonus_adder.add_bonus_points(
            quiz_session_id,
            user_id,
        )
        percentile = await self.quiz_stats_service.get_user_percentile(
            quiz_id=quiz_session.quiz_id,
            user_score=(quiz_session.correct_answers / quiz_session.questions_count)
            * 100,
        )
        quiz_session = await self.quiz_session_repo.update_progress(
            quiz_session_id,
            answered_correctly=False,
            finished_at=now,
            bonus_points=bonus_points,
            percentile=percentile,
        )

        logger.info(f"User<{user_id}> exiting {self.__class__.__name__}")

        return QuizSessionFinishedResponse.model_validate(quiz_session)
