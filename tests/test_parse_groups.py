import os.path
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import AsyncMock

import pytest

from src.ttgdtparser.constants import groups
from src.ttgdtparser.exceptions import WebsiteUnavailableException
from src.ttgdtparser.parser import parse_groups
from src.ttgdtparser.types import Group

def file_exists(name: str) -> bool:
    return os.path.isfile("tests/extra/" + name)

@pytest.fixture
def mock_session_factory():
    """Фабрика для создания mock_session с заданным статусом и текстом."""
    async def _create_mock_session(status: int, text: str = ""):
        mock_response = mock.Mock()
        mock_response.status = status
        mock_response.text = mock.AsyncMock(return_value=text)
        mock_response.__aenter__ = mock.AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = mock.AsyncMock(return_value=None)

        mock_session = mock.Mock()
        mock_session.get.return_value = mock_response
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        return mock_session
    return _create_mock_session

@pytest.mark.asyncio
async def test_parse_groups_successful(mock_session_factory) -> None:
    if not file_exists('groups.html'):
        pytest.skip("groups.html not found in extra/")
    
    with open("tests/extra/groups.html", mode='r', encoding='utf-8') as groups_file:
        html = groups_file.read()

    mock_session = await mock_session_factory(200, html)

    with mock.patch('src.ttgdtparser.parser.ClientSession', return_value=mock_session):
        try:
            result = await parse_groups(groups(base=True))
        except WebsiteUnavailableException:
            pytest.fail("Mocked website response is wrong")

    
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0

    print("Parsed {} groups".format(len(result)))

    for item in result:
        assert isinstance(item, Group) 
        assert hasattr(item, 'full_number') 
        assert isinstance(item.full_number, str)
        print(item.full_number)


@pytest.mark.asyncio
async def test_parse_groups_website_unavailable(mock_session_factory) -> None:
    mock_session = await mock_session_factory(500)
    with mock.patch('src.ttgdtparser.parser.ClientSession', return_value=mock_session):
        with pytest.raises(WebsiteUnavailableException) as e:
            await parse_groups(groups(base=True))

        print("Successful exception: {}".format(e.value))

@pytest.mark.asyncio
async def test_parse_groups_webpage_not_found(mock_session_factory) -> None:
    mock_session = await mock_session_factory(404)
    with mock.patch('src.ttgdtparser.parser.ClientSession', return_value=mock_session):
        with pytest.raises(WebsiteUnavailableException) as e:
            await parse_groups(groups(base=True))

        print("Successful exception: {}".format(e.value))