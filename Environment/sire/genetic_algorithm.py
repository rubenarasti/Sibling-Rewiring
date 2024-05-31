import base64
from io import BytesIO
import random
import os
import time

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


def plot_pareto_front2D(pareto_front, all_fitness):
    objective1 = [fit[0] for fit in all_fitness]
    objective2 = [fit[1] for fit in all_fitness]
    objective3 = [fit[2] for fit in all_fitness]

    # Crear una figura con tres subgráficos
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Primer gráfico
    axs[0].scatter(objective1, objective2, c='r', label='Individuos dominados')
    pareto_fitness1 = np.array([(ind[1][0], ind[1][1]) for ind in pareto_front])
    axs[0].scatter(pareto_fitness1[:, 0], pareto_fitness1[:, 1], c='b', label='Frente de Pareto')
    axs[0].set_title('Objetivo 1 (Max) vs Objetivo 2 (Min)')
    axs[0].set_xlabel('Número de componentes')
    axs[0].set_ylabel('Variabilidad del tamaño de componentes')
    axs[0].legend()

    # Segundo gráfico
    axs[1].scatter(objective1, objective3, c='r', label='Individuos dominados')
    pareto_fitness2 = np.array([(ind[1][0], ind[1][2]) for ind in pareto_front])
    axs[1].scatter(pareto_fitness2[:, 0], pareto_fitness2[:, 1], c='b', label='Frente de Pareto')
    axs[1].set_title('Objetivo 1 (Max) vs Objetivo 3 (Min)')
    axs[1].set_xlabel('Número de componentes')
    axs[1].set_ylabel('Variabilidad del número de enlaces')
    axs[1].legend()

    # Tercer gráfico
    axs[2].scatter(objective2, objective3, c='r', label='Individuos dominados')
    pareto_fitness3 = np.array([(ind[1][1], ind[1][2]) for ind in pareto_front])
    axs[2].scatter(pareto_fitness3[:, 0], pareto_fitness3[:, 1], c='b', label='Frente de Pareto')
    axs[2].set_title('Objetivo 2 (Min) vs Objetivo 3 (Min)')
    axs[2].set_xlabel('Variabilidad del tamaño de componentes')
    axs[2].set_ylabel('Variabilidad del número de enlaces')
    axs[2].legend()

    # Ajustar el diseño de la figura
    plt.tight_layout()

    # Guardar la figura en un buffer
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    img_data = 'data:image/png;base64,' + img_str

    plt.close(fig)

    # Devolver la cadena de imagen base64
    return img_data

