from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from math import sqrt
from random import Random
from typing import List, Dict, Tuple

from more_itertools import ilen

from symbolic_poly.monom import Monom
import cvxpy as cp

from utils.cvxpy_utils import cvxpy_sum_product
from utils.math_utils import combinations_sum
from utils.functional_utils import on_error_return


@dataclass(frozen=True)
class Poly:
    monom_to_coeff: Dict[Monom, float]

    @staticmethod
    def zero() -> Poly:
        return Poly(dict())

    def __getitem__(self, monom: Monom):
        return self.monom_to_coeff.get(monom, 0)

    @cached_property
    def monoms(self) -> List[Monom]:
        return list(self.monom_to_coeff.keys())

    def __add__(self, other: Poly) -> Poly:
        return Poly({monom: self[monom] + other[monom] for monom in set(chain(self.monoms, other.monoms))})

    def __neg__(self):
        return Poly({monom: -coeff for monom, coeff in self.monom_to_coeff.items()})

    def __sub__(self, other: Poly) -> Poly:
        return self.__add__(other.__neg__())

    def __mul__(self, other: Poly) -> Poly:
        monoms_to_coeffs = defaultdict(float)
        for monom1, coeff1 in self.monom_to_coeff.items():
            for monom2, coeff2 in other.monom_to_coeff.items():
                monoms_to_coeffs[monom1 * monom2] += coeff1 * coeff2
        return Poly(dict(monoms_to_coeffs))

    def __str__(self) -> str:
        monoms_sorted = sorted(self.monoms, key=lambda monom: (monom.degree, sorted(monom.variables)))

        def mul_monom_str(monom: Monom) -> str:
            return f'*{monom}' if monom.degree > 0 else ''

        return ' + '.join((f'{self[monom]:.5f}{mul_monom_str(monom)}' for monom in monoms_sorted))

    def normalize(self) -> Poly:
        normalization_factor = sqrt(sum((coeff ** 2 for coeff in self.monom_to_coeff.values())))
        return Poly({monom: coeff / normalization_factor for monom, coeff in self.monom_to_coeff.items()})

    def square(self) -> Poly:
        return self * self

    @staticmethod
    def gen_random(variables: List[str], deg: int, prng: Random) -> Poly:
        monom_to_coeff = dict()
        for monom_deg in range(deg + 1):
            for monom in Monom.all_monoms_in_deg(variables, monom_deg):
                monom_to_coeff[monom] = prng.uniform(-1, 1)
        return Poly(monom_to_coeff)

    # @staticmethod
    # def convex_approximation(variables: List[str], max_deg: int, basis: List[Poly], poly: Poly)\
    #         -> (List[Tuple[float, Poly]], Poly, float):
    #     try:
    #         linear_multipliers = cp.Variable(len(basis))
    #         error_poly = cp.Variable(ilen(combinations_sum(number_of_values=len(variables) + 1, desired_sum=max_deg)))
    #         objective = cp.Minimize(cp.sum_squares(error_poly))
    #         constraints = [multiplier >= 0 for multiplier in linear_multipliers]
    #
    #         monoms = [Monom(dict(zip(variables, exponents))) for deg in range(max_deg + 1)
    #                   for exponents in combinations_sum(number_of_values=len(variables), desired_sum=deg)]
    #
    #         for error, monom in zip(error_poly, monoms):
    #             coefficients = [basis_poly[monom] for basis_poly in basis]
    #             total_coefficient = cvxpy_sum_product(coefficients, list(linear_multipliers))
    #             constraints.append(total_coefficient + error == poly[monom])
    #
    #         problem = cp.Problem(objective, constraints)
    #         result = problem.solve()
    #         result_error_poly = Poly(dict(zip(monoms, error_poly.value)))
    #         multipliers = list(zip(linear_multipliers.value, basis))
    #         return multipliers, result_error_poly, result
    #     except RuntimeError as e:
    #         print(f'Convex Optimization Error: {e}', file=sys.stderr)
    #         return 0, 0, 0

    @staticmethod
    @on_error_return(None)
    def convex_approximation(variables: List[str], max_deg: int, basis: List[Poly], poly: Poly) -> float:
        linear_multipliers = cp.Variable(len(basis))
        constraints = [multiplier >= 0 for multiplier in linear_multipliers]

        monoms = [Monom(dict(zip(variables, exponents))) for deg in range(max_deg + 1)
                  for exponents in combinations_sum(number_of_values=len(variables), desired_sum=deg)]

        sum_squares_error = cp.Constant(0.0)

        for monom in monoms:
            coefficients = [basis_poly[monom] for basis_poly in basis]
            total_coefficient = cvxpy_sum_product(coefficients, list(linear_multipliers))
            sum_squares_error += (poly[monom] - total_coefficient) ** 2

        objective = cp.Minimize(sum_squares_error)
        problem = cp.Problem(objective, constraints)
        result = problem.solve()
        # result_error_poly = Poly(dict(zip(monoms, error_poly.value)))
        # multipliers = list(zip(linear_multipliers.value, basis))
        return result

    @staticmethod
    def calc_approximation_error(num_vars: int, base_polys: int, max_deg: int, sum_polys: int, prng: Random) \
            -> Optional[float]:
        half_deg = max_deg // 2
        variables = [f'x{num}' for num in range(1, num_vars + 1)]
        positive_basis = [Poly.gen_random(variables, half_deg, prng).square().normalize() for _ in range(base_polys)]
        polys_in_sum = [Poly.gen_random(variables, half_deg, prng).square().normalize() for _ in range(sum_polys)]
        sum_poly = sum(polys_in_sum, Poly.zero()).normalize()
        return Poly.convex_approximation(variables, max_deg, positive_basis, sum_poly)

        # for combination, pol in linear_combination:
        #     print(f'{combination} * ({pol}) +')
        # print(f'  + {error}')
        # print(f'   = {sum_poly}')
