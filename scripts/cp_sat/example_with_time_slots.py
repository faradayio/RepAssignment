"""Motivating example: simple example with time slots

usage:
time pdm run scripts/cp_sat/example_with_time_slots.py
"""

import numpy as np
from loguru import logger
from ortools.sat.python import cp_model

L = 3  # number of leads
R = 5  # number of reps
T = 2  # number of time slots
TIMEOUT_SECONDS = 5000


def main():
    # random data
    np.random.seed(43)
    e = np.random.randint(1, 10, size=(L, R))  # e_ij = expected profit of assigning lead i to rep j
    t = range(T)  # t_k = time slot k
    s = np.random.choice(range(len(t)), size=L)  # t[s[i]] = time slot of lead i
    a = np.random.choice([0, 1], size=(R, T), p=[0.3, 0.7])  # a_jk = availability of rep j at time slot k

    model = cp_model.CpModel()

    logger.info(f"{L=}")
    logger.info(f"{R=}")
    logger.info(f"{T=}")

    logger.info(f"\n{e=}")
    for i in range(L):
        for j in range(R):
            logger.info(f"e[{i}][{j}]={e[i][j]}")

    logger.info(f"{t=}")
    logger.info(f"{s=}")
    for i in range(L):
        logger.info(f"t[s[i]]=t[s[{i}]]=t[{s[i]}]={t[s[i]]}")

    logger.info(f"\n{a=}")
    for j in range(R):
        for k in range(T):
            logger.info(f"a[{j}][{k}]={a[j][k]}")

    # # x_{ij}
    # x = [
    #     [model.NewBoolVar(f"x[{i},{j}]") for j in range(R)] for i in range(L)
    # ]

    # # objective
    # objective_terms = [e[i][j] * x[i][j] for i in range(L) for j in range(R)]
    # model.Maximize(sum(objective_terms))
    # logger.info(f"objective: sum({objective_terms})")

    # # constraint: sum_j x_{ij} = 1
    # for i in range(L):
    #     model.Add(sum(x[i][j] for j in range(R)) == 1)
    #     logger.info(f"constraint sum_j x_ij=1 ({i=}): sum_j x[{i},j] = 1")

    # logger.info("constraints sum_j x_ij=1 added")

    # # constraint: x_{ij} <= A_{ij}
    # for i in range(L):
    #     for j in range(R):
    #         if A[i][j] == 0:
    #             model.Add(x[i][j] == 0)
    #             logger.info(f"constraint x_ij<=A_ij ({i=}, {j=}): x[{i},{j}] = 0")

    # logger.info("constraints x_ij <= A_ij added")

    # # solve
    # solver = cp_model.CpSolver()
    # solver.parameters.max_time_in_seconds = TIMEOUT_SECONDS
    # logger.info(f"starting solver with {L=}, {R=}, {TIMEOUT_SECONDS=}")
    # status = solver.Solve(model)

    # if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    #     logger.info(f"objective value: {solver.ObjectiveValue()=}")
    #     logger.info(f"status: {status=}, {solver.StatusName(status)}")
    #     for i in range(L):
    #         for j in range(R):
    #             if solver.Value(x[i][j]):
    #                 logger.info(f"Lead {i} is assigned to Rep {j}")
    # else:
    #     logger.error("No solution found or time limit reached.")


if __name__ == "__main__":
    main()