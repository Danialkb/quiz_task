from enum import Enum


class OutboxEvent(str, Enum):
    BALANCE_UPDATE = "BALANCE_UPDATE"
