from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserAnswer


class IUserAnswerRepository(ABC):
    @abstractmethod
    async def create(self, quiz_session_id: UUID, question_id: UUID, user_id: UUID, is_correct: bool): ...

    @abstractmethod
    async def count_unique_correct_answers(self, session_id: UUID, user_id: UUID): ...

    @abstractmethod
    async def answer_exists(self, session_id: UUID, user_id: UUID, question_id: UUID): ...


class UserAnswerRepository(IUserAnswerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, quiz_session_id: UUID, question_id: UUID, user_id: UUID, is_correct: bool):
        answer = UserAnswer(
            session_id=quiz_session_id,
            question_id=question_id,
            user_id=user_id,
            is_correct=is_correct,
        )
        self.session.add(answer)
        await self.session.commit()

    async def count_unique_correct_answers(
            self,
            session_id: UUID,
            user_id: UUID,
    ) -> int:
        subquery = (
            select(UserAnswer.question_id)
            .where(
                UserAnswer.user_id == user_id,
                UserAnswer.session_id != session_id,
                UserAnswer.is_correct,
            )
        )

        stmt = (
            select(func.count(UserAnswer.question_id))
            .where(
                UserAnswer.user_id == user_id,
                UserAnswer.session_id == session_id,
                UserAnswer.is_correct,
                UserAnswer.question_id.not_in(subquery),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def answer_exists(self, session_id: UUID, user_id: UUID, question_id: UUID):
        stmt = select(
            exists().where(
                UserAnswer.session_id == session_id,
                UserAnswer.user_id == user_id,
                UserAnswer.question_id == question_id,
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar()
