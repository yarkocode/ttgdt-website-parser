from typing import List

from .types import Lesson, Change


def accumulate_lessons(lessons: list[Lesson], changes: List[Change]) -> list[Lesson]:
    result = []

    for change in changes:
        if change.index_is_time:
            result.append(change)
            continue

        if change.discipline.lower() == 'нет':
            continue

        selected_indexes = list(filter(lambda l: l.index in change.subindexation, lessons))

        if len(selected_indexes) == 0:
            result.append(change)
            continue

        for lesson in selected_indexes:
            lesson.change = change

            if change.by_base:
                change.discipline = lesson.discipline

            result.append(lesson)

    unfilled = list(filter(lambda l: l.index not in [l.index for l in changes], lessons))
    result.extend(unfilled)

    return result
