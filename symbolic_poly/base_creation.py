from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import Random
from typing import List, Optional, Iterable

from symbolic_poly.poly import Poly
from symbolic_poly.poly_base import PolyBase
from utils.input_utils import get_input
from utils.iterable_utils import max_by, min_by
from utils.metaprogramming_utils import cached_property
from utils.os_utils import join_create_dir, append_line_text_file


@dataclass
class BaseCreation(ABC):
    base_size: int
    num_variables: int
    degree: int
    tests: int

    @cached_property
    def half_degree(self) -> int:
        return self.degree // 2

    @cached_property
    def variables(self) -> List[str]:
        return [f'x{num}' for num in range(1, self.num_variables + 1)]

    def create_basis(self, prng: Random, output_directory: Optional[str] = None) -> PolyBase:
        poly_basis = PolyBase([])
        for poly in self.create_basis_one_by_one(prng, output_directory):
            poly_basis = poly_basis.add_poly(poly)
            if output_directory is not None:
                append_line_text_file(os.path.join(output_directory, 'basis.txt'), poly.encode_text())
                quality = poly_basis.measure_quality(self.tests, prng)
                append_line_text_file(self.quality_measure_csv_path(output_directory), f'{len(poly_basis)},{quality}')

        return poly_basis

    @abstractmethod
    def create_basis_one_by_one(self, prng: Random, output_directory: Optional[str] = None) -> Iterable[Poly]:
        pass

    @abstractmethod
    def create_directory(self, output_directory: str, random_seed: int) -> str:
        pass

    def quality_measure_csv_path(self, directory: str) -> str:
        csv_path = os.path.join(directory, 'quality.csv')
        if not os.path.exists(csv_path):
            append_line_text_file(csv_path, 'Basis Size,Average Error')
        return csv_path

    @staticmethod
    def get_base_creation_from_user() -> BaseCreation:
        basis_size = get_input('Enter basis size', int, 10)
        num_variables = get_input('Enter number of variables', int, 2)
        degree = get_input('Enter basis degree', int, 4)
        tests = get_input('Enter number of tests for quality measure', int, 100)
        mode = get_input('Enter R for random basis and I for incremental basis, F for farthest basis and A '
                         'for best approximated basis', str, 'R')
        if mode == 'R':
            return RandomBaseCreation(basis_size, num_variables, degree, tests)
        num_candidates = get_input('Enter number of candidate polynomials', int, 10)
        if mode == 'F':
            return FarthestBaseCreation(basis_size, num_variables, degree, tests, num_candidates)
        if mode == 'A':
            return BestApproximationBaseCreation(basis_size, num_variables, degree, tests, num_candidates)
        if mode == 'I':
            num_validations = get_input('Enter number of validation polynomials', int, 10)
            return BestBasisBaseCreation(basis_size, num_variables, degree, tests, num_candidates, num_validations)
        raise ValueError(f'Mode {mode} not valid')


@dataclass
class RandomBaseCreation(BaseCreation):
    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'random-basis_seed={random_seed}', override=True)

    def create_basis_one_by_one(self, prng: Random, output_directory: Optional[str] = None) -> Iterable[Poly]:
        for _ in range(self.base_size):
            yield Poly.gen_random_positive(self.variables, self.half_degree, prng)


@dataclass
class IncrementalBaseCreation(BaseCreation):
    num_candidates: int

    @abstractmethod
    def measure_file_name(self) -> str:
        pass

    @abstractmethod
    def choose_best(self, basis: PolyBase, candidates: List[Poly], prng: Random) -> (float, Poly):
        pass

    @abstractmethod
    def initial_basis(self, prng: Random) -> PolyBase:
        pass

    def create_basis_one_by_one(self, prng: Random, output_directory: Optional[str] = None) -> Iterable[Poly]:
        basis = self.initial_basis(prng)
        yield from basis.polys

        while len(basis.polys) < self.base_size:
            candidates = Poly.gen_random_positive_polys(self.num_candidates, self.variables, self.half_degree, prng)
            measure, best_poly = self.choose_best(basis, candidates, prng)
            basis = basis.add_poly(best_poly)
            yield best_poly
            if output_directory is not None:
                append_line_text_file(os.path.join(output_directory, self.measure_file_name()),
                                      f'|Basis| = {len(basis)} --> {measure}')

        return basis


@dataclass
class FarthestBaseCreation(IncrementalBaseCreation):

    def measure_file_name(self) -> str:
        return 'distances.txt'

    def choose_best(self, basis: PolyBase, candidates: List[Poly], prng: Random) -> (float, Poly):
        return max_by(basis.min_distance_to, candidates)

    def initial_basis(self, prng: Random) -> PolyBase:
        return PolyBase([Poly.gen_random_positive(self.variables, self.half_degree, prng)])

    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'farthest-basis_candidates={self.num_candidates}_seed={random_seed}',
                               override=True)


@dataclass
class BestApproximationBaseCreation(IncrementalBaseCreation):

    def measure_file_name(self) -> str:
        return 'best_approximations.txt'

    def choose_best(self, basis: PolyBase, candidates: List[Poly], prng: Random) -> (float, Poly):
        return max_by(basis.convex_approximation, candidates)

    def initial_basis(self, prng: Random) -> PolyBase:
        return PolyBase([Poly.gen_random_positive(self.variables, self.half_degree, prng)])

    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'best-approx_candidates={self.num_candidates}_seed={random_seed}',
                               override=True)


@dataclass
class BestBasisBaseCreation(IncrementalBaseCreation):
    num_validations: int

    def measure_file_name(self) -> str:
        return 'basis_approximation.txt'

    def choose_best(self, basis: PolyBase, candidates: List[Poly], prng: Random) -> (float, Poly):
        validation_polys = Poly.gen_random_positive_polys(self.num_validations, self.variables, self.half_degree, prng)
        return min_by(lambda poly: basis.add_poly(poly).calc_average_error(validation_polys), candidates)

    def initial_basis(self, prng: Random) -> PolyBase:
        return PolyBase([])

    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'best-basis_candidates={self.num_candidates}'
                                                 f'_validations={self.num_validations}_seed={random_seed}',
                               override=True)

