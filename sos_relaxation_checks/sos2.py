from sympy import Symbol

from sos_tools import poly_opt_prob

x = Symbol('x')
y = Symbol('y')

p = -0.22148E-1*x+0.15059072E2*y*y*y*y*y*y+0.290864E1*x*y*y-0.98784*x*x*x+0.762552*y-0.39984*x*y+0.28224*x*x-0.345744E1*y*y*y*y-0.52724*y*y+0.7529536E1*x*x*x*x*x*x-0.6453888E1*x*x*x*x*x+0.537824E1*x*y*y*y*y+0.120736E1*y*y*y+0.230496E1*x*x*x*x-0.300454-0.6453888E1*y*y*y*y*y-0.153664E1*y*y*y*x

x1, y1 = 0.5, 0.8


distance = (x - x1)**2 + (y - y1) ** 2
sos2 = 1 - x**2+y**2

motzkin = x**4*y**2+x**2*y**4-3*x**2*y**2+1

problem = poly_opt_prob([x, y], distance, [p], None, 3, False)

solution = problem.solve()
print(solution)
print(solution.status)
print(solution.value)


# g = Symbol('g')
#
# alpha = Symbol('alpha')
# beta = Symbol('beta')
#
# a, b, c, d, e, f = symbols('a,b,c,d,e,f')
# sos2 = a * x ** 2 + b * y ** 2 + c * x * y + d * x + e * y + f
#
# aa,bb,cc,dd,ee,ff = symbols('aa,bb,cc,dd,ee,ff')
# sos3 = aa * x ** 2 + bb * y ** 2 + cc * x * y + dd * x + ee * y + ff
#
# motzkin = 1
#
#
# q = x**4*y**2+x**2+y**4-3*x**2*y**2+1
# # problem.add_sos_constraint(distance - g + alpha * p - beta*(1 - x*x - y*y), [x, y])
# problem = SOSProblem()
# problem.add_sos_constraint(sos2, [x, y])
# # problem.add_sos_constraint(sos3, [x, y])
# # problem.add_sos_constraint(distance - g + alpha * p - sos2*(1-x**2-y**2) - sos3*(5-2*x**2-1*y**2), [x, y])
# # problem.add_sos_constraint(distance - g + alpha * p - sos2*(1-x**2-y**2) - sos3*(5-2*x**2-1*y**2), [x, y])
# problem.add_sos_constraint(distance - g + alpha * p - sos2*(1-x**2-y**2) - sos3*(5-2*x**2-1*y**2), [x, y])
# problem.set_objective('max', problem.sym_to_var(g))
# problem.solve()
# print(problem.status)
# print(problem.sym_to_var(g).value)
