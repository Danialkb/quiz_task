import logging.config

from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from taskiq_redis import ListQueueBroker

from resources.config import settings
from resources.logs.config import logging_config

logging.config.dictConfig(logging_config)

REDIS_URL = (
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.TASKIQ_REDIS_TABLE}"
)

broker = ListQueueBroker(
    url=REDIS_URL,
)

scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])
