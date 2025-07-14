import logging

from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends
from background_tasks.taskiq import broker
from db.repositories.outbox_message import OutboxMessageRepository
from db.session import get_session
from messaging.broker import MessageBroker
from messaging.config import RabbitConfig
from messaging.producers.balance_update import BalanceUpdateProducer
from resources.config import settings
from services.outbox_message.retry import BalanceMessageRetrySender

logger = logging.getLogger(__name__)


@broker.task(schedule=[{"cron": "*/2 * * * *"}])
async def retry_outbox_messages(
    session: AsyncSession = TaskiqDepends(get_session),
) -> None:
    outbox_repo = OutboxMessageRepository(session)

    broker_config = RabbitConfig(
        RABBITMQ_URL=settings.RABBITMQ_URL,
        EXCHANGE_NAME=settings.BALANCE_EXCHANGE,
        EXCHANGE_TYPE=settings.BALANCE_EXCHANGE_TYPE,
        QUEUE_NAME=settings.BALANCE_QUEUE,
        ROUTING_KEY=settings.BALANCE_ROUTING_KEY,
    )
    message_broker = MessageBroker(broker_config)
    balance_update_producer = BalanceUpdateProducer(message_broker)

    message_retry_sender = BalanceMessageRetrySender(
        balance_update_producer=balance_update_producer,
        outbox_repo=outbox_repo,
    )
    await message_retry_sender.send()
