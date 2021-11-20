from typing import Callable, Iterable, List

from utils.generic_utils import V, T


def map_list(func: Callable[[T], V], items: Iterable[T]) -> List[V]:
    return list(map(func, items))