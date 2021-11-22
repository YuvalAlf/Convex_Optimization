from picos import SolutionFailure
from sympy import Poly

from polynomials.poly import all_symbols, poly_to_str
from sos_tools.SumOfSquares import SOSProblem
from utils.printing_utils import TabPrinter


def is_sos(poly: Poly, debug: bool) -> bool:
    with TabPrinter(debug) as printer:
        printer.regular_print('-' * 25)
        printer.regular_print('Checking whether the following polynomial is SoS:')
        printer.tab_print(poly_to_str(poly))
        try:
            prob = SOSProblem()
            constraint = prob.add_sos_constraint(poly, all_symbols(poly))
            status = prob.solve()
            printer.tab_print(f'*** SoS decomposition status: {status} *** ')
            printer.regular_print('SoS Decomposition:')
            printer.tab_print(poly_to_str(sum(constraint.get_sos_decomp())))
            return True
        except SolutionFailure as e:
            printer.regular_print('SoS decomposition failure:')
            printer.tab_print(f'{e}')
            return False
