from random import Random
from typing import List, Iterable, Set

import numpy as np
from sympy import Symbol, Poly

from utils.math_utils import combinations_sum


def all_symbols(poly: Poly) -> Set[Symbol]:
    if isinstance(poly, Symbol):
        return {poly}
    return {symbol for arg in poly.args for symbol in all_symbols(arg)}


def all_coefficients(poly: Poly) -> Iterable[float]:
    yield from poly.as_coefficients_dict().values()


def normalize(poly: Poly) -> Poly:
    sum_squares = sum(coef * coef for coef in all_coefficients(poly))
    return poly / np.sqrt(sum_squares)


def gen_normalized_poly(variables: List[Symbol], deg: int, random: Random) -> Poly:
    poly = Poly(0)
    for current_deg in range(deg + 1):
        for exponents in combinations_sum(number_of_values=len(variables), desired_sum=current_deg):
            coefficient = random.uniform(-1, 1)
            poly += coefficient * sum(exponent * variable for exponent, variable in zip(exponents, variables))
    return normalize(poly)


def poly_to_str(poly: Poly) -> str:
    return str(poly).replace('**', '^')
