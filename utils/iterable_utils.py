from typing import Callable, Iterable, List, Tuple

from utils.generic_utils import V, T


def map_list(func: Callable[[T], V], items: Iterable[T]) -> List[V]:
    return list(map(func, items))


def enumerate1(items: Iterable[T]) -> Iterable[Tuple[int, T]]:
    return enumerate(items, 1)
