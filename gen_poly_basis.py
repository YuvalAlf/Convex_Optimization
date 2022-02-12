from random import Random

from symbolic_poly.base_creation import BaseCreation
from utils.input_utils import get_input
from utils.os_utils import write_text_file


def run_base_creation(base_creation: BaseCreation, output_path: str, prng: Random) -> None:
    basis = base_creation.create_base(prng)
    write_text_file(output_path, basis.encode_text())


def main() -> None:
    prng = Random(get_input('Enter random seed', int, 0))
    output_path = get_input('Enter output basis path', str, 'basis.txt')
    base_creation = BaseCreation.get_base_creation_from_user()
    run_base_creation(base_creation, output_path, prng)


if __name__ == '__main__':
    main()
