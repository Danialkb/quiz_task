import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.mixins import UUIDMixin


class QuizSession(UUIDMixin, Base):
    __tablename__ = "quiz_sessions"

    correct_answers: Mapped[int] = mapped_column(default=0)
    questions_count: Mapped[int]
    bonus_points: Mapped[int] = mapped_column(default=0)
    percentile: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    finished_at: Mapped[datetime] = mapped_column(nullable=True, index=True)

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="quiz_sessions")
