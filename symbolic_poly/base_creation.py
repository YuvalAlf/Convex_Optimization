from __future__ import annotations

import multiprocessing
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from random import Random
from statistics import mean
from tempfile import TemporaryDirectory
from typing import List

from symbolic_poly.poly import Poly
from symbolic_poly.poly_base import PolyBase
from utils.input_utils import get_input
from utils.iterable_utils import min_arg_min
from utils.os_utils import encode_pickle, decode_pickle


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
    def create_base(self, random: Random) -> PolyBase:
        pass

    @staticmethod
    def get_base_creation_from_user() -> BaseCreation:
        basis_size = get_input('Enter basis size', int, 10)
        num_variables = get_input('Enter number of variables', int, 2)
        degree = get_input('Enter basis degree', int, 4)
        mode = get_input('Enter R for random basis and I for incremental basis', str, 'I')
        if mode == 'R':
            return RandomBaseCreation(basis_size, num_variables, degree)
        if mode == 'I':
            validation_polys = get_input('Enter number of random polynomials to generate to '
                                         'qualify each incremental basis', int, 10)
            sample_polys = get_input('Enter number of random polynomials to generate, '
                                     'from which one will be added to the basis', int, 10)
            number_of_processors = get_input('Enter number of processors to use', int, 6)
            return IncrementalBaseCreation(basis_size, num_variables, degree, validation_polys,
                                           sample_polys, number_of_processors)
        return BaseCreation.get_base_creation_from_user()


@dataclass
class RandomBaseCreation(BaseCreation):
    def create_base(self, prng: Random) -> PolyBase:
        polys = [Poly.gen_random_positive(self.variables, self.half_degree, prng) for _ in range(self.base_size)]
        return PolyBase(polys)


@dataclass
class IncrementalBaseCreation(BaseCreation):
    validation_polys: int
    sample_polys: int
    number_of_processors: int

    @staticmethod
    def run_basis_validation(candidate_index: int, validation_polys_path: str, candidates_polys_path: str,
                             current_polys_path: str) -> float:
        validation_polys = decode_pickle(validation_polys_path)
        candidates_polys = decode_pickle(candidates_polys_path)
        current_polys = decode_pickle(current_polys_path)
        candidate_poly = candidates_polys[candidate_index]
        candidate_basis = PolyBase(current_polys + [candidate_poly])
        errors = [candidate_basis.convex_approximation(candidate_basis.variables, candidate_basis.degree, validation_poly)
                  for validation_poly in validation_polys]
        return mean(errors)

    @staticmethod
    def async_best_poly(validation_polys: List[Poly], candidates_polys: List[Poly], current_polys: List[Poly],
                        pool: multiprocessing.Pool) -> (Poly, float):
        with TemporaryDirectory() as temp_dir:
            validation_polys_path = encode_pickle(os.path.join(temp_dir, 'validation_polys.pickle'), validation_polys)
            candidates_polys_path = encode_pickle(os.path.join(temp_dir, 'candidates_polys.pickle'), candidates_polys)
            current_polys_path = encode_pickle(os.path.join(temp_dir, 'current_polys.pickle'), current_polys)
            parameters = [[index, validation_polys_path, candidates_polys_path, current_polys_path]
                          for index in range(len(candidates_polys))]
            errors = pool.starmap(IncrementalBaseCreation.run_basis_validation, parameters)
            print(f'Errors: {sorted(errors)}')
            poly_index, error = min_arg_min(errors)
            return candidates_polys[poly_index], error

    def create_base(self, prng: Random) -> PolyBase:
        polys = []
        with multiprocessing.Pool(processes=self.number_of_processors) as pool:
            while len(polys) < self.base_size:
                validation_polys = Poly.gen_random_positive_polys(self.validation_polys, self.variables,
                                                                  self.half_degree, prng)
                candidates_polys = Poly.gen_random_positive_polys(self.sample_polys, self.variables,
                                                                  self.half_degree, prng)

                print(f'----- {len(polys)} -----')
                best_poly, poly_error = IncrementalBaseCreation.async_best_poly(validation_polys, candidates_polys,
                                                                                polys, pool)
                print(f'Adding poly with average error {poly_error} to basis:')
                print(best_poly)
                polys.append(best_poly)
        return PolyBase(polys)
