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
    toolbox.register("attr_int", random.randint, 0, len(gd.classrooms)-1)

    # We create the attribute array of the individual with length equal to the number of siblings
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, gd.siblings_number)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", eval.fitness)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.9)
#    toolbox.register("select", tools.selSPEA2)
    toolbox.register("select", tools.selNSGA2)   
    
    return toolbox
 
def configure_param():
    
    params = {}
    
    params['NGEN'] = 1000
    params['PSIZE'] = 100
    params['CXPB'] = 0.5
    params['MUTPB'] = 0.5
    
    return params

def solve_genetic_algorithm(df,G):
    
    dm.load_data(df, G)
    
    toolbox = base.Toolbox()

    toolbox = configure_solution()
    params = configure_param()

    population = toolbox.population(n=params['PSIZE'])
    pareto_front = []
    population, logbook = algorithms.eaMuPlusLambda(
                                population,
                                toolbox,
                                mu = params['PSIZE'],
                                lambda_ = 20,
                                cxpb = params['CXPB'],
                                mutpb = params['MUTPB'],
                                ngen = params['NGEN'],
                                verbose=False
                            )

    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0] 

    """
        i=0
    for p in population:
        print(i)
        i+=1
        print(eval.fitness(p))
    population, logbook = algorithms.eaSimple(population, toolbox, 
                                    cxpb=params['CXPB'], mutpb=params['MUTPB'], 
                                    ngen=params["NGEN"], verbose=False, stats=stats
                                    )
    new_front = tools.sortNondominated(population, len(population), first_front_only=False)[0]
        for ind in new_front:
            pareto_front.append(ind)
    for ind in population:
        print(eval.fitness(ind))
    best = eval.fitness(tools.selBest(population,1)[0])

    
    print(logbook)
    print("mejor individuo",tools.selBest(population,1)[0])
    
    print("fitness mejor individuo",eval.fitness(tools.selBest(population,1)[0]))
    
    print("fitness frente de pareto")
    for ind in pareto_front:
        print(eval.fitness(ind))
    
    graph = eval.fenotype(tools.selBest(population,1)[0])
    """
    #print(pareto_front)
    return pareto_front

def plot_pareto_front(pareto_front):

    pareto_fitness = [eval.fitness(ind) for ind in pareto_front]

    fig, ax = plt.subplots()

    pareto_fitness = np.array(pareto_fitness)

    ax.scatter(pareto_fitness[:, 0], pareto_fitness[:, 1], c='b', label='Frente de Pareto')

    ax.set_xlabel('Número de componentes')
    ax.set_ylabel('Variación del tamaño de los componentes')
    ax.set_title('Frente de Pareto')
    ax.legend()

    plt.show()



"""
"""  
if __name__ == "__main__":
    
    df = pd.read_csv("../uploads/siblings.csv")
    G = nx.read_gexf("../uploads/school_net.gexf")

    pareto_front = solve_genetic_algorithm(df, G)
    plot_pareto_front(pareto_front)
    """
    

    """
  
