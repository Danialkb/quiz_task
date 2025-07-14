import logging

from sqlalchemy import select
from taskiq import TaskiqDepends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from datetime import datetime, timedelta

from background_tasks import broker
from cache.dependencies import get_redis
from db.models import QuizSession
from db.session import get_session
from services.quiz.statistics import QuizStatsService


logger = logging.getLogger(__name__)


@broker.task(schedule=[{"cron": "*/2 * * * *"}])
async def update_quiz_stats(
    session: AsyncSession = TaskiqDepends(get_session),
    redis: Redis = TaskiqDepends(get_redis),
):
    stats_service = QuizStatsService(redis)

    result = await session.execute(
        select(QuizSession.quiz_id)
        .where(QuizSession.finished_at >= datetime.now() - timedelta(days=7))
        .distinct()
    )
    quiz_ids = result.scalars().all()

    for quiz_id in quiz_ids:
        result = await session.execute(
            select(QuizSession).where(
                QuizSession.quiz_id == quiz_id,
                QuizSession.finished_at.is_not(None),
            )
        )
        quiz_sessions = result.scalars().all()

        await stats_service.set_stats(quiz_id, quiz_sessions)
        logger.info(f"Updated stats for Quiz<{quiz_id}>")
