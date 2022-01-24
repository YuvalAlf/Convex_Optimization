from itertools import product
from random import Random

from symbolic_poly.poly_base import PolyBase
from utils.csv_writer import CsvWriter

time_entry = 'time'
num_variables_entry = 'num_variables'
base_num_polys = 'base_num_polys'
max_deg_entry = 'max_deg'
sum_num_polys_entry = 'sum_num_polys'
error_entry = 'error'


def main() -> None:
    prng = Random(2)
    num_variables_options = [2]
    base_polys_options = [1, 10, 50, 100, 200, 500, 1000, 2000]
    max_degs_options = [6]
    sum_polys_options = [1, 5, 10, 50, 100]
    times = list(range(10))
    all_options = product(num_variables_options, base_polys_options, max_degs_options, sum_polys_options, times)
    headers = [time_entry, num_variables_entry, base_num_polys, max_deg_entry, sum_num_polys_entry, error_entry]
    with CsvWriter('results/random.csv', headers) as csv_writer:
        for num_variables, base_polys, double_max_deg, sum_polys, time in all_options:
            error = PolyBase.calc_approximation_error(num_variables, base_polys, double_max_deg, sum_polys, prng)
            print(f'Error = {error}')
            if error is not None:
                csv_writer.write_line(time, num_variables, base_polys, double_max_deg, sum_polys, error)


if __name__ == '__main__':
    main()
