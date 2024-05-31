import base64
from io import BytesIO
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import networkx as nx
import global_def as gd

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

    gd.classrooms = sorted(set(clases.values()))
    
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

def plot_pareto_front2D(pareto_front, all_fitness):
    objective1 = [fit[0] for fit in all_fitness]
    objective2 = [fit[1] for fit in all_fitness]
    objective3 = [fit[2] for fit in all_fitness]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].scatter(objective1, objective2, c='r', label='Individuos dominados')
    pareto_fitness1 = np.array([(ind[1][0], ind[1][1]) for ind in pareto_front])
    axs[0].scatter(pareto_fitness1[:, 0], pareto_fitness1[:, 1], c='b', label='Frente de Pareto')
    axs[0].set_title('Objetivo 1 (Max x) vs Objetivo 2 (Min y)')
    axs[0].set_xlabel('Número de componentes')
    axs[0].set_ylabel('Variabilidad del tamaño de componentes')
    axs[0].legend()

    axs[1].scatter(objective1, objective3, c='r', label='Individuos dominados')
    pareto_fitness2 = np.array([(ind[1][0], ind[1][2]) for ind in pareto_front])
    axs[1].scatter(pareto_fitness2[:, 0], pareto_fitness2[:, 1], c='b', label='Frente de Pareto')
    axs[1].set_title('Objetivo 1 (Max x) vs Objetivo 3 (Min y)')
    axs[1].set_xlabel('Número de componentes')
    axs[1].set_ylabel('Variabilidad del número de enlaces')
    axs[1].legend()

    axs[2].scatter(objective2, objective3, c='r', label='Individuos dominados')
    pareto_fitness3 = np.array([(ind[1][1], ind[1][2]) for ind in pareto_front])
    axs[2].scatter(pareto_fitness3[:, 0], pareto_fitness3[:, 1], c='b', label='Frente de Pareto')
    axs[2].set_title('Objetivo 2 (Min x) vs Objetivo 3 (Min y)')
    axs[2].set_xlabel('Variabilidad del tamaño de componentes')
    axs[2].set_ylabel('Variabilidad del número de enlaces')
    axs[2].legend()

    plt.tight_layout()

    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    img_data = 'data:image/png;base64,' + img_str

    plt.close(fig)

    return img_data

def solution_files(individual):

    changed = set()
    etapas = nx.get_node_attributes(gd.initial_network, 'Etapa')
    cursos = nx.get_node_attributes(gd.initial_network, 'Curso')
    clases = nx.get_node_attributes(gd.initial_network, 'Clase')
    print(gd.initial_network.nodes())
    for (classroom, (sib_name, sib_data)) in zip(individual, gd.siblings_dict.items()):
        print(gd.initial_network.nodes())
        if sib_name in changed:
            # Enlace de hermano
            gd.initial_network.add_edge(sib_name, sib_data[4])
        else:
            gd.initial_network.remove_edges_from(list(gd.initial_network.edges(str(sib_name))))
            stage = sib_data[1]
            year = sib_data[2]
            group = gd.classrooms[classroom]
            
            matching_nodes = []
            
            
            for node in gd.initial_network.nodes():
                if etapas[str(node)]== stage and cursos[str(node)] == year and clases[str(node)] == group:
                    matching_nodes.append(node)
            print(matching_nodes)
            
            # Enlace de hermano
            gd.initial_network.add_edge(sib_name, sib_data[4])
            
            # Enlaces de clase
            for matching_node_id in matching_nodes:
                gd.initial_network.add_edge(sib_name, matching_node_id)

            changed.add(sib_name)

    #print(gd.initial_network.edges)

