from typing import List, Iterable

import numpy as np
from sympy import Symbol, Expr

from utils.functional_utils import apply_to_result
from utils.random_utils import prng
from utils.sympy_utils import all_coefficients


def gen_base_poly(symbols: List[Symbol]) -> Expr:
    return sum(prng.uniform(-1, 1) * symbol for symbol in symbols) ** 2


def normalize(poly: Expr) -> Expr:
    coefficients = list(all_coefficients(poly.expand()))
    sum_squares = sum(coeff ** 2 for coeff in coefficients)
    return poly / np.sqrt(float(sum_squares))


@apply_to_result(list)
def gen_basis(symbols: List[Symbol], basis_size: int, num_inner_squares: int) -> Iterable[Expr]:
    for _ in range(basis_size):
        basis_before_normalization = sum(gen_base_poly(symbols) for _ in range(num_inner_squares))
        print('-' * 40)
        print('Before Normalization:')
        print(f'\t{basis_before_normalization}')
        basis_after_normalization = normalize(basis_before_normalization)
        print('After Normalization:')
        print(f'\t{basis_after_normalization}')
        print('After Normalization, expended:')
        print(f'\t{basis_after_normalization.expand()}')
        yield basis_after_normalization


def calc_quality_measure(base_polys, another_poly):
    pass


def main():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    symbols = [x, y, z]
    first_base, *base_polys = list(gen_basis(symbols, basis_size=4, num_inner_squares=2))
    print('#' * 40)
    print('#' * 40)


if __name__ == '__main__':
    main()
