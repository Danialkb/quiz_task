from abc import ABC, abstractmethod


class Producer(ABC):
    @abstractmethod
    async def publish(self, *args, **kwargs):
        ...
