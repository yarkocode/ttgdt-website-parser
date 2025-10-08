from datetime import datetime

normilize_group_number = lambda number: number.strip().replace('.', ',')
normilize_group_number.__doc__ = """
Replace unsupported chars from string group number in changes
:param number: group number
:type number: str
:return: normalized group number string
"""


def is_time(maybe_time: str) -> bool:
    """
    Check string contains a time
    :param maybe_time: estimated time in the string
    :return: True if contains a time
    """
    if len(maybe_time) > 4 or \
            len(maybe_time.split(',')) > 2 or \
            len(maybe_time.split('.')) < 2:
        return False

    try:
        datetime.strptime(maybe_time, '%H.%M')
        return True
    except ValueError:
        return False
