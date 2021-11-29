from random import Random

from scipy.sparse.linalg import ArpackNoConvergence

from polynomials.poly import gen_normalized_poly, poly_to_str, normalize
from polynomials.poly_basis import PolyBasis
from utils.sympy_utils import sum_expr

time_entry = 'time'
num_variables_entry = 'num_variables'
base_num_polys = 'base_num_polys'
max_deg_entry = 'max_deg'
sum_num_polys_entry = 'sum_num_polys'
error_entry = 'error'


def calc_error(num_variables: int, base_polys: int, double_max_deg: int, sum_polys: int, random: Random):
    basis = PolyBasis.gen_random_basis(num_variables, base_polys, double_max_deg // 2, random)
    positive_basis = basis.square()
    sum_poly = sum_expr([gen_normalized_poly(basis.variables, basis.max_deg, random) ** 2 for _ in range(sum_polys)])
    normalized_sum_poly = normalize(sum_poly)
    linear_combination, error, error_value = positive_basis.approximate(normalized_sum_poly)
    return error_value


def main():
    random = Random(2)
    print(f'{time_entry},{num_variables_entry},{base_num_polys},{max_deg_entry},{sum_num_polys_entry},{error_entry}')
    for num_variables in [4]:
        for base_polys in [10, 20, 30, 40, 50]:
            for double_max_deg in [4]:
                for sum_polys in map(lambda x: 2 ** x, range(7, 10)):
                    for time in range(10):
                        try:
                            error = calc_error(num_variables, base_polys, double_max_deg, sum_polys, random)
                            print(f'{time},{num_variables},{base_polys},{double_max_deg},{sum_polys},{error}')
                        except RuntimeError as e:
                            print(f'{time},{num_variables},{base_polys},{double_max_deg},{sum_polys},{None}')


if __name__ == '__main__':
    main()
