import asyncio

from sqlalchemy import select

from db.models.quiz import Quiz, QuizTitleTranslation
from db.models.question import Question, QuestionTranslation
from db.models.option import Option, OptionTranslation, MatchingOptionCorrectPair
from db.session import async_session
from enums.question_type import QuestionType


def make_translations(model_cls, data: dict[str, str]):
    return [model_cls(language=lang, text=text) for lang, text in data.items()]


async def seed_quiz():
    async with async_session() as session:
        stmt = select(QuizTitleTranslation).filter(QuizTitleTranslation.title == "General Knowledge Quiz")
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            print("Db already populated. Exiting...")
            return

        quiz = Quiz(
            translations=[
                QuizTitleTranslation(language="en", title="General Knowledge Quiz"),
                QuizTitleTranslation(language="es", title="Cuestionario de Conocimientos Generales"),
            ]
        )

        # --- SINGLE CHOICE ---
        single_choice_q = Question(
            type=QuestionType.SINGLE_CHOICE,
            translations=make_translations(QuestionTranslation, {
                "en": "What is the capital of France?",
                "es": "¿Cuál es la capital de Francia?",
            }),
            options=[
                Option(
                    is_correct=True,
                    translations=make_translations(OptionTranslation, {
                        "en": "Paris",
                        "es": "París",
                    })
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(OptionTranslation, {
                        "en": "Madrid",
                        "es": "Madrid",
                    })
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(OptionTranslation, {
                        "en": "Astana",
                        "es": "Astana",
                    })
                ),
            ]
        )

        # --- MULTI CHOICE ---
        multi_choice_q = Question(
            type=QuestionType.MULTI_CHOICE,
            translations=make_translations(QuestionTranslation, {
                "en": "Select all prime numbers",
                "es": "Selecciona todos los números primos",
            }),
            options=[
                Option(
                    is_correct=True,
                    translations=make_translations(OptionTranslation, {
                        "en": "2",
                        "es": "2",
                    })
                ),
                Option(
                    is_correct=True,
                    translations=make_translations(OptionTranslation, {
                        "en": "3",
                        "es": "3",
                    })
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(OptionTranslation, {
                        "en": "4",
                        "es": "4",
                    })
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(OptionTranslation, {
                        "en": "6",
                        "es": "6",
                    })
                ),
            ]
        )

        # --- FILL GAP ---
        fill_gap_q = Question(
            type=QuestionType.FILL_GAP,
            translations=make_translations(QuestionTranslation, {
                "en": "The chemical symbol for water is ___",
                "es": "El símbolo químico del agua es ___",
            }),
            options=[
                Option(
                    is_correct=True,
                    translations=make_translations(OptionTranslation, {
                        "en": "H2O",
                        "es": "H2O",
                    })
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(OptionTranslation, {
                        "en": "CO2",
                        "es": "CO2",
                    })
                ),
                Option(
                    is_correct=False,
                    translations=make_translations(OptionTranslation, {
                        "en": "H2SO4",
                        "es": "H2SO4",
                    })
                )
            ]
        )

        # --- MATCHING ---
        matching_q = Question(
            type=QuestionType.MATCHING,
            translations=make_translations(QuestionTranslation, {
                "en": "Match the animals with their habitats",
                "es": "Relaciona los animales con sus hábitats",
            }),
        )
        left_options = [
            Option(
                is_left=True,
                is_right=False,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Camel",
                    "es": "Camello",
                })
            ),
            Option(
                is_left=True,
                is_right=False,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Penguin",
                    "es": "Pingüino",
                })
            ),
            Option(
                is_left=True,
                is_right=False,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Frog",
                    "es": "Rana",
                })
            ),
            Option(
                is_left=True,
                is_right=False,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Eagle",
                    "es": "Águila",
                })
            ),
        ]

        right_options = [
            Option(
                is_left=False,
                is_right=True,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Desert",
                    "es": "Desierto",
                })
            ),
            Option(
                is_left=False,
                is_right=True,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Antarctica",
                    "es": "Antártida",
                })
            ),
            Option(
                is_left=False,
                is_right=True,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Swamp",
                    "es": "Pantano",
                })
            ),
            Option(
                is_left=False,
                is_right=True,
                is_correct=False,
                translations=make_translations(OptionTranslation, {
                    "en": "Mountains",
                    "es": "Montañas",
                })
            ),
        ]

        matching_q.options.extend(left_options + right_options)

        quiz.questions.extend([single_choice_q, multi_choice_q, fill_gap_q, matching_q])
        session.add(quiz)
        await session.flush()

        correct_matching_pairs = [
            MatchingOptionCorrectPair(
                left_option_id=left_options[0].id,  # Camel
                right_option_id=right_options[0].id,  # Desert
                question_id=matching_q.id,
            ),
            MatchingOptionCorrectPair(
                left_option_id=left_options[1].id,  # Penguin
                right_option_id=right_options[1].id,  # Antarctica
                question_id=matching_q.id,
            ),
            MatchingOptionCorrectPair(
                left_option_id=left_options[2].id,  # Frog
                right_option_id=right_options[2].id,  # Swamp
                question_id=matching_q.id,
            ),
            MatchingOptionCorrectPair(
                left_option_id=left_options[3].id,  # Eagle
                right_option_id=right_options[3].id,  # Mountains
                question_id=matching_q.id,
            ),
        ]
        session.add_all(correct_matching_pairs)
        await session.commit()

        print("DB populated successfully")


if __name__ == "__main__":
    asyncio.run(seed_quiz())
