from typing import Any

__all__ = ['is_element']


def is_element(v: Any) -> bool:
    """
    Check if v is an 'element'
    :param v:
    :return:
    """
    if not isinstance(v, dict):
        return False
    # 'content' seems to not be mandatory
    return 'element' in v
