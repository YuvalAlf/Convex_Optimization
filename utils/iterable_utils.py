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


def min_by(by: Callable[[T], K], items: Iterable[T], map_func: Callable[[T], V]) -> V:
    return map_func(min(items, key=by))


def min_arg_min(items: Iterable[T]) -> (int, T):
    return min_by(fst, enumerate(items), id_func)
