from random import Random

from polynomials.poly import gen_normalized_poly, poly_to_str, normalize
from polynomials.poly_basis import PolyBasis


def main():
    random = Random(1)
    basis = PolyBasis.gen_random_basis(num_variables=2, num_polys=6, max_deg=1, random=random)
    positive_basis = basis.square()
    print('Basis:')
    print(f'{basis}')
    print('Squared basis:')
    print(f'{positive_basis}')
    for _ in range(3):
        print('-' * 20)
        poly = normalize(gen_normalized_poly(basis.variables, basis.max_deg, random) ** 2)
        linear_combination, error, error_value = positive_basis.approximate(poly)
        print(poly_to_str(poly) + ' = ')
        for multiplication, poly in linear_combination:
            print(f'\t{multiplication} * ({poly_to_str(poly)}) + ')
        print(f'\t + {poly_to_str(error)}')
        print(f'Error: {error_value:.4f}')


if __name__ == '__main__':
    main()
