from SumOfSquares import SOSProblem
from sympy import Symbol, symbols

from sos_tools import poly_opt_prob

x = Symbol('x')
y = Symbol('y')
x1, y1 = 0.1, 0.1
# p = 0.46267361114*x-0.567594659557*x*x*y-0.4912229939+0.216226536958*x*y*y-0.8359053482E-1*y+0.384217923284*x*y-0.175684061275*x*x*y*y+0.155239565001E1*y*y+0.915244600995E-1*y*y*y+0.435806274343*x*x*x*x+0.141644997784*y*y*y*y-0.102805582679E1*x*x*x+0.27670239652*x*x*x*y+0.903130425366*x*x
# p = 16.0*x*x*x*x-0.144E2*x*x*x-0.464E1*x*x+8.0*x*x*y*y+0.5796E1*x-0.56E1*x*y*y-0.112350401E1+0.298E1*y*y+y*y*y*y-4.0*x*x*y+0.28E1*x*y-0.49*y
p = x**4+y**4-0.25


distance = (x - x1)**2 + (y - y1) ** 2

g = Symbol('g')

alpha = Symbol('alpha')
beta = Symbol('beta')

a, b, c, d, e, f = symbols('a,b,c,d,e,f')
sos2 = a * x ** 2 + b * y ** 2 + c * x * y + d * x + e * y + f

aa,bb,cc,dd,ee,ff = symbols('aa,bb,cc,dd,ee,ff')
sos3 = aa * x ** 2 + bb * y ** 2 + cc * x * y + dd * x + ee * y + ff

motzkin = 1


q = x**4*y**2+x**2+y**4-3*x**2*y**2+1
# problem.add_sos_constraint(distance - g + alpha * p - beta*(1 - x*x - y*y), [x, y])
problem = SOSProblem()
problem.add_sos_constraint(sos2, [x, y])
# problem.add_sos_constraint(sos3, [x, y])
# problem.add_sos_constraint(distance - g + alpha * p - sos2*(1-x**2-y**2) - sos3*(5-2*x**2-1*y**2), [x, y])
# problem.add_sos_constraint(distance - g + alpha * p - sos2*(1-x**2-y**2) - sos3*(5-2*x**2-1*y**2), [x, y])
problem.add_sos_constraint(distance - g + alpha * p - sos2*(1-x**2-y**2) - sos3*(5-2*x**2-1*y**2), [x, y])
problem.set_objective('max', problem.sym_to_var(g))
problem.solve()
print(problem.status)
print(problem.sym_to_var(g).value)

# g(x) >= 0

problem = poly_opt_prob([x, y], distance, [p], [1 - x*x - y*y], 4, False)

solution = problem.solve()
print(solution)
print(solution.status)
print(solution.value)

problem = poly_opt_prob([x, y], distance, [p], [1 - x*x - y*y], 4, False)

solution = problem.solve()
print(solution)
print(solution.status)
print(solution.value)


problem = poly_opt_prob([x, y], q, None, None, 7, False)

solution = problem.solve()
print(solution)
print(solution.status)
print(solution.value)
