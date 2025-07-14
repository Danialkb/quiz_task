from uuid import UUID

from pydantic import BaseModel

from enums.balance_update_type import BalanceUpdateType


class BalanceUpdateMessage(BaseModel):
    user_id: UUID
    amount: int
    type: BalanceUpdateType
