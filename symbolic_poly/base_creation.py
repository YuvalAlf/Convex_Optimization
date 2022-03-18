from __future__ import annotations

import multiprocessing
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import Random
from statistics import mean
from tempfile import TemporaryDirectory
from typing import List, Optional

from symbolic_poly.poly import Poly
from symbolic_poly.poly_base import PolyBase
from utils.functional_utils import cached_property
from utils.input_utils import get_input
from utils.iterable_utils import min_arg_min, generate, min_by, max_by
from utils.os_utils import encode_pickle, decode_pickle, write_text_file, join_create_dir


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
    def create_base(self, prng: Random, output_directory: Optional[str] = None) -> PolyBase:
        pass

    @staticmethod
    def get_base_creation_from_user() -> BaseCreation:
        basis_size = get_input('Enter basis size', int, 10)
        num_variables = get_input('Enter number of variables', int, 2)
        degree = get_input('Enter basis degree', int, 4)
        mode = get_input('Enter R for random basis and I for incremental basis, F for farthest basis and A'
                         'for best approximated basis', str, 'R')
        if mode == 'R':
            return RandomBaseCreation(basis_size, num_variables, degree)
        if mode == 'F':
            candidates = get_input('Enter number of candidate polynomials', int, 10)
            return FarthestBaseCreation(basis_size, num_variables, degree, candidates)
        if mode == 'A':
            candidates = get_input('Enter number of candidate polynomials', int, 10)
            return BestApproximationBaseCreation(basis_size, num_variables, degree, candidates)
        if mode == 'I':
            candidates = get_input('Enter number of candidate polynomials', int, 10)
            validations = get_input('Enter number of validation polynomials', int, 10)
            processors = get_input('Enter number of processors to use', int, 5)
            return IncrementalBaseCreation(basis_size, num_variables, degree, validations, candidates, processors)
        raise ValueError(f'Mode {mode} not valid')


@dataclass
class RandomBaseCreation(BaseCreation):
    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'random-basis_seed={random_seed}')

    def create_base(self, prng: Random, output_directory: Optional[str] = None) -> PolyBase:
        polys = [Poly.gen_random_positive(self.variables, self.half_degree, prng) for _ in range(self.base_size)]
        basis = PolyBase(polys)
        if output_directory is not None:
            write_text_file(os.path.join(output_directory, 'basis.txt'), basis.encode_text())
        return basis


@dataclass
class FarthestBaseCreation(BaseCreation):
    num_candidates: int

    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'farthest-basis_candidates={self.num_candidates}_seed={random_seed}')

    def create_base(self, prng: Random, output_directory: Optional[str] = None) -> PolyBase:
        basis = PolyBase([Poly.gen_random_positive(self.variables, self.half_degree, prng)])
        while len(basis.polys) < self.base_size:
            candidates_polys = generate(self.num_candidates,
                                        lambda: Poly.gen_random_positive(self.variables, self.half_degree, prng))
            best_poly = max_by(basis.min_distance_to, candidates_polys)
            basis = basis.add_poly(best_poly)
        if output_directory is not None:
            write_text_file(os.path.join(output_directory, 'basis.txt'), basis.encode_text())
        return basis


@dataclass
class BestApproximationBaseCreation(BaseCreation):
    num_candidates: int

    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'best-approx_candidates={self.num_candidates}_seed={random_seed}')

    def create_base(self, prng: Random, output_directory: Optional[str] = None) -> PolyBase:
        basis = PolyBase([Poly.gen_random_positive(self.variables, self.half_degree, prng)])
        while len(basis.polys) < self.base_size:
            candidates_polys = generate(self.num_candidates,
                                        lambda:Poly.gen_random_positive(self.variables, self.half_degree, prng))
            best_poly = min_by(basis.convex_approximation, candidates_polys)
            basis = basis.add_poly(best_poly)
        if output_directory is not None:
            write_text_file(os.path.join(output_directory, 'basis.txt'), basis.encode_text())
        return basis


@dataclass
class IncrementalBaseCreation(BaseCreation):
    validation_polys: int
    candidate_polys: int
    number_of_processors: int

    def create_directory(self, output_directory: str, random_seed: int) -> str:
        return join_create_dir(output_directory, f'incremental-basis_candidates={self.candidate_polys}'
                                                 f'_validations={self.validation_polys}_seed={random_seed}')

    @staticmethod
    def run_basis_validation(candidate_index: int, validation_polys_path: str, candidates_polys_path: str,
                             current_polys_path: str) -> float:
        validation_polys = decode_pickle(validation_polys_path)
        candidates_polys = decode_pickle(candidates_polys_path)
        current_polys = decode_pickle(current_polys_path)
        candidate_poly = candidates_polys[candidate_index]
        candidate_basis = PolyBase(current_polys + [candidate_poly])
        errors = [candidate_basis.convex_approximation(validation_poly) for validation_poly in validation_polys]
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
            print(f'Errors: {mean(errors)}')
            poly_index, error = min_arg_min(errors)
            return candidates_polys[poly_index], error

    def create_base(self, prng: Random, output_path: Optional[str] = None) -> PolyBase:
        raise NotImplementedError()
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
                write_text_file(output_path, PolyBase(polys).encode_text())
        return PolyBase(polys)
