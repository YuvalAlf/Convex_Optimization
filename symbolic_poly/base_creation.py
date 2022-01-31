from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from random import Random
from statistics import median
from typing import List, Iterable

from symbolic_poly.poly import Poly
from symbolic_poly.poly_base import PolyBase
from utils.input_utils import get_input


@dataclass
class BaseCreation(ABC):
    base_size: int
    num_variables: int
    degree: int

    @cached_property
    def half_degree(self) -> int:
        return self.degree // 2

    @cached_property
    def variables(self) -> List[str]:
        return [f'x{num}' for num in range(1, self.num_variables + 1)]

    @abstractmethod
    def create_base(self, random: Random) -> Iterable[PolyBase]:
        pass

    @staticmethod
    def get_base_creation_from_user() -> BaseCreation:
        basis_size = get_input('Enter basis size', int, 10)
        num_variables = get_input('Enter number of variables', int, 2)
        degree = get_input('Enter basis degree', int, 6)
        mode = get_input('Enter R for random basis and I for incremental basis', str, 'I')
        if mode == 'R':
            return RandomBaseCreation(basis_size, num_variables, degree)
        if mode == 'I':
            validation_polys = get_input('Enter number of random polynomials to generate to '
                                         'qualify each incremental basis', int, 10)
            sample_polys = get_input('Enter number of random polynomials to generate, '
                                     'from which one will be added to the basis', int, 10)
            return IncrementalBaseCreation(basis_size, num_variables, degree, validation_polys, sample_polys)
        return BaseCreation.get_base_creation_from_user()


@dataclass
class RandomBaseCreation(BaseCreation):
    def create_base(self, prng: Random) -> Iterable[PolyBase]:
        polys = []
        while len(polys) < self.base_size:
            poly = Poly.gen_random(self.variables, self.half_degree, prng)
            polys.append(poly.square().normalize())
            yield PolyBase(polys)


@dataclass
class IncrementalBaseCreation(BaseCreation):
    validation_polys: int
    sample_polys: int

    def calc_median_error(self, poly_base: PolyBase, prng: Random) -> float:
        errors = [poly_base.calc_error(self.variables, self.degree, prng) for _ in range(self.validation_polys)]
        return median(errors)

    def create_base(self, prng: Random) -> Iterable[PolyBase]:
        polys = []
        while len(polys) < self.base_size:
            candidates = [Poly.gen_random(self.variables, self.half_degree, prng).square().normalize()
                          for _ in range(self.sample_polys)]
            best_poly = min(candidates, key=lambda candidate: self.calc_median_error(PolyBase(polys + [candidate]),
                                                                                     prng))
            polys.append(best_poly)
            yield PolyBase(polys)
