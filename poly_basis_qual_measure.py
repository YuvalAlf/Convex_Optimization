from random import Random

from symbolic_poly.poly_base import PolyBase
from utils.csv_writer import CsvWriter
from utils.input_utils import get_input


def run_poly_basis_quality_measurement(basis: PolyBase, num_tests: int, num_processors: int, output_path: str,
                                       prng: Random) -> None:
    with CsvWriter(output_path, ['index', 'error']) as csv_writer:
        for index in range(1, num_tests + 1):
            error = basis.calc_error(basis.variables, basis.degree, prng)
            print(f'{index}) error = {error:.8f}')
            csv_writer.write_line(index, error)


def main() -> None:
    output_path = get_input('Enter output path', str, 'basis_quality.csv')
    prng = Random(get_input('Enter random seed', int, 1))
    input_poly = PolyBase.decode_text(get_input('Enter input basis path', str, 'basis.txt'))
    num_tests = get_input('Enter number of random tests to perform', int, 10)
    num_processors = get_input('Enter number of processors to use', int, 1)
    run_poly_basis_quality_measurement(input_poly, num_tests, num_processors, output_path, prng)


if __name__ == '__main__':
    main()
