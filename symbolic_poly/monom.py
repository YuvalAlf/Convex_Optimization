from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from itertools import chain, starmap
from typing import Dict, List, Iterable

from utils.math_utils import combinations_sum


@dataclass(frozen=True)
class Monom:
    variable_to_deg: Dict[str, int]

    @staticmethod
    def create(variable_to_deg: Dict[str, int]) -> Monom:
        return Monom({var: deg for var, deg in variable_to_deg.items() if deg > 0})

    def __getitem__(self, item: str) -> int:
        return self.variable_to_deg.get(item, 0)

    @cached_property
    def variables(self) -> List[str]:
        return list(self.variable_to_deg.keys())

    @cached_property
    def degree(self) -> int:
        return sum(self.variable_to_deg.values())

    def __mul__(self, other: Monom) -> Monom:
        return Monom.create({variable: self[variable] + other[variable]
                             for variable in set(chain(self.variables, other.variables))})

    def __str__(self) -> str:
        def to_str(variable: str, deg: int) -> str:
            assert deg != 0
            if deg == 1:
                return f'{variable}'
            return f'{variable}^{deg}'
        return ''.join(starmap(to_str, self.variable_to_deg.items()))

    @cached_property
    def hash_value(self) -> int:
        return hash(tuple(sorted(self.variable_to_deg.items())))

    def __eq__(self, other: Monom) -> bool:
        return self.variable_to_deg.__eq__(other.variable_to_deg)

    def __hash__(self) -> int:
        return self.hash_value

    @staticmethod
    def all_monoms_in_deg(variables: List[str], deg: int) -> Iterable[Monom]:
        for combination in combinations_sum(number_of_values=len(variables), desired_sum=deg):
            yield Monom({variable: exponent for variable, exponent in zip(variables, combination) if exponent > 0})
