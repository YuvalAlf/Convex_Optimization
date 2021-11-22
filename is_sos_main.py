import sympy as sp
from sympy import Poly

from polynomials.is_sos import is_sos


def poly1() -> Poly:
    x, y = sp.symbols('x y')
    return x**2 - x*y + 2*y**2


def poly2() -> Poly:
    x, y = sp.symbols('x y')
    return x**2 - 3*x*y + y**2


def poly3() -> Poly:
    x, y = sp.symbols('x y')
    return 2*x**4 + 2*x**3*y - x**2*y**2 + 5*y**4


def hilbert_poly() -> Poly:
    q1, q2, q3, q4 = sp.symbols('q1:5')
    return q1*q1*q2*q2 + q1*q1*q3*q3 + q2*q2*q3*q3 + q4*q4*q4*q4 - 4*q1*q2*q3*q4


def main():
    is_sos(poly1(), debug=True)
    is_sos(poly2(), debug=True)
    is_sos(poly3(), debug=True)
    is_sos(hilbert_poly(), debug=True)


if __name__ == '__main__':
    main()
