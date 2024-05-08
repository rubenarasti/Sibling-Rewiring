import random
import os

import matplotlib.pyplot as plt

from deap import base
from deap import creator
from deap import algorithms

from deap import tools
import numpy as np
import pandas as pd
import networkx as nx

import global_def as gd
import data_management as dm
import individual_evaluation as eval

toolbox = base.Toolbox()
logbook = tools.Logbook()


def configure_solution():
    # Minimize the 2 objetives
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    # We create the values ​​that the individual's attributes can take
    toolbox.register("attr_int", random.randint, 0, len(gd.classroom)-1)

    # We create the attribute array of the individual with length equal to the number of siblings
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, gd.siblings_number)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", eval.fitness)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)
    toolbox.register("select", tools.selSPEA2)
#    toolbox.register("select", tools.selNSGA2)   
    
    return toolbox
 
def configure_param():
    
    params = {}
    
    params['NGEN'] = 10
    params['PSIZE'] = 50
    params['CXPB'] = 0.75
    params['MUTPB'] = 0.2
    
    return params

def solve_genetic_algorithm(df,G,percentage_component):
    
    dm.load_data(df, G, percentage_component)
    
    toolbox = base.Toolbox()

    toolbox = configure_solution()
    params = configure_param()

    population = toolbox.population(n=50)

    stats = tools.Statistics(lambda ind: ind.fitness.values) 
    stats.register("avg", np.mean) 
    stats.register("std", np.std) 
    population, logbook = algorithms.eaSimple(population, toolbox, 
	                               cxpb=params['CXPB'], mutpb=params['MUTPB'], 
	                               ngen=params['NGEN'], verbose=False, stats=stats
                                   )
        
    best = eval.fitness(tools.selBest(population,1)[0])
    print(logbook)

    print("mejor individuo",tools.selBest(population,1)[0])
    
    print("fitness mejor individuo",eval.fitness(tools.selBest(population,1)[0]))
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    print("fitness frente de pareto")
    for ind in pareto_front:
        print(eval.fitness(ind))
    
    graph = eval.fenotype(tools.selBest(population,1)[0])

    return best, graph, pareto_front

"""
"""  
if __name__ == "__main__":
    
    df = pd.read_csv("../uploads/siblings.csv")
    G = nx.read_gexf("../uploads/school_net.gexf")

    solve_genetic_algorithm(df, G, 50)
    """
    toolbox = base.Toolbox()

    toolbox = configure_solution()
    params = configure_param()

    population = toolbox.population(n=50)

    stats = tools.Statistics(lambda ind: ind.fitness.values) 
    stats.register("avg", np.mean) 
    stats.register("std", np.std) 
    population, logbook = algorithms.eaSimple(population, toolbox, 
	                               cxpb=params['CXPB'], mutpb=params['MUTPB'], 
	                               ngen=params['NGEN'], verbose=False, stats=stats
                                   )
    

    print(logbook)

    print(tools.selBest(population,1)[0])
    
    print(eval.fitness(tools.selBest(population,1)[0]))

    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    for ind in pareto_front:
        print(eval.fitness(ind))
    
    resultado=eval.fenotype(tools.selBest(population,1)[0])

    """
  
