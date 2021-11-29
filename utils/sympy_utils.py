import re
from typing import Any, List

from sympy import Expr, Poly

from utils.core_utils import is_float


def eval_sympy_str(string: str) -> Any:
    """
    >>> eval_sympy_str('(0.2 + 0.8) * x1 * x2*y^4')
    1.0*x1*x2*y**4
    """
    string = string.replace('^', '**')
    unique_variables = {value for value in re.split(r"[\+\*\-\(\)\=\/\ ]", string)
                        if len(value) > 0 and not is_float(value)}
    for variable in unique_variables:
        exec(f"{variable} = Symbol('{variable}')")
    return eval(string)


def sum_expr(expressions: List[Expr]) -> Poly:
    total = 0
    for expr in expressions:
        total = total + expr
    return total.as_poly()

