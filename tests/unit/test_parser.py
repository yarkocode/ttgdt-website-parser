from datetime import datetime
from datetime import datetime
from typing import Dict
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from aiohttp import ClientSession

from src.ttgdtparser.constants import raspisanie_zanyatij, zam, groups, addictions
from src.ttgdtparser.exc.http import EndpointNotFoundException, ResourceUnavailableException, \
    WebsiteDomainMovedException, WebsiteDownException
from src.ttgdtparser.parser import AddictionsParser, LessonTableParser, ChangesTableParser, GroupsParser
from src.ttgdtparser.types import Change, Group, Lesson
from tests.unit.test_data import changes_expected, all_groups


@pytest.fixture
def lessons_html_content():
    with open("tests/mock_website/lessons.html", "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def changes_html_content():
    with open("tests/mock_website/changes.html", "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def groups_html_content():
    with open("tests/mock_website/groups.html", "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def invalid_group_html_content():
    with open("tests/mock_website/invalid_group.html", "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def addictions_html_content():
    with open("tests/mock_website/addictions.html", "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def get_mock_session():
    def _get_session(html: str, status_code: int = 200):
        mock_session = ClientSession()
        mock_session.get = MagicMock()
        mock_session.post = MagicMock()

        mock_session.get.return_value.__aenter__.return_value.status = status_code
        mock_session.get.return_value.__aenter__.return_value.text.return_value = html

        mock_session.post.return_value.__aenter__.return_value.status = status_code
        mock_session.post.return_value.__aenter__.return_value.text.return_value = html
        mock_session.__aexit__ = AsyncMock(return_value=None)

        return mock_session

    return _get_session


class TestParserExpectations():  # т.к. у всех парсеров одна наследственность,
    @pytest.mark.asyncio  # тестировать у всех не имеет смысла
    async def test_website_down(self):
        parser = LessonTableParser("https://mock.codes/500")

        try:
            _ = await parser.parse(group="121,123,132", date=datetime(2025, 10, 14))
        except WebsiteDownException:
            assert True
            return
        assert False

    @pytest.mark.asyncio
    async def test_website_not_found(self):
        parser = LessonTableParser("https://mock.codes/404")

        try:
            _ = await parser.parse(group="121,123,132", date=datetime(2025, 10, 14))
        except EndpointNotFoundException:
            assert True
            return
        assert False

    @pytest.mark.asyncio
    async def test_website_moved(self):
        parser = LessonTableParser("https://mock.codes/301")

        try:
            _ = await parser.parse(group="121,123,132", date=datetime(2025, 10, 14))
        except WebsiteDomainMovedException:
            assert True
            return
        assert False

    @pytest.mark.asyncio
    async def test_website_unavailable(self):
        parser = LessonTableParser("https://mock.codes/401")

        try:
            _ = await parser.parse(group="121,123,132", date=datetime(2025, 10, 14))
        except ResourceUnavailableException:
            assert True
            return
        assert False


class TestParserParseLessons:
    @pytest_asyncio.fixture()
    async def parser(self, get_mock_session, lessons_html_content):
        session = get_mock_session(lessons_html_content)
        return LessonTableParser(raspisanie_zanyatij(), session=session)

    @pytest.mark.parametrize('group,date,expected', [
        ('121,123,132', datetime(2025, 10, 14),
         [
             Lesson(index='1', discipline='Транспортно-экспедиционная деятельность (по видам транспорта)', \
                    teacher="Савко С.Ф.", room="202", date=datetime(2025, 10, 14), by_even_weeks=None),
             Lesson(index='2', discipline='Автоматизированные системы управления на транспорте (по видам транспорта)', \
                    teacher="Черкасова К.А.", room="308", date=datetime(2025, 10, 14), by_even_weeks=None),
             Lesson(index='3', discipline='Обеспечение грузовых перевозок (по видам транспорта)', \
                    teacher="Дениженко Е.Г.", room="310", date=datetime(2025, 10, 14), by_even_weeks=None),
         ]
         ),
        ('121,123,132', datetime(2025, 10, 15),
         [
             Lesson(index='1',
                    discipline='Организация пассажирских перевозок и обслуживание пассажиров (по видам транспорта)', \
                    teacher="Криворотова М.В.", room="401", date=datetime(2025, 10, 15), by_even_weeks=None),
             Lesson(index='2', discipline='Обеспечение грузовых перевозок (по видам транспорта)', \
                    teacher="", room="310", date=datetime(2025, 10, 15), by_even_weeks=False),
             Lesson(index='2', discipline='Автоматизированные системы управления на транспорте (по видам транспорта)', \
                    teacher="", room="308", date=datetime(2025, 10, 15), by_even_weeks=True),
             Lesson(index='3', discipline='Автоматизированные системы управления на транспорте (по видам транспорта)', \
                    teacher="Черкасова К.А.", room="308", date=datetime(2025, 10, 15), by_even_weeks=None),
         ]
         ),
    ])
    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_parse_lessons_per_group_and_date(self, parser: LessonTableParser, group: str, date: datetime,
                                                    expected: list[Lesson]):
        parsed_lessons: list[Lesson] = await parser.parse(group=group, date=date)
        assert len(parsed_lessons) == len(expected)
        for i, (parsed, expected_lesson) in enumerate(zip(parsed_lessons, expected)):
            assert parsed.index == expected_lesson.index
            assert parsed.discipline == expected_lesson.discipline
            assert parsed.teacher == expected_lesson.teacher
            assert parsed.room == expected_lesson.room
            assert parsed.date.date() == expected_lesson.date.date()
            assert parsed.by_even_weeks == expected_lesson.by_even_weeks

    @pytest.mark.parametrize('group,date,expected', [
        ('121,123,132', datetime(2025, 10, 12), [])
    ])
    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_parse_lessons_for_unsupported_date(self, parser: LessonTableParser, group: str, date: datetime,
                                                      expected: list[Lesson]):
        parsed_lessons = await parser.parse(group=group, date=date)
        assert parsed_lessons == expected

    @pytest.mark.parametrize('group,date,expected', [
        ("12321123", datetime(2025, 10, 14), [])
    ])
    @pytest.mark.asyncio
    async def test_parse_lessons_for_unsupported_group(self, group: str, date: datetime, expected: list[Lesson], \
                                                       invalid_group_html_content: str, get_mock_session):
        mock_session = get_mock_session(invalid_group_html_content)
        parser = LessonTableParser(raspisanie_zanyatij(), session=mock_session)

        parsed_lessons = await parser.parse(group=group, date=date)
        assert parsed_lessons == expected


class TestParserParseChanges:  # Общая дата в html-файле: 3 октября 2025, 2 октября 2025

    @pytest_asyncio.fixture()
    async def parser(self, get_mock_session, changes_html_content):
        session = get_mock_session(changes_html_content)
        return ChangesTableParser(zam(), session=session)

    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_parse_changes(self, parser: ChangesTableParser, expected: list[Change] = changes_expected):
        parsed_changes = await parser.parse()

        assert len(parsed_changes) == len(expected)
        for gr, changes in parsed_changes.items():
            try:
                assert len(changes) == len(expected[gr])
                for change in changes:
                    assert change in expected[gr]
            except AssertionError:
                print(gr)
                print(changes)
                print(expected[gr])
                raise

    @pytest.mark.parametrize('group', [
        ("741")
    ])
    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_parse_changes_per_group(self, parser: ChangesTableParser, group: str,
                                           expected: list[Change] = changes_expected):
        parsed_changes = await parser.parse(group=group)

        expected = {gr: expected[gr] for gr in expected if gr == group}

        assert len(parsed_changes) == len(expected)
        for gr, changes in parsed_changes.items():
            try:
                assert len(changes) == len(expected[gr])
                for change in changes:
                    assert change in expected[gr]
            except AssertionError:
                print(gr)
                print(changes)
                print(expected[gr])
                raise

    @pytest.mark.parametrize('group', [
        ("8019237")
    ])
    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_parse_lessons_for_unsupported_group(self, parser: ChangesTableParser, group: str):
        parsed_changes = await parser.parse(group=group)
        assert parsed_changes == {}


class TestParserParseGroups:
    @pytest_asyncio.fixture()
    async def parser(self, get_mock_session, groups_html_content):
        session = get_mock_session(groups_html_content)
        return GroupsParser(groups(), session=session)

    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_parse_groups(self, parser: GroupsParser, alive_groups: list[Group] = all_groups):
        parsed_groups = await parser.parse()
        assert parsed_groups == alive_groups

    @pytest.mark.parametrize("group,result", [
        ("121,123,132", True),
        ("531-П", True),
        ("123", False),
        ("899", False),
    ])
    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_check_group_is_alive(self, parser: GroupsParser, group: str, result: bool):
        assert await parser.is_alive(group) == result


class TestParserAddictions:

    @pytest_asyncio.fixture()
    async def parser(self, get_mock_session, addictions_html_content):
        session = get_mock_session(addictions_html_content)
        return AddictionsParser(addictions(), session=session)

    @pytest.mark.parametrize('date,expected', [
        (datetime(2025, 10, 20),  # понедельник, там нет пар
         {
             "251-П, 253-П": [],
             "551-П": [],
             "141,152 143,154": [],
             "241-П": [],
             "541-П": [],
             "231-П": [],
         }
         ),
        (datetime(2025, 10, 21),  # вторник
         {
             "251-П, 253-П": [],
             "551-П": [
                 Lesson(index=4, by_even_weeks=True, teacher="Гаврилова Е.А.", room="612", date=datetime(2025, 10, 21),
                        discipline="Математика")],
             "141,152 143,154": [Lesson(index=0, by_even_weeks=None, teacher="Криворотова М.В.", room="401",
                                        date=datetime(2025, 10, 21),
                                        discipline="Введение в теорию решения изобретательских задач, в т.ч. основы инженерных расчетов")],
             "241-П": [
                 Lesson(index=0, by_even_weeks=None, teacher="Архипова Ю.В.", room="405", date=datetime(2025, 10, 21),
                        discipline="Введение в теорию решения изобретательских задач, в т.ч. основы инженерных расчетов")],
             "541-П": [
                 Lesson(index=4, by_even_weeks=None, teacher="Трифонова Е.Г.", room="604", date=datetime(2025, 10, 21),
                        discipline="Введение в теорию решения изобретательских задач, в т.ч. основы инженерных расчетов")],
             "231-П": [
                 Lesson(index=4, by_even_weeks=False, teacher="Архипова Ю.В.", room="405", date=datetime(2025, 10, 21),
                        discipline="Перегонные системы автоматики"),
                 Lesson(index=4, by_even_weeks=True, teacher="Архипова Ю.В.", room="405", date=datetime(2025, 10, 21),
                        discipline="Линии автоматики и телемеханики"),
             ],
         }
         )
    ])
    @pytest.mark.usefixtures('parser')
    @pytest.mark.asyncio
    async def test_parse_addictions(self, parser: AddictionsParser, date: datetime, expected: Dict[str, list[Lesson]]):
        parsed_addictions = await parser.parse(date=date)
        assert len(parsed_addictions) == len(expected)

        for group, lessons in parsed_addictions.items():
            assert len(lessons) == len(expected[group])
            for lesson in lessons:
                assert lesson in expected[group]
        print(parsed_addictions)
