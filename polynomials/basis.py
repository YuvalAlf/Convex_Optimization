from dataclasses import dataclass
from typing import List

from sympy import Poly


@dataclass
class Basis:
    polys: List[Poly]


