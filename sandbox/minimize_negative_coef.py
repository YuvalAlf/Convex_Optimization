from sympy import Symbol, symbols

from sos_tools import poly_opt_prob, SOSProblem


# coeffs = symbols('a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14')
# a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14 = coeffs
# poly = a0*x*x*x*x+a1*x*x*x*y+a2*x*x*y*y+a3*x*y*y*y+a4*y*y*y*y+a5*x*x*x+a6*x*x*y+a7*x*y*y+a8*y*y*y+a9*x*x+a10*x*y+a11*y*y+a12*x+a13*y+a14
# norm = a0**2+a1**2+a2**2+a3**2+a4**2+a5**2+a6**2+a7**2+a8**2+a9**2+a10**2+a11**2+a12**2+a13**2+a14**2

x = Symbol('x')
y = Symbol('y')
a1, a2, a3, a4, a5, a6 = symbols('a1,a2,a3,a4,a5,a6')
poly = a1*x*x + a2*x*y + a3*y*y + a4*x + a5*y + a6
norm = a1**2 + a2**2 + a3**2 + a4**2 + a5**2 + a6**2

# g = Symbol('g')

problem = SOSProblem()
constraint = problem.add_sos_constraint(poly, [x, y])
problem.add_constraint(norm == 1)
problem.set_objective('min', problem.sym_to_var(a1))



# constraint = problem.add_sos_constraint(poly, [x, y])
# problem.add_sos_constraint(poly - g*(norm - 1), [x, y])

# PEx = problem.get_pexpect([x, y], 6)
# problem.add_constraint(PEx(norm) == 1)

solution = problem.solve()
print(problem.status)
print(problem.value)
print(solution.value)
print(solution.status)
print(sum(constraint.get_sos_decomp()))
