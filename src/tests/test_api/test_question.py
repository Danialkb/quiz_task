from uuid import uuid4
from httpx import AsyncClient
from fastapi import status

from enums.question_type import QuestionType

ENDPOINT = "/api/v1/quizzes/{quiz_id}/questions"


async def test_get_questions_empty_quiz(async_client: AsyncClient, test_quiz):
    response = await async_client.get(
        ENDPOINT.format(quiz_id=test_quiz.id),
        headers={
            "X-User-ID": str(uuid4()),
            "X-Language": "en",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_get_questions_with_one_question(
    async_client: AsyncClient, test_question
):
    response = await async_client.get(
        ENDPOINT.format(quiz_id=test_question.quiz_id),
        headers={
            "X-User-ID": str(uuid4()),
            "X-Language": "en",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == "Test Question"
    assert data[0]["type"] == QuestionType.SINGLE_CHOICE
    assert data[0]["options"] == []


async def test_get_questions_with_options(
    async_client: AsyncClient, test_question_with_options
):
    response = await async_client.get(
        ENDPOINT.format(quiz_id=test_question_with_options.quiz_id),
        headers={
            "X-User-ID": str(uuid4()),
            "X-Language": "en",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    question = data[0]
    assert question["text"] == "Select correct options"
    assert question["type"] == QuestionType.MULTI_CHOICE
    assert len(question["options"]) == 2
    assert {o["text"] for o in question["options"]} == {
        "Correct option",
        "Wrong option",
    }


async def test_get_questions_multilang(
    async_client: AsyncClient, test_question_with_multilang
):
    en_response = await async_client.get(
        ENDPOINT.format(quiz_id=test_question_with_multilang.quiz_id),
        headers={
            "X-User-ID": str(uuid4()),
            "X-Language": "en",
        },
    )
    en_data = en_response.json()
    assert en_data[0]["text"] == "English question"
    assert en_data[0]["options"][0]["text"] == "English option"

    es_response = await async_client.get(
        ENDPOINT.format(quiz_id=test_question_with_multilang.quiz_id),
        headers={
            "X-User-ID": str(uuid4()),
            "X-Language": "es",
        },
    )
    es_data = es_response.json()
    assert es_data[0]["text"] == "Pregunta en español"
    assert es_data[0]["options"][0]["text"] == "Opción en español"


async def test_get_questions_nonexistent_quiz(async_client: AsyncClient):
    response = await async_client.get(
        ENDPOINT.format(quiz_id=uuid4()),
        headers={
            "X-User-ID": str(uuid4()),
            "X-Language": "en",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_get_questions_invalid_user_id(async_client: AsyncClient, test_quiz):
    response = await async_client.get(
        ENDPOINT.format(quiz_id=test_quiz.id),
        headers={
            "X-User-ID": "invalid_id",
            "X-Language": "en",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
