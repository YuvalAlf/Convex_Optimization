from itertools import product
from random import Random, shuffle
from statistics import mean
from typing import List, Iterable, Tuple
from utils.csv_writer import CsvWriter
from symbolic_poly.poly import Poly
from utils.iterable_utils import generate
import time
time_entry = 'time'
num_variables_entry = 'num_variables'
base_num_polys = 'base_num_polys'
max_deg_entry = 'max_deg'
sum_num_polys_entry = 'sum_num_polys'
error_entry = 'error'


# def calc_error_danny_alg(num_variables: int, max_base_poly: int, max_deg: int, sum_polys: int, random: Random) -> Iterable[Tuple[int, float]]:
#     half_deg = max_deg // 2
#     variables = [f'x{num}' for num in range(1, num_variables + 1)]
#     positive_basis = list(generate(10000,
#                                    lambda: Poly.gen_random(variables, half_deg, random).square().normalize()))
#     basis = []
#
#     def measure_basis(candidate_basis: List[Poly]) -> float:
#         values = []
#         for _ in range(10):
#             poly = Poly.gen_random(variables, half_deg, random).square().normalize()
#             linear_combination, error, error_value = Poly.convex_approximation(variables, max_deg, candidate_basis,
#                                                                                poly)
#             values.append(error_value)
#         return mean(values)
#
#     for _ in range(max_base_poly):
#         shuffle(positive_basis)
#         best_candidate = min(positive_basis[:10], key=lambda candidate: measure_basis(basis + [candidate]))
#         basis.append(best_candidate)
#         positive_basis.remove(best_candidate)
#         yield len(basis), measure_basis(basis)


def main() -> None:
    prng = Random(2)
    num_variables_options = [2]
    base_polys_options = [1000]
    max_degs_options = [6]
    sum_polys_options = [1]
    times = list(range(5))
    all_options = product(num_variables_options, base_polys_options, max_degs_options, sum_polys_options, times)
    headers = [time_entry, num_variables_entry, base_num_polys, max_deg_entry, sum_num_polys_entry, error_entry]
    with CsvWriter('results/random.csv', headers) as csv_writer:
        for num_variables, base_polys, double_max_deg, sum_polys, time in all_options:
            error = Poly.calc_approximation_error(num_variables, base_polys, double_max_deg, sum_polys, prng)
            print(f'Error = {error}')
            if error is not None:
                csv_writer.write_line(time, num_variables, base_polys, double_max_deg, sum_polys, error)


def main_danny() -> None:
    prng = Random(2)
    num_variables = 3
    max_deg = 6
    headers = [num_variables_entry, base_num_polys, max_deg_entry, error_entry]

    with CsvWriter('results/danny_alg.csv', headers) as csv_writer:
        basis = PolyBasis([])
        for i in range(1000):
            median_error = basis.add_best(prng)
            csv_writer.write_line(num_variables, len(basis), max_deg, median_error)


if __name__ == '__main__':
    main()
