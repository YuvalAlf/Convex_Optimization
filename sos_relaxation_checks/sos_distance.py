import sympy as sp
from sympy import Symbol
from sos_tools import SOSProblem, poly_opt_prob

x = Symbol('x')
y = Symbol('y')
x1, y1 = 0.6, 0.3
zero_set = 0.3559027778*x-0.2583498678*x*x*y-0.4912229939+0.09841899725*x*y*y-0.0643004114*y+0.2273478836*x*y-0.06151187328*x*x*y*y+0.9185773077*y*y+0.04165883482*y*y*y+0.1525878906*x*x*x*x+0.04959385098*y*y*y*y-0.4679361979*x*x*x+0.09688120042*x*x*x*y+0.5343967014*x*x
distance = (x - x1)**2 + (y - y1) ** 2

# (1 - x^2 - y^2)
def prob1():
    gamma = Symbol('g')

    a, b, c, d, e, f = sp.symbols('a,b,c,d,e,f')
    poly = a*x**2 + b*y**2 + c*x*y + d*x + e*y + f

    problem = SOSProblem()
    problem.add_sos_constraint(distance - gamma + poly*zero_set, [x, y])
    problem.set_objective('max', problem.sym_to_var(gamma))
    problem.solve()
    print(problem.sym_to_var(gamma).value)


def prob2():
    problem = poly_opt_prob([x, y], distance, [zero_set], None, 5, False)

    solution = problem.solve()
    print(problem.status)
    print(problem.value)
    print(problem.sp)


prob2()

