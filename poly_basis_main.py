from itertools import product
from random import Random

from sympy_utils.poly_basis import PolyBasis
from sympy_utils.sympy_utils import gen_normalized_poly, normalize

time_entry = 'time'
num_variables_entry = 'num_variables'
base_num_polys = 'base_num_polys'
max_deg_entry = 'max_deg'
sum_num_polys_entry = 'sum_num_polys'
error_entry = 'error'


def calc_error(num_variables: int, base_polys: int, double_max_deg: int, sum_polys: int, random: Random, normalized: bool = False):

    basis = PolyBasis.gen_random_basis(num_variables, base_polys, double_max_deg // 2, random) if not normalized \
        else PolyBasis.gen_orthonormal_random_basis(num_variables, base_polys, double_max_deg // 2, random)
    positive_basis = basis.square()
    sum_poly = sum([gen_normalized_poly(basis.variables, basis.max_deg, random) ** 2 for _ in range(sum_polys)])
    normalized_sum_poly = normalize(sum_poly)
    linear_combination, error, error_value = positive_basis.approximate(normalized_sum_poly)
    return error_value


def main():
    random = Random(2)
    num_variables_options = [4]
    base_polys_options = [1, 4, 16, 64]
    double_max_deg_options = [4]
    sum_polys_options = [1, 4, 16, 256, 1024]
    times = list(range(10))
    all_options = product(num_variables_options, base_polys_options, double_max_deg_options, sum_polys_options, times)
    print(f'{time_entry},{num_variables_entry},{base_num_polys},{max_deg_entry},{sum_num_polys_entry},{error_entry}')
    for num_variables, base_polys, double_max_deg, sum_polys, time in all_options:
        try:
            error = calc_error(num_variables, base_polys, double_max_deg, sum_polys, random)
            print(f'{time},{num_variables},{base_polys},{double_max_deg},{sum_polys},{error}')
        except RuntimeError as e:
            print(f'{time},{num_variables},{base_polys},{double_max_deg},{sum_polys},{None}')


if __name__ == '__main__':
    main()
