from typing import List

from cvxpy import Expression


def sum_product(coefficients: List[float], variables: List[Expression]) -> Expression:
    total = 0
    for coefficient, variable in zip(coefficients, variables):
        total = total + coefficient * variable
    return total
