from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from math import sqrt
from random import Random
from typing import List, Dict

from symbolic_poly.monom import Monom


@dataclass(frozen=True)
class Poly:
    monom_to_coeff: Dict[Monom, float]

    @staticmethod
    def zero() -> Poly:
        return Poly(dict())

    def __getitem__(self, monom: Monom):
        return self.monom_to_coeff.get(monom, 0)

    @cached_property
    def monoms(self) -> List[Monom]:
        return list(self.monom_to_coeff.keys())

    def __add__(self, other: Poly) -> Poly:
        return Poly({monom: self[monom] + other[monom] for monom in set(chain(self.monoms, other.monoms))})

    def __neg__(self):
        return Poly({monom: -coeff for monom, coeff in self.monom_to_coeff.items()})

    def __sub__(self, other: Poly) -> Poly:
        return self.__add__(other.__neg__())

    def __mul__(self, other: Poly) -> Poly:
        monoms_to_coeffs = defaultdict(float)
        for monom1, coeff1 in self.monom_to_coeff.items():
            for monom2, coeff2 in other.monom_to_coeff.items():
                monoms_to_coeffs[monom1 * monom2] += coeff1 * coeff2
        return Poly(dict(monoms_to_coeffs))

    def __str__(self) -> str:
        monoms_sorted = sorted(self.monoms, key=lambda monom: (monom.degree, sorted(monom.variables)))

        def mul_monom_str(monom: Monom) -> str:
            return f'*{monom}' if monom.degree > 0 else ''

        return ' + '.join((f'{self[monom]:.5f}{mul_monom_str(monom)}' for monom in monoms_sorted))

    def normalize(self) -> Poly:
        normalization_factor = sqrt(sum((coeff ** 2 for coeff in self.monom_to_coeff.values())))
        return Poly({monom: coeff / normalization_factor for monom, coeff in self.monom_to_coeff.items()})

    def square(self) -> Poly:
        return self * self

    @staticmethod
    def gen_random(variables: List[str], deg: int, prng: Random) -> Poly:
        monom_to_coeff = dict()
        for monom_deg in range(deg + 1):
            for monom in Monom.all_monoms_in_deg(variables, monom_deg):
                monom_to_coeff[monom] = prng.uniform(-1, 1)
        return Poly(monom_to_coeff)
