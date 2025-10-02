import os.path
from datetime import datetime
from unittest import mock
from unittest.mock import AsyncMock

import pytest

from ttgdtparser.constants import raspisanie_zanyatij
from ttgdtparser.exceptions import WebsiteUnavailableException
from ttgdtparser.parser import parse_lessons


def file_exists(name: str) -> bool:
    return os.path.isfile("extra/" + name)


@pytest.mark.asyncio
async def test_lesson_parsing_successful() -> None:
    if not file_exists("lessons.html"):
        pytest.skip("lessons.html not found in extra/")

    with open("extra/lessons.html", mode='r', encoding='utf-8') as lessons_file:
        html = lessons_file.read()

    mock_response = mock.Mock()
    mock_response.status = 200
    mock_response.text = mock.AsyncMock(return_value=html)
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    mock_session = mock.Mock()
    mock_session.post.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    now = datetime.now()

    with mock.patch('ttgdtparser.parser.ClientSession', return_value=mock_session):
        try:
            result = await parse_lessons(raspisanie_zanyatij(base=True), '121,123,132', now)
        except WebsiteUnavailableException:
            pytest.fail("Mocked website response is wrong")

    assert result is not None
    assert len(result) != 0
    assert result[0].date == now

    print("Parsed {} results per date {}".format(len(result), now.date()))
    for lesson in result:
        print(lesson.index, lesson.discipline)


@pytest.mark.asyncio
async def test_lesson_parsing_webpage_not_found() -> None:
    mock_response = mock.Mock()
    mock_response.status = 404
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    mock_session = mock.Mock()
    mock_session.post.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    with mock.patch('ttgdtparser.parser.ClientSession', return_value=mock_session):
        with pytest.raises(WebsiteUnavailableException) as e:
            await parse_lessons(raspisanie_zanyatij(base=True), '121,123,132', datetime.now())

        print("Successful exception: {}".format(e))


@pytest.mark.asyncio
async def test_lesson_parsing_website_unavailable() -> None:
    mock_response = mock.Mock()
    mock_response.status = 500
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    mock_session = mock.Mock()
    mock_session.post.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    with mock.patch('ttgdtparser.parser.ClientSession', return_value=mock_session):
        with pytest.raises(WebsiteUnavailableException) as e:
            await parse_lessons(raspisanie_zanyatij(base=True), '121,123,132', datetime.now())

        print("Successful exception: {}".format(e))
