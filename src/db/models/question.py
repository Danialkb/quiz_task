import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.mixins import UUIDMixin, TimestampMixin
from db.models.option import Option
from db.models.quiz import Quiz
from enums.question_type import QuestionType


class Question(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "questions"

    type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)

    quiz_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quiz: Mapped[Quiz] = relationship(back_populates="questions")
    options: Mapped[list[Option]] = relationship(back_populates="question", cascade="all, delete-orphan")
    translations: Mapped[list["QuestionTranslation"]] = relationship(
        "QuestionTranslation",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class QuestionTranslation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "question_translations"

    language: Mapped[str] = mapped_column(String(5), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)

    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question: Mapped[Question] = relationship(back_populates="translations")
