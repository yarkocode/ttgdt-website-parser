from abc import ABC
from datetime import datetime, time
from typing import List

import pytest

from src.ttgdtparser.aggregator import Aggregator
from src.ttgdtparser.exc.aggregator import LessonRequiredByIndexForChangeException
from src.ttgdtparser.types import Change, Lesson, BaseLesson, LessonMatch


class TestAggregator(ABC):
    @pytest.fixture(name="aggregator")
    def aggregator(self) -> Aggregator:
        return Aggregator()


class TestAggregatorAccumulateMethod(TestAggregator):
    @pytest.mark.usefixtures("aggregator")
    @pytest.mark.parametrize("lessons,changes,expected", [
        (
                [Lesson(index='1', discipline='ТИС', date=datetime.today())],
                [Change(index="1,2", discipline="Графический дизайн", room="102", date=datetime.today())],
                [
                    Change(index=1, discipline="Графический дизайн", room="102", date=datetime.today()),
                    Change(index=2, discipline="Графический дизайн", room="102", date=datetime.today())
                ]
        ),
        (
                [Lesson(index='1', discipline='ТИС', date=datetime.today())],
                [Change(index="3,4.5", discipline="Физкультура", date=datetime.today())],
                [
                    Lesson(index=1, discipline='ТИС', date=datetime.today()),
                    Change(index=3, discipline="Физкультура", date=datetime.today()),
                    Change(index=4, discipline="Физкультура", date=datetime.today()),
                    Change(index=5, discipline="Физкультура", date=datetime.today())
                ]
        )
    ])
    def test_flat_indexes_in_result_lesson_table(self, aggregator: Aggregator,
                                                 lessons: List[Lesson],
                                                 changes: List[Change],
                                                 expected: List[Change | Lesson]):
        aggr = aggregator.accumulate(lessons, changes)
        assert len(aggr) == len(expected), 'Length of aggregation result has difference with expected'
        assert any(not isinstance(l.index, list) for l in aggr), 'Some or any key has type list (of int)'

    @pytest.mark.usefixtures("aggregator")
    @pytest.mark.parametrize("lessons,changes,expected", [
        (
                [Lesson(index='1', discipline='ТИС', date=datetime.today())],
                [Change(index="1", discipline="Графический дизайн", room="102", date=datetime.today())],
                [
                    Change(index=1, discipline="Графический дизайн", room="102", date=datetime.today())
                ]
        ),
        (
                [
                    Lesson(index='1', discipline='ТИС', date=datetime.today()),
                    Lesson(index='2', discipline='ТИС', date=datetime.today())
                ],
                [Change(index="2", discipline="Физкультура", date=datetime.today())],
                [
                    Lesson(index=1, discipline='ТИС', date=datetime.today()),
                    Lesson(index=2, discipline='Физкультура', date=datetime.today())
                ]
        )
    ])
    def test_include_changes_without_indexes_by_base(self, aggregator: Aggregator,
                                                     lessons: List[Lesson],
                                                     changes: List[Change],
                                                     expected: List[Change | Lesson]) -> None:
        aggr = aggregator.accumulate(lessons, changes)
        assert len(aggr) == len(expected), 'Length of aggregation result has difference with expected'

    @pytest.mark.usefixtures("aggregator")
    @pytest.mark.parametrize("lessons,changes,expected", [
        (
                [Lesson(index='1', discipline='Графический дизайн', room='102', date=datetime.today())],
                [Change(index='1', discipline='По расписанию', room='404', date=datetime.today(), by_base=True)],
                [
                    Lesson(index=1, discipline='Графический дизайн', room='404', date=datetime.today())
                ]
        ),
    ])
    def test_include_changes_with_indexes_by_base(self, aggregator: Aggregator,
                                                  lessons: List[Lesson],
                                                  changes: List[Change],
                                                  expected: List[Change | Lesson]):
        aggr = aggregator.accumulate(lessons, changes)
        assert len(aggr) == len(expected), 'Length of aggregation result has difference with expected'
        assert aggr[0].discipline == expected[0].discipline, 'Discipline name by base has been not changed'

    @pytest.mark.usefixtures("aggregator")
    @pytest.mark.parametrize("lessons,changes", [
        (
                [Lesson(index='1', discipline='Графический дизайн', room='102', date=datetime.today())],
                [Change(index='2', discipline='По расписанию', room='404', date=datetime.today(), by_base=True)]
        )
    ])
    def test_raise_base_lesson_required_for_by_base_flag(self, aggregator: Aggregator,
                                                         lessons: List[Lesson],
                                                         changes: List[Change]):
        with pytest.raises(LessonRequiredByIndexForChangeException):
            aggregator.accumulate(lessons, changes)


class TestAggregatorMatchMethod(TestAggregator):
    @pytest.mark.usefixtures("aggregator")
    @pytest.mark.parametrize("lessons1,lessons2,expected", [
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="101")],
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="102")],
                []
        ),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Физика", room="201")],
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Химия", room="201")],
                []
        ),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Информатика", room="301")],
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Информатика", room="301")],
                [(
                        BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Информатика", room="301"),
                        BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Информатика", room="301")
                )]
        ),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Биология", room="401")],
                [BaseLesson(date=datetime(2023, 9, 1), index='2', discipline="Биология", room="401")],
                []
        ),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="История", room="501")],
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Литература", room="502")],
                []
        ),
        (
                [
                    BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="101"),
                    BaseLesson(date=datetime(2023, 9, 1), index='2', discipline="Физика", room="201"),
                    BaseLesson(date=datetime(2023, 9, 1), index='3', discipline="Химия", room="301")
                ],
                [
                    BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="111"),
                    BaseLesson(date=datetime(2023, 9, 1), index='2', discipline="Биология", room="201"),
                    BaseLesson(date=datetime(2023, 9, 1), index='3', discipline="Химия", room="311")
                ],
                []
        ),
        ([], [], []),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="101")],
                [],
                []
        ),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="101")],
                [BaseLesson(date=datetime(2023, 9, 1), index=time(9, 0), discipline="Математика", room="102")],
                []
        ),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index=[1, 2], discipline="Математика", room="101")],
                [BaseLesson(date=datetime(2023, 9, 1), index=[1, 2], discipline="Математика", room="102")],
                []
        ),
        (
                [Lesson(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="101")],
                [Change(date=datetime(2023, 9, 1), index='1', discipline="Математика", room="102", by_base=False)],
                []
        ),
        (
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Физкультура", room="Спортзал")],
                [BaseLesson(date=datetime(2023, 9, 1), index='1', discipline="Музыка", room="Актовый зал")],
                []
        ),
    ])
    def test_matches_with_changes(self, aggregator: Aggregator,
                                  lessons1: List[Lesson],
                                  lessons2: List[Lesson],
                                  expected: List[LessonMatch]):
        matches = aggregator.find_match(lessons1, lessons2)

        assert len(matches) == len(expected)

        for lesson1, lesson2 in matches:
            assert lesson1.index == lesson2.index, 'Index mismatch'
            assert lesson1.discipline == lesson2.discipline or lesson1.room == lesson2.room, 'Discipline or room mismatch'
