import logging
from abc import ABC, abstractmethod
from uuid import UUID

import httpx

from resources.config import settings
from schemas.user_balance import UserBalanceAddSchema


logger = logging.getLogger(__name__)


class IUserBalanceExternalAPI(ABC):
    @abstractmethod
    async def update_user_balance(self, user_id: UUID, amount: int): ...


class UserBalanceExternalAPI(IUserBalanceExternalAPI):
    def __init__(self):
        self.base_url = settings.BALANCE_SERVICE_URL
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    # TODO: Configure retry policy
    async def update_user_balance(self, user_id: UUID, amount: int):
        url = f"{self.base_url}/user_balance/add"
        headers = {
            "Content-Type": "application/json",
            "X-User-ID": str(user_id),
        }
        payload = UserBalanceAddSchema(amount=amount).model_dump()

        logger.info(f"Sending {payload} to external Balance service")
        response = await self.client.post(
            url,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
