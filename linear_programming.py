import cvxpy as cp
import numpy as np


def main(solver: str):
    x = cp.Variable()
    y = cp.Variable()
    constraint1 = y <= x + 2
    constraint2 = y >= -2*x - 3
    constraint3 = y <= 3*x - 1
    objective = cp.Minimize(cp.square(x) + cp.square(y))
    problem = cp.Problem(objective, [constraint1, constraint2, constraint3])
    result = problem.solve(solver, verbose=True)
    print(f'{result=}')
    print(f'{problem.status=}')
    print(f'{problem.value=}')
    print(f'{problem.solution=}')
    print(f'{problem.solver_stats=}')
    print(f'{x.value=}')
    print(f'{y.value=}')
    raw_data = problem.get_problem_data(solver)
    print(raw_data)


if __name__ == '__main__':
    main(cp.CVXOPT)
