import os
from datetime import datetime
from unittest import mock
from unittest.mock import AsyncMock

import pytest

from src.ttgdtparser.constants import zam
from src.ttgdtparser.exceptions import WebsiteUnavailableException
from src.ttgdtparser.parser import parse_changes


def file_exists(name: str) -> bool:
    return os.path.isfile("extra/" + name)


@pytest.mark.asyncio
async def test_changes_parsing_successful() -> None:
    if not file_exists("changes.html"):
        pytest.skip("lessons.html not found in extra/")

    with open("extra/changes.html", mode='r', encoding='utf-8') as changes_file:
        html = changes_file.read()

    mock_response = mock.Mock()
    mock_response.status = 200
    mock_response.text = mock.AsyncMock(return_value=html)
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    mock_session = mock.Mock()
    mock_session.get.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    with mock.patch('src.ttgdtparser.parser.ClientSession', return_value=mock_session):
        try:
            result = await parse_changes(zam(base=True))
        except WebsiteUnavailableException:
            pytest.fail("Mocked website response is wrong")

    assert len(result) > 0
    assert len(result.get('741')) > 0

    october_2 = datetime(year=2025, month=10, day=2)
    october_3 = datetime(year=2025, month=10, day=3)

    assert result.get('741')[0].date == october_2 or result.get('741')[0].date == october_3

    print("Successfully parsed {} results".format(len(result)))

    assert all(len(result[group]) <= 8 for group in result.keys()), "One or more groups have more than 8 results"

    for group in result:
        print(group, f"changes {len(result.get(group))}", sep=' -- ')


@pytest.mark.asyncio
async def test_lesson_parsing_webpage_not_found() -> None:
    mock_response = mock.Mock()
    mock_response.status = 404
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    mock_session = mock.Mock()
    mock_session.get.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    with mock.patch('src.ttgdtparser.parser.ClientSession', return_value=mock_session):
        with pytest.raises(WebsiteUnavailableException) as e:
            await parse_changes(zam(base=True))

        print("Successful exception: {}".format(e))


@pytest.mark.asyncio
async def test_lesson_parsing_website_unavailable() -> None:
    mock_response = mock.Mock()
    mock_response.status = 500
    mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mock.AsyncMock(return_value=None)

    mock_session = mock.Mock()
    mock_session.get.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    with mock.patch('src.ttgdtparser.parser.ClientSession', return_value=mock_session):
        with pytest.raises(WebsiteUnavailableException) as e:
            await parse_changes(zam(base=True))

        print("Successful exception: {}".format(e))
