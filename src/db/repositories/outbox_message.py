from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.outbox_message import OutboxMessage
from enums.outbox_event import OutboxEvent


class IOutboxMessageRepository(ABC):
    @abstractmethod
    async def get_unprocessed_messages(self) -> Iterable[OutboxMessage]:
        ...

    @abstractmethod
    async def create(self, event_type: OutboxEvent, payload: dict) -> OutboxMessage:
        ...

    @abstractmethod
    async def mark_message_processed(self, message_id: UUID) -> OutboxMessage:
        ...


class OutboxMessageRepository(IOutboxMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_unprocessed_messages(self) -> Iterable[OutboxMessage]:
        stmt = select(OutboxMessage).where(OutboxMessage.is_processed == False)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, event_type: OutboxEvent, payload: dict) -> OutboxMessage:
        message = OutboxMessage(
            event_type=event_type,
            payload=payload,
        )
        self.session.add(message)
        await self.session.commit()
        return message

    async def mark_message_processed(self, message_id: UUID) -> OutboxMessage | None:
        stmt = select(OutboxMessage).where(OutboxMessage.id == message_id)
        result = await self.session.execute(stmt)
        message = result.scalar_one_or_none()
        if not message:
            return
        message.is_processed = True
        await self.session.commit()
        return message
