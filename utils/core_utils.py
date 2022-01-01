from typing import Any, Tuple

from utils.generic_utils import T


def is_float(value: str) -> bool:
    try:
        _ = float(value)
        return True
    except ValueError:
        return False


def fst(array: Tuple[T, ...]) -> T:
    return array[0]


def snd(array: Tuple[Any, T, ...]) -> T:
    return array[1]
