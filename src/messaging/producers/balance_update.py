import json
import logging
from messaging.broker import MessageBroker
from messaging.producers.base import Producer
from messaging.producers.exceptions import ProducerException
from messaging.producers.messages import BalanceUpdateMessage


logger = logging.getLogger(__name__)


class BalanceUpdateProducer(Producer):
    def __init__(self, broker: MessageBroker):
        self.broker = broker

    async def publish(self, message: BalanceUpdateMessage) -> None:
        try:
            await self.broker.connect()
            await self.broker.publish(
                message_body=json.dumps(message.model_dump(mode="json")).encode(),
            )
            logger.info(f"Published balance update for user {message.user_id}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise ProducerException(f"Publishing failed: {str(e)}") from e
        finally:
            logger.info("Closing broker connection...")
            await self.broker.close()
