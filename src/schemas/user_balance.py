from pydantic import BaseModel


class UserBalanceAddSchema(BaseModel):
    amount: int
