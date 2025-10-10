def is_time(time_repr: str):
    """
    Check string contains a time
    :param time_repr: estimated time in the string
    :return: True if contains a time
    """
    if time_repr is not None:
        if len(time_repr) == 1 or len(time_repr) > 5 or time_repr.count(':') > 1 or time_repr.count(':') == 0:
            return False

        parts = time_repr.split(':')
        return len(parts[1]) == 2

    return False
