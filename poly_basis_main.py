from random import Random

from symbolic_poly.base_creation import BaseCreation
from utils.csv_writer import CsvWriter
from utils.input_utils import get_input

time_entry = 'time'
num_variables_entry = 'num_variables'
base_num_polys = 'base_num_polys'
max_deg_entry = 'max_deg'
sum_num_polys_entry = 'sum_num_polys'
error_entry = 'error'


def run_main(base_creation: BaseCreation, output_csv_path: str, prng: Random) -> None:
    with CsvWriter(output_csv_path, ['Basis Size', 'Error']) as csv_writer:
        for basis in base_creation.create_base(prng):
            for _ in range(10):
                error = basis.calc_error(base_creation.variables, base_creation.degree, prng)
                print(f'|Basis| = {len(basis.polys)}  ---> error = {error:0.5f}')
                csv_writer.write_line(len(basis.polys), error)


def main() -> None:
    prng = Random(2)
    output_csv_path = get_input('Enter output CSV path', str, 'results.csv')
    base_creation = BaseCreation.get_base_creation_from_user()
    run_main(base_creation, output_csv_path, prng)


if __name__ == '__main__':
    main()
