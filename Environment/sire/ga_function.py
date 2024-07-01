import numpy as np
import random

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.pntx import SinglePointCrossover, TwoPointCrossover
from pymoo.core.mutation import Mutation
from pymoo.operators.crossover.ux import UniformCrossover
from pymoo.optimize import minimize
from pymoo.termination import get_termination

import global_def as gd
import individual_evaluation as ie
import data_management as dm

class MyMultiObjectiveProblem(ElementwiseProblem):

    def __init__(self, n, c):
        self.n = n  # Number of variables
        self.c = c  # Upper value of each variable
        super().__init__(
                        n_var=n,
                        n_obj=3, # Number of objetives
                        n_ieq_constr=0,
                        xl=np.zeros(n),
                        xu=np.full(n, c),
                        vtype=int)

    def _evaluate(self, x, out, *args, **kwargs):

        f1, f2 ,f3 = ie.fitness(x)
        out["F"] = [-f1, f2, f3]

class MyMutUniformInt(Mutation):

    def __init__(self, prob=0.05, prob_var=0.2):
        super().__init__()
        self.prob = prob
        self.prob_var = prob_var

    def _do(self, problem, X, **kwargs):
        for i in range(len(X)):
            if random.random() < self.prob:
                for j in range(problem.n):
                    if random.random() < self.prob_var:
                        X[i][j] = random.randint(0, problem.c)
        return X



def solve_genetic_algorithm(siblings_matrix, school_graph, ngen, psize, cxpb, mutpb, cx_op):

    dm.load_data(siblings_matrix, school_graph)

    problem = MyMultiObjectiveProblem(gd.siblings_number, len(gd.classrooms)-1)

    if cx_op == 'one_point':
        crossover=SinglePointCrossover(prob=cxpb)
    elif cx_op == 'two_point':
        crossover=TwoPointCrossover(prob=cxpb)
    elif cx_op == 'uniform':
        crossover=UniformCrossover(prob=cxpb)

    mutation = MyMutUniformInt(prob=mutpb)
    
    algorithm = NSGA2(
                    pop_size=psize,
                    sampling=IntegerRandomSampling(),
                    mutation=mutation,
                    crossover=crossover
                    )

    termination = get_termination("n_gen", ngen)

    res = minimize(problem,
                algorithm,
                termination,
                save_history=True,
                verbose=False
                )

    all_fitness = []
    pareto_front = []

    for entry in res.history:
        pop = entry.pop
        F = pop.get("F")
        F = [[int(-fit[0]), float(fit[1]), float(fit[2])] for fit in F]
        all_fitness.extend(F)


    all_fitness = list(set(tuple(fit) for fit in all_fitness))
    
    unique_solutions = {}

    for ind, fit in zip(res.X, res.F):
        ind_tuple = tuple(int(i) for i in ind)
        fit_tuple = (int(-fit[0]), float(fit[1]), float(fit[2]))
        if ind_tuple not in unique_solutions:
            unique_solutions[ind_tuple] = fit_tuple

    pareto_front = [(list(ind), fit) for ind, fit in unique_solutions.items()]

    pareto_front = sorted(pareto_front, key=lambda x: (x[1][0], x[1][1]))

    return pareto_front, all_fitness

