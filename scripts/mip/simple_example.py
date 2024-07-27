"""Simple example: each rep visits at most one lead per day

usage:
time pdm run scripts/mip/simple_example.py
"""

import numpy as np
from loguru import logger
from ortools.linear_solver import pywraplp

L = 5  # number of leads
R = 7  # number of reps
TIMEOUT_SECONDS = 5000


def main():
    # random data
    np.random.seed(42)
    e = np.random.randint(1, 10, size=(L, R))  # e_ij = expected profit of assigning lead i to rep j

    model = pywraplp.Solver.CreateSolver("SCIP")

    logger.info(f"{L=}")
    logger.info(f"{R=}")

    logger.info(f"\n{e=}")
    for i in range(L):
        for j in range(R):
            logger.info(f"e[{i}][{j}]={e[i][j]}")

    # x_{ij}
    x = [
        [model.BoolVar(f"x[{i},{j}]") for j in range(R)] for i in range(L)
    ]

    # objective
    objective_terms = [e[i][j] * x[i][j] for i in range(L) for j in range(R)]
    model.Maximize(sum(objective_terms))
    logger.info(f"objective: sum({objective_terms})")

    # constraint: sum_j x_{ij} = 1 : every lead is assigned to exactly one rep
    for i in range(L):
        model.Add(sum(x[i][j] for j in range(R)) == 1)
        logger.info(f"constraint sum_j x_ij=1 ({i=}): sum_j x[{i},j] = 1")

    # constraint: sum_i x_{ij} <= 1 : every rep visits at most one lead
    for j in range(R):
        model.Add(sum(x[i][j] for i in range(L)) <= 1)
        logger.info(f"constraint sum_i x_ij<=1 ({j=}): sum_i x[i,{j}] <= 1")

    # solve
    model.set_time_limit(TIMEOUT_SECONDS)
    logger.info(f"starting solver with {L=}, {R=}, {TIMEOUT_SECONDS=}")
    status = model.Solve()

    # result
    if status in [pywraplp.Solver.OPTIMAL]:
        logger.info(f"objective value: {model.Objective().Value()=}")
        logger.info(f"status: {status=} (means optimal)")
        for i in range(L):
            for j in range(R):
                if x[i][j].solution_value():
                    logger.info(f"Lead {i} is assigned to Rep {j}")
    else:
        logger.error("No optimal solution found or time limit reached.")


if __name__ == "__main__":
    main()