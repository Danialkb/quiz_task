from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import MatchingOptionCorrectPair


class IMatchingOptionPairRepository(ABC):
    @abstractmethod
    async def get_correct_pairs(
        self, question_id: UUID
    ) -> Iterable[MatchingOptionCorrectPair]: ...


class MatchingOptionPairRepository(IMatchingOptionPairRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_correct_pairs(
        self, question_id: UUID
    ) -> Iterable[MatchingOptionCorrectPair]:
        stmt = select(MatchingOptionCorrectPair).where(
            MatchingOptionCorrectPair.question_id == question_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
