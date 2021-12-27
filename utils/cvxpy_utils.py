from typing import List

from cvxpy import Expression


def cvxpy_sum_product(coefficients: List[float], variables: List[Expression]) -> Expression:
    total = 0
    for coefficient, variable in zip(coefficients, variables):
        total = total + coefficient * variable
    return total


def cvxpy_sum_expr(expressions: List[Expression]) -> Expression:
    total = 0
    for expr in expressions:
        total = total + expr
    return total


def cvxpy_mul_expr(expressions: List[Expression]) -> Expression:
    total = 1
    for expr in expressions:
        total = total * expr
    return total
