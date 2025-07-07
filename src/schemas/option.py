from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OptionResponse(BaseModel):
    id: UUID
    text: str
    is_left: Optional[bool]
    is_right: Optional[bool]

    model_config = ConfigDict(from_attributes=True)
