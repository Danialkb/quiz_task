import asyncio

from sqlalchemy import select, delete

from db.models import UserAnswer
from db.models.quiz import Quiz, QuizTitleTranslation
from db.models.question import Question, QuestionTranslation
from db.models.option import Option, OptionTranslation
from db.session import async_session
from enums.question_type import QuestionType


def make_translations(model_cls, data: dict[str, str]):
    return [model_cls(language=lang, text=text) for lang, text in data.items()]


async def delete_matching_questions_and_answers():
    async with async_session() as session:
        matching_questions_stmt = select(Question.id).where(Question.type == "MATCHING")
        result = await session.execute(matching_questions_stmt)
        matching_question_ids = [row[0] for row in result.fetchall()]

        if not matching_question_ids:
            print("No matching questions found.")
            return

        print(f"Found {len(matching_question_ids)} matching questions.")

        delete_answers_stmt = delete(UserAnswer).where(
            UserAnswer.question_id.in_(matching_question_ids)
        )
        await session.execute(delete_answers_stmt)

        delete_questions_stmt = delete(Question).where(
            Question.id.in_(matching_question_ids)
        )
        await session.execute(delete_questions_stmt)

        await session.commit()
        print(
            f"Deleted {len(matching_question_ids)} matching questions and their answers."
        )


async def seed_quiz():
    await delete_matching_questions_and_answers()
    async with async_session() as session:
        stmt = select(QuizTitleTranslation).filter(
            QuizTitleTranslation.title == "General Knowledge Quiz"
        )
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            print("Db already populated. Exiting...")
            return

        quiz = Quiz(
            translations=[
                QuizTitleTranslation(language="en", title="General Knowledge Quiz"),
                QuizTitleTranslation(
                    language="es", title="Cuestionario de Conocimientos Generales"
                ),
            ]
        )

        # --- SINGLE CHOICE ---
        single_choice_q = Question(
            type=QuestionType.SINGLE_CHOICE,
            translations=make_translations(
                QuestionTranslation,
                {
                    "en": "What is the capital of France?",
                    "es": "¿Cuál es la capital de Francia?",
                },
            ),
            options=[
                Option(
                    is_correct=True,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "Paris",
                            "es": "París",
                        },
                    ),
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "Madrid",
                            "es": "Madrid",
                        },
                    ),
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "Astana",
                            "es": "Astana",
                        },
                    ),
                ),
            ],
        )

        # --- MULTI CHOICE ---
        multi_choice_q = Question(
            type=QuestionType.MULTI_CHOICE,
            translations=make_translations(
                QuestionTranslation,
                {
                    "en": "Select all prime numbers",
                    "es": "Selecciona todos los números primos",
                },
            ),
            options=[
                Option(
                    is_correct=True,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "2",
                            "es": "2",
                        },
                    ),
                ),
                Option(
                    is_correct=True,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "3",
                            "es": "3",
                        },
                    ),
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "4",
                            "es": "4",
                        },
                    ),
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "6",
                            "es": "6",
                        },
                    ),
                ),
            ],
        )

        # --- FILL GAP ---
        fill_gap_q = Question(
            type=QuestionType.FILL_GAP,
            translations=make_translations(
                QuestionTranslation,
                {
                    "en": "The chemical symbol for water is ___",
                    "es": "El símbolo químico del agua es ___",
                },
            ),
            options=[
                Option(
                    is_correct=True,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "H2O",
                            "es": "H2O",
                        },
                    ),
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "CO2",
                            "es": "CO2",
                        },
                    ),
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(
                        OptionTranslation,
                        {
                            "en": "H2SO4",
                            "es": "H2SO4",
                        },
                    ),
                ),
            ],
        )

        # --- MATCHING ---

        quiz.questions.extend([single_choice_q, multi_choice_q, fill_gap_q])
        session.add(quiz)
        await session.flush()
        await session.commit()

        print("DB populated successfully")


if __name__ == "__main__":
    asyncio.run(seed_quiz())
