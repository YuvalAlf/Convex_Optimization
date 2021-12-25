from dataclasses import dataclass
from functools import cached_property, cache
from itertools import chain, starmap
from typing import Dict, List, Iterable

from utils.math_utils import combinations_sum


@dataclass(frozen=True)
class Monom:
    symbol_to_deg: Dict[str, int]

    def __getitem__(self, item: str) -> int:
        return self.symbol_to_deg.get(item, 0)

    def symbols(self):
        return self.symbol_to_deg.keys()

    @cached_property
    def degree(self):
        return sum(self.symbol_to_deg.values())

    def __mul__(self, other: 'Monom') -> 'Monom':
        return Monom({symbol: self[symbol] + other[symbol] for symbol in set(chain(self.symbols(), other.symbols()))})

    def __str__(self):
        def to_str(symbol: str, deg: int) -> str:
            assert deg != 0
            return f'{symbol}' if deg == 1 else f'{symbol}^{deg}'
        return ''.join(starmap(to_str, self.symbol_to_deg.items()))

    # @cache
    def __hash__(self) -> int:
        return hash(tuple(chain(self.symbol_to_deg.items())))

    @staticmethod
    def all_monoms_in_deg(symbols: List[str], deg: int) -> Iterable['Monom']:
        for combination in combinations_sum(number_of_values=len(symbols), desired_sum=deg):
            yield Monom({symbol: exponent for symbol, exponent in zip(symbols, combination) if exponent > 0})

