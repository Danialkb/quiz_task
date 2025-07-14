import logging

from db.repositories.outbox_message import IOutboxMessageRepository
from enums.outbox_event import OutboxEvent
from messaging.producers.base import Producer
from messaging.producers.messages import BalanceUpdateMessage

logger = logging.getLogger(__name__)


class BalanceMessageRetrySender:
    def __init__(
        self, balance_update_producer: Producer, outbox_repo: IOutboxMessageRepository
    ):
        self.balance_update_producer = balance_update_producer
        self.outbox_repo = outbox_repo

    async def send(self):
        messages = await self.outbox_repo.get_unprocessed_messages()
        for message in messages:
            if message.event_type != OutboxEvent.BALANCE_UPDATE:
                continue
            validated_message = BalanceUpdateMessage.model_validate(message.payload)
            try:
                await self.balance_update_producer.publish(validated_message)
                message = await self.outbox_repo.mark_message_processed(message.id)
                logger.info(f"Message<{message.id}> has been processed successfully")
            except Exception as e:
                logger.error(f"Error during handling outbox messages: {e}", exc_info=e)
