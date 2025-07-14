import logging
from uuid import UUID

from db.repositories.outbox_message import IOutboxMessageRepository
from enums.balance_update_type import BalanceUpdateType
from enums.outbox_event import OutboxEvent
from messaging.producers.base import Producer
from messaging.producers.exceptions import ProducerException
from messaging.producers.messages import BalanceUpdateMessage
from services.user_balance.calculator import QuizBonusCalculator


logger = logging.getLogger(__name__)


class BonusAdder:
    def __init__(
        self,
        bonus_calculator: QuizBonusCalculator,
        balance_update_producer: Producer,
        outbox_repo: IOutboxMessageRepository,
    ):
        self.bonus_calculator = bonus_calculator
        self.balance_update_producer = balance_update_producer
        self.outbox_repo = outbox_repo

    async def add_bonus_points(self, quiz_session_id: UUID, user_id: UUID) -> int:
        bonus_amount = await self.bonus_calculator.calculate_bonus(
            quiz_session_id, user_id
        )
        if bonus_amount == 0:
            return 0

        message = BalanceUpdateMessage(
            user_id=user_id,
            amount=bonus_amount,
            type=BalanceUpdateType.QUIZ_REWARD,
        )
        try:
            await self.balance_update_producer.publish(message)
        except ProducerException as e:
            logger.error("Error during sending bonus points", str(e), exc_info=True)
            await self.outbox_repo.create(
                event_type=OutboxEvent.BALANCE_UPDATE,
                payload=message.model_dump(mode="json"),
            )

        return bonus_amount
