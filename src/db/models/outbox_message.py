from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from db.models.mixins import UUIDMixin


class OutboxMessage(UUIDMixin, Base):
    __tablename__ = "outbox"

    event_type: Mapped[str]
    payload: Mapped[dict] = mapped_column(JSONB)
    is_processed: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
