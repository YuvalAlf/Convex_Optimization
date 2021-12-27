from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property, cache
from itertools import chain, starmap
from typing import Dict, List, Iterable

from utils.core_utils import not_equal, snd
from utils.iterable_utils import filter_by
from utils.math_utils import combinations_sum


class Monom:
    def __init__(self, symbol_to_deg: Dict[str, int]):
        self.symbol_to_deg = {var: deg for var, deg in symbol_to_deg.items() if deg > 0}

    def __getitem__(self, item: str) -> int:
        return self.symbol_to_deg.get(item, 0)

    def symbols(self):
        return self.symbol_to_deg.keys()

    @cached_property
    def degree(self):
        return sum(self.symbol_to_deg.values())

    def __mul__(self, other: Monom) -> Monom:
        return Monom({symbol: self[symbol] + other[symbol] for symbol in set(chain(self.symbols(), other.symbols()))})

    def __str__(self):
        def to_str(symbol: str, deg: int) -> str:
            assert deg != 0
            if deg == 1:
                return f'{symbol}'
            return f'{symbol}^{deg}'
        return ''.join(starmap(to_str, self.symbol_to_deg.items()))

    # noinspection PyTypeChecker
    @cached_property
    def hash_value(self):
        return hash(tuple(sorted(chain(self.symbol_to_deg.items()))))

    def __eq__(self, other: Monom):
        return self.symbol_to_deg.__eq__(other.symbol_to_deg)

    def __hash__(self) -> int:
        return self.hash_value

    @staticmethod
    def all_monoms_in_deg(symbols: List[str], deg: int) -> Iterable[Monom]:
        for combination in combinations_sum(number_of_values=len(symbols), desired_sum=deg):
            yield Monom({symbol: exponent for symbol, exponent in zip(symbols, combination) if exponent > 0})

