from typing import Any

from utils.generic_utils import T


def is_float(value: str) -> bool:
    try:
        _ = float(value)
        return True
    except ValueError:
        return False


def fst(array: Any) -> Any:
    return array[0]


def snd(array: Any) -> Any:
    return array[1]


def id_func(value: T) -> T:
    return value
