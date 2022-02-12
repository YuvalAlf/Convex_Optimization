from typing import Callable

from utils.generic_utils import T


def get_input(str_to_print: str, mapping: Callable[[str], T], default_value: T) -> T:
    while True:
        try:
            result = input(f'{str_to_print} (default = {default_value}): ')
            if len(result) == 0:
                return default_value
            return mapping(result)
        except ValueError as e:
            print(f'Error: {e}')
            print(f'Please enter again: ', end='')

