from typing import Tuple

from symbolic_poly.base_creation import BaseCreation
from utils.argparser_wrapper import ArgParserWrapper
from utils.random_utils import set_seed


def get_input_args() -> Tuple[int, str]:
    return ArgParserWrapper("Generate sos poly basis")\
        .add_arg('random_seed', int)\
        .add_arg('output_directory', str)\
        .parse()


def run_base_creation(random_seed: int, output_directory: str) -> None:
    prng = set_seed(random_seed)
    base_creation = BaseCreation.get_base_creation_from_user()
    result_directory = base_creation.create_directory(output_directory, random_seed)
    basis = base_creation.create_basis(prng, result_directory)
    print('Basis is:')
    print(basis.encode_text())


if __name__ == '__main__':
    run_base_creation(*get_input_args())
