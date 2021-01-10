"""Util functions for movie link app"""


def parse_value(func, value):
    """Cast a value based on func

    :return parsed value or None if ValueError is raised
    """
    try:
        return func(value)
    except ValueError:
        return None
