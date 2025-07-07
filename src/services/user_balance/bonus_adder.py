from uuid import UUID

from services.user_balance.calculator import QuizBonusCalculator
from services.user_balance.external_api import IUserBalanceExternalAPI


class BonusAdder:
    def __init__(
            self,
            bonus_calculator: QuizBonusCalculator,
            balance_external_api: IUserBalanceExternalAPI,
    ):
        self.bonus_calculator = bonus_calculator
        self.balance_external_api = balance_external_api

    async def add_bonus_points(self, quiz_session_id: UUID, user_id: UUID) -> int:
        bonus_amount = await self.bonus_calculator.calculate_bonus(quiz_session_id, user_id)
        if bonus_amount == 0:
            return 0

        async with self.balance_external_api as balance_api:
            await balance_api.update_user_balance(user_id, bonus_amount)

        return bonus_amount
