from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from random import Random
from statistics import median, mean
from typing import List, Optional

import cvxpy as cp

from symbolic_poly.monom import Monom
from symbolic_poly.poly import Poly
from utils.cvxpy_utils import cvxpy_sum_product
from utils.math_utils import combinations_sum
from utils.os_utils import read_text_file


@dataclass
class PolyBase:
    polys: List[Poly]

    @cached_property
    def variables(self):
        return sorted(list({variable for poly in self.polys for variable in poly.variables}))

    @cached_property
    def degree(self):
        return max((poly.degree for poly in self.polys))

    @staticmethod
    def gen_random(variables: List[str], deg: int, num_polys: int, prng: Random) -> PolyBase:
        return PolyBase([Poly.gen_random(variables, deg, prng) for _ in range(num_polys)])

    def normalize_square(self) -> PolyBase:
        return PolyBase([poly.square().normalize() for poly in self.polys])

    def convex_approximation(self, variables: List[str], max_deg: int, poly: Poly) -> float:
        linear_multipliers = cp.Variable(len(self.polys))
        constraints = [multiplier >= 0 for multiplier in linear_multipliers]

        monoms = [Monom.create(dict(zip(variables, exponents))) for deg in range(max_deg + 1)
                  for exponents in combinations_sum(number_of_values=len(variables), desired_sum=deg)]

        sum_squares_error = cp.Constant(0.0)

        for monom in monoms:
            coefficients = [basis_poly[monom] for basis_poly in self.polys]
            total_coefficient = cvxpy_sum_product(coefficients, list(linear_multipliers))
            sum_squares_error += (poly[monom] - total_coefficient) ** 2

        objective = cp.Minimize(sum_squares_error)
        problem = cp.Problem(objective, constraints)
        result = problem.solve()
        return result

    def calc_error(self, variables: List[str], max_deg: int, prng: Random) -> float:
        poly = Poly.gen_random_positive(variables, max_deg // 2, prng)
        return self.convex_approximation(variables, max_deg, poly)

    @staticmethod
    def calc_average_error(poly_base: PolyBase, validation_polys: List[Poly], variables: List[str]) -> float:
        errors = [poly_base.convex_approximation(variables, poly_base.degree, poly) for poly in validation_polys]
        return mean(errors)

    @staticmethod
    def calc_approximation_error(num_vars: int, base_polys: int, max_deg: int, sum_polys: int, prng: Random) \
            -> Optional[float]:
        half_deg = max_deg // 2
        variables = [f'x{num}' for num in range(1, num_vars + 1)]
        polys_in_sum = [Poly.gen_random(variables, half_deg, prng).square().normalize() for _ in range(sum_polys)]
        sum_poly = sum(polys_in_sum, Poly.zero()).normalize()
        poly_basis = PolyBase.gen_random(variables, half_deg, base_polys, prng).normalize_square()
        return poly_basis.convex_approximation(variables, max_deg, sum_poly)

    def encode_text(self) -> str:
        return '\n'.join((poly.encode_text() for poly in self.polys))

    @staticmethod
    def decode_text(path: str) -> PolyBase:
        content = read_text_file(path)
        lines = content.split('\n')
        polys = list(map(Poly.decode_text, lines))
        return PolyBase(polys)
