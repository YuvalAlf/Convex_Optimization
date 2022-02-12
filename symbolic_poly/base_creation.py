from __future__ import annotations

import multiprocessing
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from itertools import product
from random import Random
from statistics import median
from tempfile import TemporaryDirectory
from typing import List, Iterable

from symbolic_poly.poly import Poly
from symbolic_poly.poly_base import PolyBase
from utils.core_utils import fst, snd
from utils.input_utils import get_input
from utils.iterable_utils import generate, min_by
from utils.os_utils import decode_json, encode_json


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
        degree = get_input('Enter basis degree', int, 6)
        mode = get_input('Enter R for random basis and I for incremental basis', str, 'R')
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

    @cached_property
    def process_pool(self) -> multiprocessing.Pool:
        return multiprocessing.Pool(processes=self.number_of_processors)

    @staticmethod
    def async_median_error(candidates_base_path: str, validation_polys_path: str, variables_path: str) -> float:
        candidates_base = decode_json(candidates_base_path)
        validation_polys = decode_json(validation_polys_path)
        variables = decode_json(variables_path)
        return PolyBase.calc_median_error(candidates_base, validation_polys, variables)

    def create_base(self, prng: Random) -> PolyBase:
        polys = []
        while len(polys) < self.base_size:
            with TemporaryDirectory() as temp_dir:
                validation_polys = list(generate(self.validation_polys, lambda: Poly.gen_random(self.variables, self.half_degree, prng).square().normalize()))
                candidates_polys = list(generate(self.sample_polys, lambda: Poly.gen_random(self.variables, self.half_degree, prng).square().normalize()))
                candidate_bases = [PolyBase(polys + [candidates_poly]) for candidates_poly in candidates_polys]
                # arguments = list(product(candidate_bases, [validation_polys], [self.variables]))
                #
                # encode_json(candidate_bases, os.pathl)
                # encode_json()

                # encode_json(temp_dir, o)
                # for i, candidate_base in enumerate(candidate_bases):
                #     encode_json()
                #     self.process_pool.apply_async(IncrementalBaseCreation.async_median_error,)
                errors = [PolyBase.calc_median_error(candidate_base, validation_polys, self.variables)
                          for candidate_base in candidate_bases]
                best_poly = min_by(fst, zip(errors, candidates_polys), snd)

                polys.append(best_poly)
                yield PolyBase(polys)
