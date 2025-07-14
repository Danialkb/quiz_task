from typing import Optional, Callable, Awaitable

import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractChannel,
    AbstractExchange,
    AbstractQueue,
    AbstractIncomingMessage,
)

from messaging.config import RabbitConfig


class MessageBroker:
    def __init__(self, config: RabbitConfig):
        self.config = config
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.exchange: Optional[AbstractExchange] = None
        self.queue: Optional[AbstractQueue] = None

    async def connect(self, needs_dlq: bool = True):
        self.connection = await aio_pika.connect_robust(self.config.RABBITMQ_URL)
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            name=self.config.EXCHANGE_NAME,
            type=self.config.EXCHANGE_TYPE,
            durable=True,
            auto_delete=False,
        )

        queue_args = {}
        if needs_dlq:
            queue_args.update(
                {
                    "x-dead-letter-exchange": f"{self.config.EXCHANGE_NAME}.dlx",
                    "x-dead-letter-routing-key": f"{self.config.QUEUE_NAME}.dlq",
                }
            )

        self.queue = await self.channel.declare_queue(
            name=self.config.QUEUE_NAME,
            durable=True,
            arguments=queue_args,
        )

        if needs_dlq:
            await self._setup_dlq()

        await self.queue.bind(self.exchange, self.config.ROUTING_KEY)

    async def _setup_dlq(self):
        self.dlx_exchange = await self.channel.declare_exchange(
            name=f"{self.config.EXCHANGE_NAME}.dlx",
            type="direct",
            durable=True,
            auto_delete=False,
        )

    async def publish(
        self,
        message_body: bytes,
        routing_key: str | None = None,
    ):
        if not self.exchange:
            raise RuntimeError("Exchange not initialized. Call connect() first.")

        message = aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self.exchange.publish(
            message=message,
            routing_key=routing_key or self.config.ROUTING_KEY,
        )

    async def close(self):
        if not self.connection:
            return

        await self.connection.close()
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None
