"""Demo script using https://developers.google.com/optimization/cp/cp_solver for a rep assignment problem.

usage:
```
time PYTHONPATH=$(pwd) pdm run cp_sat_demo.py
```
"""

import numpy as np
from loguru import logger
from ortools.sat.python import cp_model

N_LEADS = 1_000
N_REPS = 1_000
TIMEOUT_SECONDS = 5000


def main():
    # random data
    np.random.seed(42)
    E = np.random.randint(1, 100, size=(N_LEADS, N_REPS))
    A = np.random.choice([0, 1], size=(N_LEADS, N_REPS), p=[0.3, 0.7])
    D = np.random.randint(10, 1000, size=(N_LEADS, N_REPS))
    M = np.random.randint(200, 500, size=N_REPS)

    model = cp_model.CpModel()

    # x_{ij}
    x = [
        [model.NewBoolVar(f"x[{i},{j}]") for j in range(N_REPS)] for i in range(N_LEADS)
    ]

    # objective
    objective_terms = [E[i][j] * x[i][j] for i in range(N_LEADS) for j in range(N_REPS)]
    model.Maximize(sum(objective_terms))

    # constraint: sum_j x_{ij} = 1
    for i in range(N_LEADS):
        model.Add(sum(x[i][j] for j in range(N_REPS)) == 1)

    logger.info("constraints sum_j x_ij=1 added")

    # constraint: x_{ij} <= A_{ij}
    for i in range(N_LEADS):
        for j in range(N_REPS):
            if A[i][j] == 0:
                model.Add(x[i][j] == 0)

    logger.info("constraints x_ij <= A_ij added")

    # # constraint: sum_i D_{ij} * x_{ij} <= M_j
    # for j in range(N_REPS):
    #     model.Add(sum(D[i][j] * x[i][j] for i in range(N_LEADS)) <= M[j])
    # logger.info(f"constraints sum_i D_ij*x_ij <= M_j added")

    for i in range(N_LEADS):
        for j in range(N_REPS):
            model.Add(D[i][j] * x[i][j] <= M[j])
    logger.info("constraints D_ij*x_ij <= M_j added")

    # solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = TIMEOUT_SECONDS
    logger.info(f"starting solver with {N_LEADS=}, {N_REPS=}, {TIMEOUT_SECONDS=}")
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        logger.info(f"objective value: {solver.ObjectiveValue()=}")
        logger.info(f"status: {status=}, {solver.StatusName(status)}")
        for i in range(N_LEADS):
            for j in range(N_REPS):
                if solver.Value(x[i][j]):
                    logger.info(f"Lead {i} is assigned to Rep {j}")
    else:
        logger.error("No solution found or time limit reached.")


if __name__ == "__main__":
    main()