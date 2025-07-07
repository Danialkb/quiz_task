import pytest
from uuid import uuid4
from httpx import AsyncClient
from fastapi import status

ENDPOINT = "/api/v1/quizzes/"


@pytest.mark.asyncio
async def test_list_quizzes_invalid_user_id(async_client: AsyncClient):
    headers = {
        "X-User-ID": "INVALID ID",
        "X-Language": "en",
    }
    response = await async_client.get(ENDPOINT, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid X-User-ID format" in response.json().get("detail", "")


@pytest.mark.asyncio
async def test_list_empty_quizzes(async_client: AsyncClient):
    headers = {
        "X-User-ID": str(uuid4()),
        "X-Language": "en",
    }
    response = await async_client.get(ENDPOINT, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_quizzes_with_data(async_client: AsyncClient, test_quiz):
    headers = {
        "X-User-ID": str(uuid4()),
        "X-Language": "en",
    }
    response = await async_client.get(ENDPOINT, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "English Title"


@pytest.mark.asyncio
async def test_get_quiz_not_found(async_client: AsyncClient):
    quiz_id = uuid4()
    headers = {
        "X-User-ID": str(uuid4()),
        "X-Language": "en",
    }
    response = await async_client.get(f"{ENDPOINT}{quiz_id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_quiz_success(async_client: AsyncClient, test_quiz):
    headers = {
        "X-User-ID": str(uuid4()),
        "X-Language": "en",
    }
    response = await async_client.get(f"{ENDPOINT}{test_quiz.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "English Title"


@pytest.mark.asyncio
async def test_get_quiz_with_different_language(
    async_client: AsyncClient,
    test_quiz,
):
    en_headers = {
        "X-User-ID": str(uuid4()),
        "X-Language": "en",
    }
    en_response = await async_client.get(
        f"{ENDPOINT}{test_quiz.id}",
        headers=en_headers
    )
    assert en_response.json()["title"] == "English Title"

    ru_headers = {
        "X-User-ID": str(uuid4()),
        "X-Language": "es",
    }
    ru_response = await async_client.get(
        f"{ENDPOINT}{test_quiz.id}",
        headers=ru_headers
    )
    assert ru_response.json()["title"] == "Nombre español"
