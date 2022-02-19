from sympy import Symbol, symbols

from sos_tools import poly_opt_prob, SOSProblem

x = Symbol('x')
y = Symbol('y')
g = Symbol('g')
a = Symbol('a')

p = -0.22148E-1*x+0.15059072E2*y*y*y*y*y*y+0.290864E1*x*y*y-0.98784*x*x*x+0.762552*y-0.39984*x*y+0.28224*x*x-0.345744E1*y*y*y*y-0.52724*y*y+0.7529536E1*x*x*x*x*x*x-0.6453888E1*x*x*x*x*x+0.537824E1*x*y*y*y*y+0.120736E1*y*y*y+0.230496E1*x*x*x*x-0.300454-0.6453888E1*y*y*y*y*y-0.153664E1*y*y*y*x

x1, y1 = 0.2, 0.1


distance = (x - x1)**2 + (y - y1) ** 2
a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14 = symbols('a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14')
sos2 = a1*x*x*x*y+a2*x*x*y*y+a3*x*y*y*y+a4*y*y*y*y+a5*x*x*x+a6*x*x*y+a7*x*y*y+a8*y*y*y+a9*x*x+a10*x*y+a11*y*y+a12*x+a13*y+a14

motzkin = x**4*y**2+x**2*y**4-3*x**2*y**2+1

problem = poly_opt_prob([x, y], distance, [p], [], 3, False)
solution = problem.solve()
print(solution)
print(solution.status)
print(solution.value)
print('-' * 20)

problem = SOSProblem()
problem.add_sos_constraint(sos2, [x, y])
# problem.add_sos_constraint(distance - g + sos2*(1-x**2-y**2), [x, y])
problem.add_sos_constraint(distance - g - a*p - sos2*(1-x**2-y**2), [x, y])
problem.set_objective('max', problem.sym_to_var(g))
problem.solve()
print(problem.status)
print(problem.sym_to_var(g).value)
