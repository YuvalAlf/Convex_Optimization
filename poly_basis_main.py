from random import Random

from polynomials.poly import gen_normalized_poly, poly_to_str, normalize
from polynomials.poly_basis import PolyBasis
from utils.sympy_utils import sum_expr


def calc_error(num_variables: int, num_polys: int, double_max_deg: int, poly_sum: int, random: Random):
    basis = PolyBasis.gen_random_basis(num_variables, num_polys, double_max_deg // 2, random)
    positive_basis = basis.square()
    sum_poly = sum_expr([gen_normalized_poly(basis.variables, basis.max_deg, random) ** 2 for _ in range(poly_sum)])
    normalized_sum_poly = normalize(sum_poly)
    linear_combination, error, error_value = positive_basis.approximate(normalized_sum_poly)
    return error_value


def main():
    random = Random(2)
    print(f'num_variables,num_polys,max_deg,time,poly_sum,error')
    for num_variables in [4]:
        for num_polys in [10, 20, 30]: #, 40, 50, 60, 70]:
            for double_max_deg in [4]:
                for poly_sum in map(lambda x: 2**x, range(1, 3)):
                    for time in range(1):
                        error = calc_error(num_variables, num_polys, double_max_deg, poly_sum, random)
                        print(f'{num_variables},{num_polys},{double_max_deg},{time},{poly_sum},{error}')


if __name__ == '__main__':
    main()
