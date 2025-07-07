from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from db.models import Question
from db.models.quiz import Quiz, QuizTitleTranslation


class IQuizRepository(ABC):
    @abstractmethod
    async def get_all(self, language: str) -> Iterable[Quiz]: ...

    @abstractmethod
    async def get_by_id(self, instance_id: UUID, **kwargs) -> Quiz | None: ...

    @abstractmethod
    async def get_question_count(self, quiz_id: UUID) -> int: ...


class QuizRepository(IQuizRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, language: str) -> Iterable[Quiz]:
        stmt = (
            select(Quiz)
            .join(Quiz.translations)
            .filter(QuizTitleTranslation.language == language)
            .options(contains_eager(Quiz.translations))
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_by_id(self, instance_id: UUID, **kwargs) -> Quiz | None:
        stmt = select(Quiz).filter(Quiz.id == instance_id)
        language = kwargs.get("language")
        if language:
            stmt = (
                stmt
                .join(Quiz.translations)
                .filter(QuizTitleTranslation.language == language)
                .options(contains_eager(Quiz.translations))
            )

        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    async def get_question_count(self, quiz_id: UUID) -> int:
        stmt = (
            select(func.count(Question.id))
            .where(Question.quiz_id == quiz_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
