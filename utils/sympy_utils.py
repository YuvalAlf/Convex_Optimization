import re
from typing import Any
from sympy import Symbol
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
