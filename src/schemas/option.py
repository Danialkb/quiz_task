from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OptionResponse(BaseModel):
    id: UUID
    text: str

    model_config = ConfigDict(from_attributes=True)
