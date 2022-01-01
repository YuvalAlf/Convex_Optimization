import operator
from functools import reduce
from typing import List, Iterable

from utils.generic_utils import T


def combinations_sum(number_of_values: int, desired_sum: int) -> Iterable[List[int]]:
    """
    >>> sorted(list(combinations_sum(3, 2)))
    [[0, 0, 2], [0, 1, 1], [0, 2, 0], [1, 0, 1], [1, 1, 0], [2, 0, 0]]
    """
    if number_of_values == 1:
        yield [desired_sum]
    else:
        for number in range(desired_sum + 1):
            for combination in combinations_sum(number_of_values - 1, desired_sum - number):
                combination.append(number)
                yield combination


def math_product(values: Iterable[T]) -> T:
    return reduce(operator.mul, values, 1)
