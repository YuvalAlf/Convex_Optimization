from typing import List

from cvxpy import Expression


def cvxpy_sum_product(coefficients: List[float], variables: List[Expression]) -> Expression:
    return sum(coefficient * expr for coefficient, expr in zip(coefficients, variables))
