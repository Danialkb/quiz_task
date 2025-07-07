from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import OptionTranslation, Option, QuestionTranslation, Question, QuizSession
from db.models.quiz import Quiz, QuizTitleTranslation
from enums.question_type import QuestionType


@pytest.fixture
async def test_quiz(db_session: AsyncSession):
    quiz = Quiz()
    db_session.add(quiz)
    await db_session.flush()

    translations = [
        QuizTitleTranslation(
            quiz_id=quiz.id,
            language="en",
            title="English Title"
        ),
        QuizTitleTranslation(
            quiz_id=quiz.id,
            language="es",
            title="Nombre español"
        )
    ]
    db_session.add_all(translations)
    await db_session.commit()
    return quiz


@pytest.fixture
async def test_question(db_session: AsyncSession, test_quiz):
    question = Question(
        quiz_id=test_quiz.id,
        type=QuestionType.SINGLE_CHOICE
    )
    db_session.add(question)
    await db_session.flush()

    translation = QuestionTranslation(
        question_id=question.id,
        language="en",
        text="Test Question"
    )
    db_session.add(translation)
    await db_session.commit()
    return question


@pytest.fixture
async def test_question_with_options(db_session: AsyncSession, test_quiz):
    question = Question(
        quiz_id=test_quiz.id,
        type=QuestionType.MULTI_CHOICE
    )
    db_session.add(question)
    await db_session.flush()

    db_session.add(QuestionTranslation(
        question_id=question.id,
        language="en",
        text="Select correct options"
    ))

    option1 = Option(question_id=question.id, is_correct=True)
    option2 = Option(question_id=question.id, is_correct=False)
    db_session.add_all([option1, option2])
    await db_session.flush()

    db_session.add_all([
        OptionTranslation(
            option_id=option1.id,
            language="en",
            text="Correct option"
        ),
        OptionTranslation(
            option_id=option2.id,
            language="en",
            text="Wrong option"
        )
    ])

    await db_session.commit()
    return question


@pytest.fixture
async def test_question_with_multilang(db_session: AsyncSession, test_quiz):
    question = Question(
        quiz_id=test_quiz.id,
        type=QuestionType.SINGLE_CHOICE
    )
    db_session.add(question)
    await db_session.flush()

    db_session.add_all([
        QuestionTranslation(
            question_id=question.id,
            language="en",
            text="English question"
        ),
        QuestionTranslation(
            question_id=question.id,
            language="es",
            text="Pregunta en español"
        )
    ])

    option = Option(question_id=question.id, is_correct=True)
    db_session.add(option)
    await db_session.flush()

    db_session.add_all([
        OptionTranslation(
            option_id=option.id,
            language="en",
            text="English option"
        ),
        OptionTranslation(
            option_id=option.id,
            language="es",
            text="Opción en español"
        )
    ])

    await db_session.commit()
    return question


@pytest.fixture
def test_user_id() -> str:
    return str(uuid4())


@pytest.fixture
async def test_quiz_session(db_session: AsyncSession, test_quiz, test_user_id):
    session = QuizSession(
        quiz_id=test_quiz.id,
        user_id=test_user_id,
        correct_answers=2,
        questions_count=5,
        created_at=datetime.now(),
    )
    db_session.add(session)
    await db_session.commit()
    return session
