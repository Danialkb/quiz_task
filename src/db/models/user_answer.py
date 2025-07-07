import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from db.models.mixins import UUIDMixin


class UserAnswer(UUIDMixin, Base):
    __tablename__ = "user_answers"

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id"),
        index=True,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quiz_sessions.id"),
        index=True,
    )
    is_correct: Mapped[bool]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
