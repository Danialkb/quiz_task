from uuid import uuid4

import pytest

from db.models import Option


@pytest.fixture
def correct_option():
    return Option(id=uuid4(), is_correct=True)


@pytest.fixture
def wrong_option():
    return Option(id=uuid4(), is_correct=False)


@pytest.fixture
def left_option():
    return Option(id=uuid4(), is_left=True)


@pytest.fixture
def right_option():
    return Option(id=uuid4(), is_left=False)
