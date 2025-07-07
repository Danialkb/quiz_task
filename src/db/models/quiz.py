import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.mixins import UUIDMixin, TimestampMixin


class Quiz(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "quizzes"

    translations: Mapped[list["QuizTitleTranslation"]] = relationship(
        "QuizTitleTranslation",
        back_populates="quiz",
        cascade="all, delete-orphan",
    )
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )
    quiz_sessions: Mapped[list["QuizSession"]] = relationship(
        "QuizSession", back_populates="quiz"
    )


class QuizTitleTranslation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "quiz_title_translations"

    language: Mapped[str] = mapped_column(String(5), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)

    quiz_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quiz = relationship(Quiz, back_populates="translations")
