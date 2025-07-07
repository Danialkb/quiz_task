from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from db.models import QuizSession, Quiz, QuizTitleTranslation


class IQuizSessionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, instance_id: UUID) -> QuizSession | None: ...

    @abstractmethod
    async def get_all(self, user_id: UUID, language: str) -> Iterable[QuizSession]: ...

    @abstractmethod
    async def create(self, data: dict) -> QuizSession: ...

    @abstractmethod
    async def update_progress(
            self,
            session_id: UUID,
            answered_correctly: bool = True,
            finished_at: datetime | None = None,
    ) -> QuizSession | None: ...


class QuizSessionRepository(IQuizSessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, instance_id: UUID) -> QuizSession | None:
        stmt = select(QuizSession).filter(QuizSession.id == instance_id)
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    async def get_all(self, user_id: UUID, language: str) -> Iterable[QuizSession]:
        stmt = (
            select(QuizSession)
            .join(QuizSession.quiz)
            .join(Quiz.translations)
            .where(QuizSession.user_id == user_id)
            .where(QuizTitleTranslation.language == language)
            .options(
                contains_eager(QuizSession.quiz)
                .contains_eager(Quiz.translations)
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def create(self, data: dict) -> QuizSession:
        quiz_session = QuizSession(**data)
        self.session.add(quiz_session)
        await self.session.commit()
        await self.session.refresh(quiz_session)
        return quiz_session

    async def update_progress(
        self,
        session_id: UUID,
        answered_correctly: bool = True,
        finished_at: datetime | None = None,
    ) -> QuizSession | None:
        stmt = select(QuizSession).filter(QuizSession.id == session_id)
        result = await self.session.execute(stmt)
        quiz_session = result.scalar_one_or_none()

        if quiz_session is None:
            return None

        if answered_correctly:
            quiz_session.correct_answers += 1

        if finished_at:
            quiz_session.finished_at = finished_at

        await self.session.commit()
        await self.session.refresh(quiz_session)
        return quiz_session
