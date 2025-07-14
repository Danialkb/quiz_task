import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.mixins import UUIDMixin, TimestampMixin


class Option(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "options"

    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question: Mapped["Question"] = relationship(back_populates="options")
    translations: Mapped[list["OptionTranslation"]] = relationship(
        "OptionTranslation",
        back_populates="option",
        cascade="all, delete-orphan",
    )


class OptionTranslation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "option_translations"

    language: Mapped[str] = mapped_column(String(5), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)

    option_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("options.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    option: Mapped[Option] = relationship(back_populates="translations")
