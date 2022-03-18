from sympy import Symbol

#
# from sos_tools import poly_opt_prob
#
x = Symbol('x')
y = Symbol('y')
# x1, y1 = 0.1, 0.1
# # p = 0.46267361114*x-0.567594659557*x*x*y-0.4912229939+0.216226536958*x*y*y-0.8359053482E-1*y+0.384217923284*x*y-0.175684061275*x*x*y*y+0.155239565001E1*y*y+0.915244600995E-1*y*y*y+0.435806274343*x*x*x*x+0.141644997784*y*y*y*y-0.102805582679E1*x*x*x+0.27670239652*x*x*x*y+0.903130425366*x*x
# # p = 16.0*x*x*x*x-0.144E2*x*x*x-0.464E1*x*x+8.0*x*x*y*y+0.5796E1*x-0.56E1*x*y*y-0.112350401E1+0.298E1*y*y+y*y*y*y-4.0*x*x*y+0.28E1*x*y-0.49*y
# p = x**4+y**4-0.25
#
#
# distance = (x - x1)**2 + (y - y1) ** 2
#
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
# print(0.848241-0.685224*y+0.1961964E1*y*y-0.73656*y*y*y+0.9801*y*y*y*y+0.431028*x+0.302982*x*y+0.270624*x*y*y+0.51282*x*y*y*y+0.157809E1*x*x-0.494076*x*x*y+0.1704541E1*x*x*y*y+0.387036*x*x*x+0.428386*x*x*x*y+0.683929*x*x*x*x)
print(0.390625+0.76*y+0.1192164E1*y*y+0.800128*y*y*y+0.432964*y*y*y*y-0.6475*x-0.1457388E1*x*y-0.148668E1*x*y*y-0.871192*x*y*y*y+0.450824*x*x+0.863368*x*x*y+0.63038*x*x*y*y-0.151256*x*x*x-0.193304*x*x*x*y+0.21316E-1*x*x*x*x)
# print(-0.1716*x-0.5132*x*y-0.53*x*x*x*y+0.10556E1*x*x*y*y+0.5168*x*x*y-0.76*x*y*y*y-0.6144*x*y*y+0.2184*y+0.6712*y*y+0.4618*x*x+0.2809*x*x*x*x-0.2332*x*x*x+0.5776*y*y*y*y+0.4256*y*y*y+0.1521)
# print(-0.219*x+0.14256E1*x*y+0.11988E1*x*x*x*y+0.15441E1*x*x*y*y-0.23814E1*x*x*y+0.972*x*y*y*y-0.21882E1*x*y*y-0.243*y+0.8361*y*y+0.7549*x*x+0.5476*x*x*x*x-0.10804E1*x*x*x+0.36*y*y*y*y-0.972*y*y*y+0.225E-1)
# print(0.2112*x-0.14948E1*x*y-0.6298*x*x*x*y+0.353E-1*x*x*y*y-0.17962E1*x*x*y+0.5896*x*y*y*y+0.719*x*y*y-0.3104*y+0.8001*y*y+0.586*x*x+0.2209*x*x*x*x+0.6204*x*x*x+0.1936*y*y*y*y+0.8536*y*y*y+0.256E-1)
# print(0.6204*x+0.14646E1*x*y+0.6438*x*x*x*y+0.3129*x*x*y*y+0.1511E1*x*x*y-0.1044E1*x*y*y*y+0.606E-1*x*y*y+0.4606*y-0.3239*y*y+0.7834*x*x+0.2209+0.1369*x*x*x*x+0.4884*x*x*x+0.36*y*y*y*y-0.588*y*y*y)
# print(-0.276E-1*x-0.439*x*y-0.9118*x*x*x*y+0.385E-1*x*x*y*y+0.16112E1*x*x*y+0.18624E1*x*y*y*y+0.7622*x*y*y+0.116E-1*y+0.4E-3+0.457E-1*y*y+0.4949*x*x+0.2209*x*x*x*x-0.6486*x*x*x+0.9216*y*y*y*y-0.5568*y*y*y)
# print(0.3762*x+0.6006*x*y-0.19208E1*x*x*y*y-0.17836E1*x*x*y+0.6468*x*y*y+0.10374E1*y+0.3249+0.19453E1*y*y-0.10083E1*x*x+0.9604*x*x*x*x-0.6468*x*x*x+0.9604*y*y*y*y+0.17836E1*y*y*y)
# print(-0.6806*x+0.1681+0.1842E1*x*y+0.178E1*x*x*x*y-0.3679*x*x*y*y-0.28174E1*x*x*y-0.10324E1*x*y*y*y-0.2298*x*y*y-0.5494*y-0.267E-1*y*y+0.15089E1*x*x+0.1E1*x*x*x*x-0.166E1*x*x*x+0.3364*y*y*y*y+0.7772*y*y*y)
# print(-0.10944E1*x-0.14526E1*x*y+0.9796*x*x*x*y+0.10322E1*x*x*y*y+0.3434*x*x*y+0.5084*x*y*y*y+0.1822*x*y*y+0.4416*y+0.9216-0.7343*y*y-0.11919E1*x*x+0.6241*x*x*x*x+0.9006*x*x*x+0.1681*y*y*y*y-0.1886*y*y*y)
# print(0.1624*x-0.2068*x*y-0.576*x*x*x*y-0.2976*x*x*y*y+0.12624E1*x*x*y+0.4224*x*y*y*y-0.532*x*y*y-0.4592*y+0.9188*y*y-0.2519*x*x+0.36*x*x*x*x-0.348*x*x*x+0.1936*y*y*y*y-0.7216*y*y*y+0.784E-1)
# print(0.364E-1*x-0.3164*x*y-0.7308*x*x*x*y+0.11769E1*x*x*y*y-0.4614*x*x*y-0.87*x*y*y*y+0.6172*x*y*y-0.784E-1*y+0.2184*y*y+0.1345*x*x+0.1764*x*x*x*x+0.1092*x*x*x+0.25*y*y*y*y-0.28*y*y*y+0.196E-1)

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
#
# # g(x) >= 0
#
# problem = poly_opt_prob([x, y], distance, [p], [1 - x*x - y*y], 4, False)
#
# solution = problem.solve()
# print(solution)
# print(solution.status)
# print(solution.value)
#
# problem = poly_opt_prob([x, y], distance, [p], [1 - x*x - y*y], 4, False)
#
# solution = problem.solve()
# print(solution)
# print(solution.status)
# print(solution.value)
#
#
# problem = poly_opt_prob([x, y], q, None, None, 7, False)
#
# solution = problem.solve()
# print(solution)
# print(solution.status)
# print(solution.value)
