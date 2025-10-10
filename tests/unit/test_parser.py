from abc import ABC, abstractmethod
from datetime import timedelta, datetime

import pytest

from ttgdtparser.constants import raspisanie_zanyatij, zam, groups
from ttgdtparser.parser import BaseTtgdtWebsiteParser, LessonTableParser, ChangesTableParser, GroupsParser
from ttgdtparser.types import Lesson


class TestParser(ABC):
    @pytest.fixture(name='parser')
    @abstractmethod
    def parser(self) -> BaseTtgdtWebsiteParser:
        raise NotImplementedError('Implement method parser to initialize parser and test it')


class TestParserParseLessons(TestParser):
    def parser(self) -> LessonTableParser:
        return LessonTableParser(raspisanie_zanyatij())

    @pytest.mark.parametrize('group,date,expected', [
        ('711,722', datetime.today(), []),
        ('731',)
    ])
    def test_parse_lessons_per_group(self, parser: LessonTableParser, group: str, expected: list[Lesson]):
        parser.parse(group, )

    def test_parse_lessons_for_unsupported_date(self, parser: LessonTableParser):
        pass


class TestParserParseChanges(TestParser):
    def parser(self) -> ChangesTableParser:
        return ChangesTableParser(zam())

    def test_parse_lessons_per_group(self):
        pass

    def test_parse_lessons_for_unsupported_date(self):
        pass


class TestParserParseGroups(TestParser):
    def parser(self) -> GroupsParser:
        return GroupsParser(groups())

    def test_parse_groups(self, parser: GroupsParser):
        pass

    def test_check_group_is_alive(self):
        pass
