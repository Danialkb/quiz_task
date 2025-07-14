from dataclasses import dataclass


@dataclass
class RabbitConfig:
    RABBITMQ_URL: str
    EXCHANGE_NAME: str
    EXCHANGE_TYPE: str
    QUEUE_NAME: str
    ROUTING_KEY: str
