from random import Random
from typing import List, Iterable, Set

import numpy as np
from sympy import Symbol, Poly, Expr

from cvxpy_utils.cvxpy_utils import cvxpy_mul_expr
from utils.math_utils import combinations_sum

Monomial = Expr


def all_symbols(poly: Poly) -> Set[Symbol]:
    if isinstance(poly, Symbol):
        return {poly}
    return {symbol for arg in poly.args for symbol in all_symbols(arg)}


def all_coefficients(expr: Expr) -> Iterable[float]:
    yield from expr.expand().as_coefficients_dict().values()


def normalize(poly: Poly) -> Poly:
    sum_squares = sum(coefficient * coefficient for coefficient in all_coefficients(poly.as_expr()))
    normalized_poly_expr = poly / np.sqrt(float(sum_squares))
    return normalized_poly_expr.as_poly()


def gen_normalized_poly(variables: List[Symbol], deg: int, random: Random) -> Poly:
    poly = 0
    for current_deg in range(deg + 1):
        for exponents in combinations_sum(number_of_values=len(variables), desired_sum=current_deg):
            coefficient = random.uniform(-1, 1)
            monomial = cvxpy_mul_expr([variable**exponent for variable, exponent in zip(variables, exponents)])
            poly = poly + coefficient * monomial
    return normalize(poly)


def poly_to_str(poly: Poly) -> str:
    return str(poly.as_expr()).replace('**', '^')
