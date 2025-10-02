from typing import List

from .types import Lesson, Change


def accumulate_lessons(lessons: list[Lesson], changes: List[Change]) -> list[Lesson]:
    result = []

    for change in changes:
        if change.index_is_time:
            result.append(change)

        if change.discipline.lower() == 'нет':
            continue

        selected_indexes = list(filter(lambda l: l.index in change.subindexation, lessons))

        for lesson in selected_indexes:
            lesson.change = change

            if change.by_base:
                change.discipline = lesson.discipline

            result.append(lesson)

    return result