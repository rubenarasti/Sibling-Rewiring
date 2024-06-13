import random
import time

from deap import base
from deap import creator
from deap import algorithms

from deap import tools

import global_def as gd
import data_management as dm
import individual_evaluation as eval

toolbox = base.Toolbox()

def configure_solution(crossover_operator):
    # Maximize the first objetive and minimize the 2 other objetives
    creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, -1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    # Create the values ​​that the individual's attributes can take
    toolbox.register("attr_int", random.randint, 0, len(gd.classrooms)-1)

    # Create the attribute array of the individual with length equal to the number of siblings
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, gd.siblings_number)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", eval.fitness)

    if crossover_operator == 'one_point':
        toolbox.register("mate", tools.cxOnePoint)
    elif crossover_operator == 'two_point':
        toolbox.register("mate", tools.cxTwoPoint)
    elif crossover_operator == 'uniform':
        toolbox.register("mate", tools.cxUniform, indpb=0.5)

    toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(gd.classrooms)-1, indpb=0.2)
    toolbox.register("select", tools.selNSGA2)   
    
    return toolbox
 

def solve_genetic_algorithm(siblings_matrix, school_graph, ngen, psize, cxpb, mutpb, cx_op):

    dm.load_data(siblings_matrix, school_graph)
    
    toolbox = base.Toolbox()

    toolbox = configure_solution(cx_op)

    population = toolbox.population(n=psize)
    
    unique_fitnesses = set()
    
    fits = toolbox.map(toolbox.evaluate, population)
    for fit, ind in zip(fits, population):
        ind.fitness.values = fit
        unique_fitnesses.add(fit)

    for gen in range(ngen):
        offspring = algorithms.varOr(population, 
                                     toolbox, 
                                     lambda_=psize, 
                                     cxpb=cxpb, 
                                     mutpb=mutpb)
        
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        for ind in offspring:
            unique_fitnesses.add(ind.fitness.values)
        population = toolbox.select(offspring + population, k=psize)


    non_dominated = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    pareto_front = [] # list to store non_duplicate individuals and their fitnesses

    for ind in non_dominated:
        fitness = ind.fitness.values
        if (ind,fitness) not in pareto_front:
             pareto_front.append((ind,fitness))

    return pareto_front, unique_fitnesses


