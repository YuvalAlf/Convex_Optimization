from typing import Callable, Iterable, List, Tuple

from utils.core_utils import fst, id_func
from utils.generic_utils import V, T, K


def map_list(func: Callable[[T], V], items: Iterable[T]) -> List[V]:
    return list(map(func, items))


def enumerate1(items: Iterable[T]) -> Iterable[Tuple[int, T]]:
    return enumerate(items, 1)


def generate(times: int, generator: Callable[[], T]) -> Iterable[T]:
    for _ in range(times):
        yield generator()


def filter_by(by: Callable[[T], V], predicate: Callable[[V], bool], items: Iterable[T]) -> Iterable[T]:
    for item in items:
        if predicate(by(item)):
            yield item


def min_by(by: Callable[[T], K], items: Iterable[T]) -> (K, V):
    return min(((by(item), item) for item in items), key=fst)


def max_by(by: Callable[[T], K], items: Iterable[T]) -> (K, V):
    return max(((by(item), item) for item in items), key=fst)
