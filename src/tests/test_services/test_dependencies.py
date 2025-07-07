import pytest
from fastapi import HTTPException
from api.dependencies.user import get_user_id
from api.dependencies.language import get_language
from enums.language import Language
from uuid import uuid4


def test_get_user_id_valid():
    user_id = str(uuid4())
    result = get_user_id(x_user_id=user_id)
    assert str(result) == user_id


def test_get_user_id_invalid():
    with pytest.raises(HTTPException) as exc_info:
        get_user_id(x_user_id="invalid-uuid")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid X-User-ID format"


def test_get_language_valid():
    assert get_language(x_language="en") == "en"
    assert get_language(x_language="es") == "es"


def test_get_language_invalid_or_none():
    assert get_language(x_language="invalid") == Language.ENGLISH.value
    assert get_language(x_language="") == Language.ENGLISH.value
