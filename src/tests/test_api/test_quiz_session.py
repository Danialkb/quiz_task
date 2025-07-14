import pytest
from uuid import uuid4
from httpx import AsyncClient
from fastapi import status

ENDPOINT = "/api/v1/quiz_sessions"


async def test_create_quiz_session_success(
    async_client: AsyncClient,
    test_quiz,
    test_user_id,
):
    response = await async_client.post(
        ENDPOINT,
        json={"quiz_id": str(test_quiz.id)},
        headers={"X-User-ID": test_user_id},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["quiz_id"] == str(test_quiz.id)
    assert data["user_id"] == test_user_id


async def test_create_quiz_session_nonexistent_quiz(
    async_client: AsyncClient,
    test_user_id,
):
    response = await async_client.post(
        ENDPOINT, json={"quiz_id": str(uuid4())}, headers={"X-User-ID": test_user_id}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_quiz_session_invalid_user_id(
    async_client: AsyncClient,
    test_quiz,
):
    response = await async_client.post(
        ENDPOINT,
        json={"quiz_id": str(test_quiz.id)},
        headers={"X-User-ID": "invalid_id"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_quiz_sessions_empty(
    async_client: AsyncClient,
    test_user_id,
):
    response = await async_client.get(
        ENDPOINT, headers={"X-User-ID": test_user_id, "X-Language": "en"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_get_quiz_sessions(
    async_client: AsyncClient, test_quiz_session, test_user_id
):
    response = await async_client.get(
        ENDPOINT, headers={"X-User-ID": test_user_id, "X-Language": "en"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["quiz"]["id"] == str(test_quiz_session.quiz_id)
    assert data[0]["finished_at"] is None


async def test_finish_quiz_session_success(
    async_client: AsyncClient, test_quiz_session, test_user_id
):
    response = await async_client.post(
        f"{ENDPOINT}/{test_quiz_session.id}/finish", headers={"X-User-ID": test_user_id}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(test_quiz_session.id)
    assert data["user_id"] == test_user_id
    assert data["quiz_id"] == str(test_quiz_session.quiz_id)
    assert data["finished_at"] is not None
    assert data["percentile"] == 100


async def test_finish_nonexistent_quiz_session(async_client: AsyncClient, test_user_id):
    response = await async_client.post(
        f"{ENDPOINT}/{uuid4()}/finish", headers={"X-User-ID": test_user_id}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
