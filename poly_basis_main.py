import os
from random import Random

from symbolic_poly.base_creation import BaseCreation
from utils.csv_writer import CsvWriter
from utils.input_utils import get_input
from utils.os_utils import write_text_file

time_entry = 'time'
num_variables_entry = 'num_variables'
base_num_polys = 'base_num_polys'
max_deg_entry = 'max_deg'
sum_num_polys_entry = 'sum_num_polys'
error_entry = 'error'


def run_main(base_creation: BaseCreation, test_times: int, output_directory: str, prng: Random) -> None:
    stats_csv_path = os.path.join(output_directory, 'stats.csv')
    basis_path = os.path.join(output_directory, 'basis.txt')
    with CsvWriter(stats_csv_path, ['Basis Size', 'Error']) as csv_writer:
        for basis in base_creation.create_base(prng):
            write_text_file(basis_path, basis.encode_text())
            for _ in range(test_times):
                error = basis.calc_error(base_creation.variables, base_creation.degree, prng)
                print(f'|Basis| = {len(basis.polys)}  ---> error = {error:0.5f}')
                csv_writer.write_line(len(basis.polys), error)


def main() -> None:
    prng = Random(2)
    output_directory = get_input('Enter output directory path', str, 'results')
    base_creation = BaseCreation.get_base_creation_from_user()
    test_times = get_input('Enter number of times for the resulted basis to be tested', int, 2)
    run_main(base_creation, test_times, output_directory, prng)


if __name__ == '__main__':
    main()
