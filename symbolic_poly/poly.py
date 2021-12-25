from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import chain
from math import sqrt
from random import Random
from typing import List, Dict

from symbolic_poly.monom import Monom


@dataclass(frozen=True)
class Poly:
    monom_to_coeff: Dict[Monom, float]

    def __getitem__(self, monom: Monom):
        return self.monom_to_coeff.get(monom, 0)

    def monoms(self):
        return self.monom_to_coeff.keys()

    def __add__(self, other: 'Poly') -> 'Poly':
        return Poly({monom: self[monom] + other[monom] for monom in set(chain(self.monoms(), other.monoms()))})

    def __neg__(self):
        return Poly({monom: -coeff for monom, coeff in self.monom_to_coeff.items()})

    def __sub__(self, other: 'Poly') -> 'Poly':
        return self.__add__(other.__neg__())

    def __mul__(self, other: 'Poly') -> 'Poly':
        monoms_to_coeffs = defaultdict(float)
        for monom1, coeff1 in self.monom_to_coeff.items():
            for monom2, coeff2 in other.monom_to_coeff.items():
                monoms_to_coeffs[monom1 * monom2] += coeff1 * coeff2
        return Poly(dict(monoms_to_coeffs))

    def __str__(self):
        monoms_sorted = sorted(self.monoms(), key=lambda monom:(monom.degree, sorted(monom.symbols())))
        def mul_monom(monom: Monom) -> str:
            return f'*{monom}' if monom.degree > 0 else ''
        return ' + '.join((f'{self[monom]:.5f}{mul_monom(monom)}' for monom in monoms_sorted))

    @cache
    def __hash__(self) -> int:
        return hash(self.monom_to_coeff)

    def normalize(self):
        sum_squared_coeffs = sum((coeff**2 for coeff in self.monom_to_coeff.values()))
        normalization_factor = sqrt(sum_squared_coeffs)
        return Poly({monom: coeff / normalization_factor for monom, coeff in self.monom_to_coeff.items()})

    @staticmethod
    def gen_random(symbols: List[str], deg: int, prng: Random):
        monom_to_coeff = dict()
        for monom_deg in range(deg + 1):
            for monom in Monom.all_monoms_in_deg(symbols, monom_deg):
                monom_to_coeff[monom] = prng.uniform(-1, 1)
        return Poly(monom_to_coeff)

p = Poly.gen_random(['a', 'b'], 2, Random())
print((p * p).normalize())
