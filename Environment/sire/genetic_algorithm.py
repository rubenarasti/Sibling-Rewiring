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

def configure_solution():
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
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.9)
    toolbox.register("select", tools.selNSGA2)   
    
    return toolbox
 
def configure_param():
    
    params = {}
    
    params['NGEN'] = 200
    params['PSIZE'] = 200
    params['CXPB'] = 0.6
    params['MUTPB'] = 0.05
    
    return params


def solve_genetic_algorithm(df,G):
    
    dm.load_data(df, G)

    #start_time = time.time()
    
    toolbox = base.Toolbox()

    toolbox = configure_solution()
    params = configure_param()

    population = toolbox.population(n=params['PSIZE'])
    
    all_fitness = []
    
    fits = toolbox.map(toolbox.evaluate, population)
    for fit, ind in zip(fits, population):
        ind.fitness.values = fit
        all_fitness.append(fit)

    for gen in range(params['NGEN']):
        offspring = algorithms.varOr(population, 
                                     toolbox, 
                                     lambda_=params['PSIZE'], 
                                     cxpb=params['CXPB'], 
                                     mutpb=params['MUTPB'])
        
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        for ind in offspring:
            all_fitness.append(ind.fitness.values)
        population = toolbox.select(offspring + population, k=params['PSIZE'])


    #end_time = time.time()

    #elapsed_time = end_time - start_time

    non_dominated = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    pareto_front = [] # list to store non_duplicate individuals and their fitnesses

    for ind in non_dominated:
        fitness = ind.fitness.values
        if (ind,fitness) not in pareto_front:
             pareto_front.append((ind,fitness))

    #print("Total time: ", elapsed_time, "s")

    return pareto_front, all_fitness


