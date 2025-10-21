from datetime import time
from typing import List, Tuple, Union

from .exc.aggregator import LessonRequiredByIndexForChangeException
from .types import Lesson, Change, BaseLesson, LessonMatch

 
class Aggregator:
    def accumulate(self, lessons: List[Lesson], changes: List[Change]) -> List[BaseLesson]:
        lessons_map: dict[int, Lesson] = {l.index: l for l in lessons}
        result_map: dict[int, Union[Lesson, Change]] = {}
        timed_changes: list[Change] = [ch for ch in changes if isinstance(ch.index, time)]

        for change in changes:
            if isinstance(change.index, str) and change.index == "*":
                return [change]

            if isinstance(change.index, list):
                for idx in change.index:
                    original_lesson = lessons_map.get(idx)

                    if original_lesson is None:
                        if change.by_base:
                            raise LessonRequiredByIndexForChangeException(
                                "Lesson by that index could not found to place the change", change.index, change)
                        result_map[idx] = change
                        continue

                    if change.by_base:
                        result_map[idx] = original_lesson
                        continue

                    rchange = change.model_copy()
                    rchange.index = idx
                    rchange.original = original_lesson
                    result_map[idx] = rchange

                continue

            if isinstance(change.index, int):
                original_lesson = lessons_map.get(change.index)

                if original_lesson is None:
                    if change.by_base:
                        raise LessonRequiredByIndexForChangeException(
                            "Lesson by that index could not found to place the change", change.index, change)
                    result_map[change.index] = change
                    continue

                rchange = change.model_copy()
                rchange.original = original_lesson

                if change.by_base:
                    rchange.discipline = lessons_map.get(change.index).discipline

                result_map[rchange.index] = rchange

                continue

        finalres = list(result_map.values())
        finalres.extend(timed_changes)
        delta = lessons_map.keys() - result_map.keys()

        if len(delta) > 0:
            for idx in delta:
                finalres.append(lessons_map.get(idx))

        return finalres

    def find_match(self, lessons_1: List[BaseLesson], lessons_2: List[BaseLesson]) -> List[LessonMatch]:
        matches: List[Tuple[BaseLesson, BaseLesson]] = []

        if len(lessons_1) == 0 or len(lessons_2) == 0:
            return matches

        for lesson_1 in lessons_1:
            for lesson_2 in lessons_2:
                if lesson_1.index == lesson_2.index and self._match(lesson_1, lesson_2):
                    matches.append((lesson_1, lesson_2))

        return matches

    def _match(self, lesson_1: BaseLesson, lesson_2: BaseLesson):
        if lesson_1.discipline == lesson_2.discipline:
            if (lesson_1.room == "" or lesson_2.room == "") or lesson_1.room == lesson_2.room:
                return True

        return False


def accumulate_lessons(lessons: list[Lesson], changes: List[Change]) -> List[BaseLesson]:
    """
    Aggregate changes with lessons table
    :param lessons: list of lessons from common table
    :param changes: list of changes today
    :return: aggregated list of lessons

    Usage:

        from ttgdtparser import aggregator, parser, constants
        import datetime

        gr_no = "711,722"
        now = datetime.datetime.now()
        lessons = await parser.parse_lessons(constants.raspisanie_zanyatij(), gr_no, now)
        changes = list(filter(lambda l: l.date == now, await parser.parse_changes(constants.zam())[gr_no])

        aggr_lessons = await aggregator.accumulate_lessons(lessons, changes)
    """
    aggregator = Aggregator()
    return aggregator.accumulate(lessons, changes)


def find_match(lessons_1: list[BaseLesson], lessons_2: List[BaseLesson]) -> List[LessonMatch]:
    """
    Find matching lessons
    :param lessons_1: list of lessons for first group
    :param lessons_2: list of lessons for second group
    :return: matched lessons for both groups

    Usage:

        from ttgdtparser import aggregator, parser, constants
        import datetime

        lessons_1 = await aggregator.accumulate_lessons(...)
        lessons_2 = await aggregator.accumulate_lessons(...)

        matched_pairs = await aggregator.find_match(lessons_1, lessons_2)
    """
    aggregator = Aggregator()
    return aggregator.find_match(lessons_1, lessons_2)
