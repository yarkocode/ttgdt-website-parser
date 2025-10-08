from typing import List

from .types import Lesson, Change


def accumulate_lessons(lessons: list[Lesson], changes: List[Change]) -> list[Lesson]:
    """
    Aggregate changes with lessons table
    :param lessons: list of lessons from common table
    :param changes: list of changes today
    :return: aggregated list of lessons

    Usage:

    from ttgdtparser import accumulator, parser, constants
    import datetime

    gr_no = "711,722"
    now = datetime.datetime.now()
    lessons = await parser.parse_lessons(constants.raspisanie_zanyatij(), gr_no, now)
    changes = list(filter(lambda l: l.date == now, await parser.parse_changes(constants.zam())[gr_no])

    aggr_lessons = await accumulator.accumulate_lessons(lessons, changes)
    """
    result = []

    # aggregate lessons and changes
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

    # fill with lessons from common table by unfilled indexes
    unfilled = list(filter(lambda l: l.index not in [l.index for l in changes], lessons))
    result.extend(unfilled)

    return result
