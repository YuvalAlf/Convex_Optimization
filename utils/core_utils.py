from typing import Any, Tuple

from utils.functional_utils import curry
from utils.generic_utils import T


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


@curry
def not_equal(x1: bool, x2: Any) -> bool:
    return x1 != x2


def fst(array: Tuple[T, Any]) -> T:
    return array[0]


def snd(array: Tuple[Any, T]) -> T:
    return array[1]
