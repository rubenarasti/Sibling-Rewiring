import copy
import random
import pymoo

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import global_def as gd

from pymoo.core.problem import ElementwiseProblem
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.crossover.pntx import PointCrossover, SinglePointCrossover
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.visualization.scatter import Scatter
from pymoo.core.mutation import Mutation



class MyMutFlipBit(Mutation):

    def __init__(self, prob=0.1, prob_var=0.9):
        super().__init__()
        self.prob = prob
        self.prob_var = prob_var

    def _do(self, problem, X, **kwargs):
        # Para cada individuo en la población
        for i in range(len(X)):
            # Decidir si este individuo será mutado basado en prob_var
            if random.random() < self.prob_var:
                # Para cada variable del individuo
                for j in range(problem.n):
                    # Decidir si esta variable será mutada basado en prob
                    if random.random() < self.prob:
                        # Mutar la variable
                        X[i][j] = random.randint(0, problem.c)
        return X


def load_data(siblings, graph):

    gd.initial_network = graph
    gd.total_students = len(graph.nodes())
    gd.siblings_number = len(siblings)
    
    for index, row in enumerate(siblings):
        gd.siblings_dict[row[0]] = [index] + [str(item) for item in row[1:4]] + [row[4]]

    dicNombre = {}
    dicEtapa = {}
    dicCurso = {}
    dicClase = {}
    dicEstudiantes = {}
    etapas = nx.get_node_attributes(graph,'Etapa')
    clases = nx.get_node_attributes(graph,'Clase')
    cursos = nx.get_node_attributes(graph,'Curso')

    for node in graph.nodes():
        name = []
        name.append(etapas[node])
        name.append(cursos[node])
        name.append(clases[node])
        node_name = ''.join(str(e) for e in name)
	
        if node_name not in gd.graph_eval_ini.nodes():
            gd.graph_eval_ini.add_node(node_name)
            dicNombre[node_name] = node_name
            dicEtapa[node_name] = etapas[node]
            dicCurso[node_name] = cursos[node]
            dicClase[node_name] = clases[node]
            dicEstudiantes[node_name] = []    
			
    nx.set_node_attributes(gd.graph_eval_ini, dicNombre, 'Nombre')
    nx.set_node_attributes(gd.graph_eval_ini, dicEtapa, 'Etapa')
    nx.set_node_attributes(gd.graph_eval_ini, dicCurso, 'Curso')
    nx.set_node_attributes(gd.graph_eval_ini, dicClase, 'Clase')
    nx.set_node_attributes(gd.graph_eval_ini, dicEstudiantes, 'Estudiantes')



def fitness (individual):
    
    graph_eval = fenotype(individual)
    #print(list(nx.connected_components(graph_eval)))
    components_sizes = []
    components_edges = []
    contag_compo = 0

    for component in nx.connected_components(graph_eval):
        contag_compo += 1
        components_sizes.append(len(component))
        subgraph = graph_eval.subgraph(component)
        total_weight = subgraph.size(weight='weight')
        components_edges.append(total_weight)

    components_sizes_np = np.array(components_sizes)
    comp_size_var = components_sizes_np.var()

    components_edges_np = np.array(components_edges)
    comp_edges_var = components_edges_np.var()

    return -contag_compo, comp_size_var, comp_edges_var

def fenotype (individual):
    graph_eval = copy.deepcopy(gd.graph_eval_ini)
    seen = set() # Set to avoid repeating those already seen
    
    for (classroom1, (sib_name1, sib_data1)) in zip(individual, gd.siblings_dict.items()):

        sib_name2 = sib_data1[4]
        # Order the pair 
        if sib_name2 > sib_name1:
            siblings_pair = (sib_name1, sib_name2)
        else:
            siblings_pair = (sib_name2, sib_name1)

        if siblings_pair in seen:
            continue

        seen.add(siblings_pair)
        
        sibling1 = []
        sibling1.append(sib_data1[1]) # Obtain the stage
        sibling1.append(sib_data1[2]) # Obtain the year
        sibling1.append(gd.classrooms[classroom1])
        sibling1_class = ''.join(str(e) for e in sibling1)
        
        sib_data2 = gd.siblings_dict[sib_name2]
        classroom2 = individual[sib_data2[0]] # Obtain the sibling2 classroom with the index

        sibling2 = []
        sibling2.append(sib_data2[1])
        sibling2.append(sib_data2[2])
        sibling2.append(gd.classrooms[classroom2])
        sibling2_class = ''.join(str(e) for e in sibling2)

        if graph_eval.has_edge(sibling1_class, sibling2_class):
            graph_eval.edges[sibling1_class, sibling2_class]["weight"] += 1
        else:
            graph_eval.add_edge(sibling1_class, sibling2_class)
            graph_eval.edges[sibling1_class, sibling2_class]["weight"] = 1

    return graph_eval


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
        
        f1, f2 ,f3 = fitness(x)
        if f1 < -1:
            print(x)
            print([f1, f2, f3])
        
        out["F"] = [f1, f2, f3]  # Store the 3 objetives

def solve_genetic_algorithm(df,G):
    
    load_data(df, G)
    
    problem = MyMultiObjectiveProblem(gd.siblings_number, len(gd.classrooms)-1)
    
    #crossover=SBX(prob=0.5, eta=1, vtype=float)
    crossover=SinglePointCrossover(prob=0.6)
    #mutation=PM(prob=0.2, eta=1, vtype=float, repair=RoundingRepair())
    #mutation = BitflipMutation(prob=0.5, prob_var=0.9)
    mutation = MyMutFlipBit(prob = 0.05, prob_var=0.9)
    pop = 20000
    algorithm = NSGA2(
                    pop_size=pop,  # Tamaño de la población
                    sampling=IntegerRandomSampling(),
                    mutation=mutation,
                    crossover=crossover
                    )
    
    # Definir el criterio de terminación
    termination = get_termination("n_gen", 10)
    #termination = get_termination("time", "01:00:00")

    res = minimize(problem,
                algorithm,
                termination,
                pf=True,
                save_history=True,
                verbose=True
                )
    
    #Scatter().add(res.F).show()
    hist = res.history

    all_individuals = []
    all_objectives = []

    for entry in hist:
        pop = entry.pop
        X = pop.get("X")
        F = pop.get("F")
        all_individuals.extend(X)
        all_objectives.extend(F)
    
    print(f"Total de individuos: {len(all_individuals)}")

    # Convertir listas a numpy arrays para facilitar el manejo
    import numpy as np
    all_individuals = np.array(all_individuals)
    all_objectives = np.array(all_objectives)

    # Graficar todos los individuos del historial en gráficos 2D
    plt.figure(figsize=(18, 5))

    # Comparar Objetivo 1 vs Objetivo 2
    plt.subplot(1, 3, 1)
    plt.scatter(all_objectives[:, 0], all_objectives[:, 1], s=10, facecolors='none', edgecolors='b')
    plt.title("Objetivo 1 vs Objetivo 2")
    plt.xlabel("Objetivo 1")
    plt.ylabel("Objetivo 2")

    # Comparar Objetivo 1 vs Objetivo 3
    plt.subplot(1, 3, 2)
    plt.scatter(all_objectives[:, 0], all_objectives[:, 2], s=10, facecolors='none', edgecolors='r')
    plt.title("Objetivo 1 vs Objetivo 3")
    plt.xlabel("Objetivo 1")
    plt.ylabel("Objetivo 3")

    # Comparar Objetivo 2 vs Objetivo 3
    plt.subplot(1, 3, 3)
    plt.scatter(all_objectives[:, 1], all_objectives[:, 2], s=10, facecolors='none', edgecolors='g')
    plt.title("Objetivo 2 vs Objetivo 3")
    plt.xlabel("Objetivo 2")
    plt.ylabel("Objetivo 3")

    plt.tight_layout()
    plt.show()
    
    return 

"""
"""
if __name__ == "__main__":
    
    df = pd.read_csv("uploads/siblings.csv")
    mat = df.values
    mat1 = [row[1:] for row in mat]
    G = nx.read_gexf("uploads/school_net.gexf")

    solve_genetic_algorithm(mat1, G)
    

