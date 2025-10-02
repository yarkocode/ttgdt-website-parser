from datetime import datetime

normilize_group_number = lambda number: number.strip().replace('.', ',')


def is_time(maybe_time: str):
    if len(maybe_time) > 4 or \
            len(maybe_time.split(',')) > 2 or \
            len(maybe_time.split('.')) < 2:
        return False

    try:
        datetime.strptime(maybe_time, '%H.%M')
        return True
    except ValueError:
        return False
