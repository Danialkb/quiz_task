from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select, func, exists, union_all, or_, and_, cast, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserAnswer, Question
from enums.question_type import QuestionType


class IUserAnswerRepository(ABC):
    @abstractmethod
    async def create(
            self, quiz_session_id: UUID, question_id: UUID, user_id: UUID, is_correct: bool
    ): ...

    @abstractmethod
    async def count_unique_correct_answers(self, session_id: UUID, user_id: UUID): ...

    @abstractmethod
    async def answer_exists(
            self, session_id: UUID, user_id: UUID, question_id: UUID
    ): ...


class UserAnswerRepository(IUserAnswerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self, quiz_session_id: UUID, question_id: UUID, user_id: UUID, is_correct: bool
    ):
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
        matching_questions = select(Question.id).where(Question.type == QuestionType.MATCHING)
        #   для каждой сессии и вопроса в других сессиях вычисляем:
        #   all_correct: bool_and(is_correct) -> True, если все ответы правильные
        #   any_correct: bool_or(is_correct) -> True, если есть хотя бы один правильный
        session_question_agg = select(
            UserAnswer.session_id,
            UserAnswer.question_id,
            func.bool_and(UserAnswer.is_correct).label("all_correct"),
            func.bool_or(UserAnswer.is_correct).label("any_correct"),
        ).where(
            UserAnswer.user_id == user_id,
            UserAnswer.session_id != session_id,
        ).group_by(
            UserAnswer.session_id,
            UserAnswer.question_id,
        ).alias("session_question_agg")

        # Matching вопросы, полностью правильно отвеченные в других сессиях
        fully_correct_matching = select(
            session_question_agg.c.question_id,
        ).where(
            session_question_agg.c.question_id.in_(matching_questions),
            session_question_agg.c.all_correct == True,
        ).distinct()

        # обычные вопросы с хотя бы одним правильным ответом в других сессиях
        any_correct_regular = select(
            session_question_agg.c.question_id,
        ).where(
            session_question_agg.c.question_id.not_in(matching_questions),
            session_question_agg.c.any_correct == True,
        ).distinct()

        previously_correct = union_all(fully_correct_matching, any_correct_regular).alias("previously_correct")

        current_question_agg = select(
            UserAnswer.question_id,
            func.bool_and(UserAnswer.is_correct).label("all_correct"),
            func.bool_or(UserAnswer.is_correct).label("any_correct"),
        ).where(
            UserAnswer.user_id == user_id,
            UserAnswer.session_id == session_id,
        ).group_by(
            UserAnswer.question_id,
        ).alias("current_question_agg")

        # в текущей сессии правильно отвеченные вопросы
        correct_in_current = select(
            current_question_agg.c.question_id
        ).where(
            or_(
                and_(
                    current_question_agg.c.question_id.in_(matching_questions),
                    current_question_agg.c.all_correct == True,
                ),
                and_(
                    current_question_agg.c.question_id.not_in(matching_questions),
                    current_question_agg.c.any_correct == True,
                )
            )
        ).distinct()

        stmt = select(
            func.count(correct_in_current.c.question_id),
        ).select_from(
            correct_in_current,
        ).where(
            correct_in_current.c.question_id.not_in(select(previously_correct.c.question_id)),
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
