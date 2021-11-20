import sympy as sp
from sympy import Expr

from is_sos import is_sos


def poly1() -> Expr:
    x, y = sp.symbols('x y')
    return x**2 - x*y + 2*y**2


def poly2() -> Expr:
    x, y = sp.symbols('x y')
    return x**2 - 3*x*y + y**2


def poly3() -> Expr:
    x, y = sp.symbols('x y')
    a = 2*x**4 + 2*x**3*y - x**2*y**2 + 5*y**4
    return a


def hilbert_poly() -> Expr:
    q1, q2, q3, q4 = sp.symbols('q1:5')
    return q1*q1*q2*q2 + q1*q1*q3*q3 + q2*q2*q3*q3 + q4*q4*q4*q4 - 4*q1*q2*q3*q4


def main():
    is_sos(poly1())
    is_sos(poly2())
    is_sos(poly3())
    is_sos(hilbert_poly())


if __name__ == '__main__':
    main()
