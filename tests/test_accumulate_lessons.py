import asyncio
import os
from datetime import datetime
from unittest import mock

import pytest

from src.ttgdtparser.accumulator import accumulate_lessons
from src.ttgdtparser.constants import raspisanie_zanyatij, zam
from src.ttgdtparser.parser import parse_lessons, parse_changes


def file_exists(name: str) -> bool:
    return os.path.isfile("tests/mock_website/" + name)


def get_mock_session(mock_response) -> mock.Mock:
    mock_session = mock.Mock()
    mock_session.post.return_value = mock_response
    mock_session.__aenter__ = mock.AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = mock.AsyncMock(return_value=None)
    return mock_session


@pytest.fixture(scope='module')
def mock_session_lessons() -> mock.Mock:
    if not file_exists("lessons.html"):
        pytest.skip("lessons.html not found in mock_website/")

    with open("tests/mock_website/lessons.html", mode='r', encoding='utf-8') as lessons_file:
        html = lessons_file.read()

    mock_response = mock.Mock()
    mock_response.status = 200
    mock_response.text = mock.AsyncMock(return_value=html)
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    return get_mock_session(mock_response)


@pytest.fixture(scope='module')
def mock_session_changes(mock_session_lessons) -> mock.Mock:
    if not file_exists("changes.html"):
        pytest.skip("changes.html not found in mock_website/")

    with open("tests/mock_website/changes.html", mode='r', encoding='utf-8') as lessons_file:
        html = lessons_file.read()

    mock_response = mock.Mock()
    mock_response.status = 200
    mock_response.text = mock.AsyncMock(return_value=html)
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    return get_mock_session(mock_response)


@pytest.mark.asyncio
async def test_accumulate_lessons(mock_session_lessons, mock_session_changes):
    date = datetime(year=2025, month=10, day=2)
    gr_no = "543,552"
    lessons, changes = await asyncio.gather(
        parse_lessons(raspisanie_zanyatij(base=True), gr_no, date),
        parse_changes(zam(base=True))
    )
    filtered_changes = list(filter(lambda change: change.date == date, changes.get(gr_no)))
    accumulated = accumulate_lessons(lessons, filtered_changes)

    print("Successfully accumulated lessons {} per group {}".format(len(accumulated), gr_no))
    for lesson in accumulated:
        print(lesson.index, lesson.change.discipline if lesson.has_difference else lesson.discipline, sep=" -- ")

