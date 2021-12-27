from itertools import product
from random import Random, shuffle
from statistics import mean
from typing import List, Iterable, Tuple

from symbolic_poly.poly import Poly
from utils.iterable_utils import generate

time_entry = 'time'
num_variables_entry = 'num_variables'
base_num_polys = 'base_num_polys'
max_deg_entry = 'max_deg'
sum_num_polys_entry = 'sum_num_polys'
error_entry = 'error'


def calc_error(num_variables: int, base_polys: int, max_deg: int, sum_polys: int, random: Random) -> float:
    half_deg = max_deg // 2
    variables = [f'x{num}' for num in range(1, num_variables + 1)]
    positive_basis = list(generate(base_polys,
                                   lambda: Poly.gen_random(variables, half_deg, random).square().normalize()))
    sum_poly = sum(generate(sum_polys, lambda: Poly.gen_random(variables, half_deg, random).square().normalize()),
                   Poly.zero()).normalize()
    linear_combination, error, error_value = Poly.convex_approximation(variables, max_deg, positive_basis, sum_poly)
    # for combination, pol in linear_combination:
    #     print(f'{combination} * ({pol}) +')
    # print(f'  + {error}')
    # print(f'   = {sum_poly}')
    return error_value


def calc_error_danny_alg(num_variables: int, max_base_poly: int, max_deg: int, sum_polys: int, random: Random) -> Iterable[Tuple[int, float]]:
    half_deg = max_deg // 2
    variables = [f'x{num}' for num in range(1, num_variables + 1)]
    positive_basis = list(generate(10000,
                                   lambda: Poly.gen_random(variables, half_deg, random).square().normalize()))
    basis = []

    def measure_basis(candidate_basis: List[Poly]) -> float:
        values = []
        for _ in range(10):
            poly = Poly.gen_random(variables, half_deg, random).square().normalize()
            linear_combination, error, error_value = Poly.convex_approximation(variables, max_deg, candidate_basis,
                                                                               poly)
            values.append(error_value)
        return mean(values)

    for _ in range(max_base_poly):
        shuffle(positive_basis)
        best_candidate = min(positive_basis[:10], key=lambda candidate: measure_basis(basis + [candidate]))
        basis.append(best_candidate)
        positive_basis.remove(best_candidate)
        yield len(basis), measure_basis(basis)


def main():
    random = Random(2)
    num_variables_options = [2]
    base_polys_options = list(range(1, 201))
    max_degs_options = [4]
    sum_polys_options = [1]
    times = list(range(10))
    all_options = product(num_variables_options, base_polys_options, max_degs_options, sum_polys_options, times)
    print(f'{time_entry},{num_variables_entry},{base_num_polys},{max_deg_entry},{sum_num_polys_entry},{error_entry}')
    for num_variables, base_polys, double_max_deg, sum_polys, time in all_options:
        error = calc_error(num_variables, base_polys, double_max_deg, sum_polys, random)
        print(f'{time},{num_variables},{base_polys},{double_max_deg},{sum_polys},{error}')


def main_danny():
    random = Random(2)
    num_variables_options = [2]
    base_polys_options = list(range(1, 201)) #[int(1.5**i) for i in range(20)]
    max_degs_options = [4]
    sum_polys_options = [1]
    times = list(range(10))
    all_options = product(num_variables_options, base_polys_options, max_degs_options, sum_polys_options, times)
    print(f'{time_entry},{num_variables_entry},{base_num_polys},{max_deg_entry},{sum_num_polys_entry},{error_entry}')
    # for num_variables, base_polys, double_max_deg, sum_polys, time in all_options:
    for num_basis, error in calc_error_danny_alg(2, 2217, 4, 1, random):
        print(f'{0},{2},{num_basis},{4},{1},{error}')


if __name__ == '__main__':
    main()
    # main_danny()
