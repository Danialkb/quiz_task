from abc import abstractmethod, ABC
from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload, with_loader_criteria

from db.models import Question, QuestionTranslation, Option, OptionTranslation


class IQuestionRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, instance_id: UUID, include_options: bool = False
    ) -> Question | None:
        ...

    @abstractmethod
    async def get_by_quiz_id(self, quiz_id: UUID, language: str) -> Iterable[Question]:
        ...


class QuestionRepository(IQuestionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self, instance_id: UUID, include_options: bool = False
    ) -> Question | None:
        stmt = select(Question).filter(Question.id == instance_id)

        if include_options:
            stmt = stmt.options(selectinload(Question.options))

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_quiz_id(self, quiz_id: UUID, language: str) -> Iterable[Question]:
        stmt = (
            select(Question)
            .join(Question.translations)
            .filter(Question.quiz_id == quiz_id)
            .filter(QuestionTranslation.language == language)
            .options(
                contains_eager(Question.translations),
                selectinload(Question.options).selectinload(Option.translations),
                with_loader_criteria(
                    OptionTranslation, OptionTranslation.language == language
                ),
            )
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()
