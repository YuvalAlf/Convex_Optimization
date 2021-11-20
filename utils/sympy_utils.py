from typing import Set, Iterable

from sympy import Expr, Symbol


def get_symbols(expression: Expr) -> Set[Symbol]:
    if isinstance(expression, Symbol):
        return {expression}
    return {symbol for arg in expression.args for symbol in get_symbols(arg)}


def poly_to_str(poly: Expr) -> str:
    return str(poly).replace('**', '^')


def all_coefficients(poly: Expr) -> Iterable[float]:
    yield from poly.as_coefficients_dict().values()
