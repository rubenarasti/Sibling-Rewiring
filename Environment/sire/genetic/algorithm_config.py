import base64
from io import BytesIO
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
    creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, -1.0))
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
    
    params['NGEN'] = 100
    params['PSIZE'] = 100
    params['CXPB'] = 0.6
    params['MUTPB'] = 0.05
    
    return params

def solve_genetic_algorithm(df,G):
    
    dm.load_data(df, G)
    
    toolbox = base.Toolbox()

    toolbox = configure_solution()
    params = configure_param()

    population = toolbox.population(n=params['PSIZE'])
    #hof = tools.ParetoFront
    hof = tools.ParetoFront()
    all_fitness = []
    pareto_front = []
    for gen in range(params['NGEN']):
        population, logbook = algorithms.eaSimple(population, toolbox, 
                                    cxpb=params['CXPB'], mutpb=params['MUTPB'], 
                                    ngen=1, verbose=False, stats=[], halloffame=hof
                                    )
        print("GEN ", gen)
        for ind in population:
            if eval.fitness(ind)[0]>14:
                print(ind)
            print(eval.fitness(ind))
            all_fitness.append(eval.fitness(ind))
    
    """
    for gen in range(params['NGEN']):
        population, logbook = algorithms.eaMuPlusLambda(
                                population,
                                toolbox,
                                mu = params['PSIZE'],
                                lambda_ = 20,
                                cxpb = params['CXPB'],
                                mutpb = params['MUTPB'],
                                ngen = 1,
                                halloffame=hof,
                                verbose=False
                            )
    
        for ind in population:
            all_fitness.append(eval.fitness(ind))

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
    """
    non_dominated = tools.sortNondominated(population, len(population), first_front_only=True)[0] 

    unique_fitness = set()

    pareto_front = []

    for ind in non_dominated:
        fitness = eval.fitness(ind)
        
        if fitness not in unique_fitness:
            pareto_front.append((ind,fitness))
            unique_fitness.add(fitness)
    print("HOF")
    for ind in hof:
        print(eval.fitness(ind))
    return pareto_front, all_fitness




def plot_pareto_front2D(pareto_front, all_fitness):
    objective1 = [fit[0] for fit in all_fitness]
    objective2 = [fit[1] for fit in all_fitness]
    objective3 = [fit[2] for fit in all_fitness]
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    # Objetivo 1 vs Objetivo 2
    # Objetivo 1 vs Objetivo 2
    

    # Objetivo 1 vs Objetivo 3
    

    # Objetivo 2 vs Objetivo 3
    axs[0].scatter(objective1, objective2, c='r', label='Individuos dominados')
    
    pareto_fitness = np.array([(ind[1][0], ind[1][1]) for ind in pareto_front])
    axs[0].scatter(pareto_fitness[:, 0], pareto_fitness[:, 1], c='b', label='Frente de Pareto')
    axs[0].set_title('Frente de Pareto (Objetivo 1 vs Objetivo 2)')
    axs[0].set_xlabel('Objetivo 1')
    axs[0].set_ylabel('Objetivo 2')
    axs[0].legend()

    # Objetivo 1 vs Objetivo 3
    axs[1].scatter(objective1, objective3, c='r', label='Individuos dominados')
    pareto_fitness = np.array([(ind[1][0], ind[1][2]) for ind in pareto_front])
    axs[1].scatter(pareto_fitness[:, 0], pareto_fitness[:, 1], c='b', label='Frente de Pareto')
    axs[1].set_title('Frente de Pareto (Objetivo 1 vs Objetivo 3)')
    axs[1].set_xlabel('Objetivo 1')
    axs[1].set_ylabel('Objetivo 3')
    axs[1].legend()

    # Objetivo 2 vs Objetivo 3
    axs[2].scatter(objective2, objective3, c='r', label='Individuos dominados')
    pareto_fitness = np.array([(ind[1][1], ind[1][2]) for ind in pareto_front])
    axs[2].scatter(pareto_fitness[:, 0], pareto_fitness[:, 1], c='b', label='Frente de Pareto')
    axs[2].set_title('Frente de Pareto (Objetivo 2 vs Objetivo 3)')
    axs[2].set_xlabel('Objetivo 2')
    axs[2].set_ylabel('Objetivo 3')
    axs[2].legend()

    plt.tight_layout()
    plt.show()

def is_pareto_efficient_simple(costs):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient]<c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self
    return is_efficient

"""
""" 
if __name__ == "__main__":
    
    df = pd.read_csv("../uploads/siblings.csv")
    G = nx.read_gexf("../uploads/school_net.gexf")    
    mat = df.values
    mat1 = [row[1:] for row in mat]
    pareto_front, all_f = solve_genetic_algorithm(mat1, G)
    plot_pareto_front2D(pareto_front, all_f)
 
"""

def plot_pareto_front2D1(pareto_front, all_fitness):
    # Extraer los primeros y terceros valores de las tuplas de pareto_fitness
    pareto_fitness = [(ind[1][0], ind[1][1]) for ind in pareto_front]
    fig, ax = plt.subplots()

    # Convertir all_fitness a un array de numpy y extraer los primeros y terceros valores
    all_fitness = np.array(list(all_fitness))
    all_fitness_2d = all_fitness[:, [0, 1]]

    ax.scatter(all_fitness_2d[:, 0], all_fitness_2d[:, 1], c='r', label='Individuos dominados')

    pareto_fitness = np.array(pareto_fitness)
    ax.scatter(pareto_fitness[:, 0], pareto_fitness[:, 1], c='b', label='Frente de Pareto')

    ax.set_xlabel('Número de componentes')
    ax.set_ylabel('Nuevo Objetivo')  # Cambia esto por el nombre del tercer valor
    ax.set_title('Frente de Pareto')
    ax.legend()

    #plt.show()
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    img_data = 'data:image/png;base64,' + img_str

    plt.close(fig)
    return img_data

def plot_pareto_front2D2(pareto_front, all_fitness):
    # Extraer los primeros y terceros valores de las tuplas de pareto_fitness
    pareto_fitness = [(ind[1][0], ind[1][2]) for ind in pareto_front]
    fig, ax = plt.subplots()

    # Convertir all_fitness a un array de numpy y extraer los primeros y terceros valores
    all_fitness = np.array(list(all_fitness))
    all_fitness_2d = all_fitness[:, [0, 1]]
    
    ax.scatter(all_fitness_2d[:, 0], all_fitness_2d[:, 1], c='r', label='Individuos dominados')

    pareto_fitness = np.array(pareto_fitness)
    ax.scatter(pareto_fitness[:, 0], pareto_fitness[:, 1], c='b', label='Frente de Pareto')

    ax.set_xlabel('Número de componentes')
    ax.set_ylabel('Nuevo Objetivo')  # Cambia esto por el nombre del tercer valor
    ax.set_title('Frente de Pareto')
    ax.legend()

    #plt.show()
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    img_data = 'data:image/png;base64,' + img_str

    plt.close(fig)
    return img_data
"""