import base64
import colorsys
from io import BytesIO
import io
import math
import random
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import networkx as nx
import global_def as gd
import individual_evaluation as ie

def load_data(siblings, graph):

    gd.initial_network = graph
    gd.total_students = len(graph.nodes())
    gd.siblings_dict = {}

    # Reconvert the siblings matrix to a pandas dataframe
    columns = ['nombre', 'etapa', 'curso', 'clase', 'hermano de']
    siblings_df = pd.DataFrame(siblings, columns=columns)

    # Group data by name
    siblings_grouped = siblings_df.groupby('nombre')

    for index, (name, group) in enumerate(siblings_grouped):

        etapa = group['etapa'].iloc[0]
        curso = group['curso'].iloc[0]
        clase = group['clase'].iloc[0]

        # siblings list
        hermanos = [str(h) for h in group['hermano de'].tolist()]

        # dict to access siblings fastly
        gd.siblings_dict[str(name)] = [index,
                                    str(etapa),
                                    str(curso),
                                    str(clase),
                                    hermanos
                                    ]

    gd.siblings_number = len(gd.siblings_dict)

    students_count = {}
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

        course_key = (etapas[node], cursos[node])
        if course_key not in students_count:
            students_count[course_key] = 0
        students_count[course_key] += 1
			
    nx.set_node_attributes(gd.graph_eval_ini, dicNombre, 'Nombre')
    nx.set_node_attributes(gd.graph_eval_ini, dicEtapa, 'Etapa')
    nx.set_node_attributes(gd.graph_eval_ini, dicCurso, 'Curso')
    nx.set_node_attributes(gd.graph_eval_ini, dicClase, 'Clase')
    nx.set_node_attributes(gd.graph_eval_ini, dicEstudiantes, 'Estudiantes')	

    for num_students in students_count.values():
        course_capacity = math.ceil(num_students / len(gd.classrooms))
        if course_capacity > gd.capacity:
            gd.capacity = course_capacity

def convert_to_base64(data, data_type):
    buffer = BytesIO()

    if data_type == 'csv':
        data.to_csv(buffer, index=False)
    elif data_type == 'matplotlib_figure':
        data.savefig(buffer, format='png')
    elif data_type == 'graph':
        nx.write_gexf(data, buffer)
    
    buffer.seek(0)
    data_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return data_str  

def plot_pareto_front_2d(pareto_front, all_fitness):
    objective1 = [fit[0] for fit in all_fitness]
    objective2 = [fit[1] for fit in all_fitness]
    objective3 = [fit[2] for fit in all_fitness]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    dominated_tag = 'Individuos dominados'
    non_dominated_tag = 'Frente de Pareto'
    objective1_tag = 'Número de componentes'
    objective2_tag = 'Variabilidad del tamaño de componentes'
    objective3_tag = 'Variabilidad del número de enlaces'

    axs[0].scatter(objective1, objective2, c='r', label=dominated_tag)
    pareto_fitness1 = np.array([(ind[1][0], ind[1][1]) for ind in pareto_front])
    axs[0].scatter(pareto_fitness1[:, 0], pareto_fitness1[:, 1], c='b', label=non_dominated_tag)
    axs[0].set_title('Objetivo 1 (Max x) vs Objetivo 2 (Min y)')
    axs[0].set_xlabel(objective1_tag)
    axs[0].set_ylabel(objective2_tag)
    axs[0].legend()

    axs[1].scatter(objective1, objective3, c='r', label=dominated_tag)
    pareto_fitness2 = np.array([(ind[1][0], ind[1][2]) for ind in pareto_front])
    axs[1].scatter(pareto_fitness2[:, 0], pareto_fitness2[:, 1], c='b', label=non_dominated_tag)
    axs[1].set_title('Objetivo 1 (Max x) vs Objetivo 3 (Min y)')
    axs[1].set_xlabel(objective1_tag)
    axs[1].set_ylabel(objective3_tag)
    axs[1].legend()

    axs[2].scatter(objective2, objective3, c='r', label=dominated_tag)
    pareto_fitness3 = np.array([(ind[1][1], ind[1][2]) for ind in pareto_front])
    axs[2].scatter(pareto_fitness3[:, 0], pareto_fitness3[:, 1], c='b', label=non_dominated_tag)
    axs[2].set_title('Objetivo 2 (Min x) vs Objetivo 3 (Min y)')
    axs[2].set_xlabel(objective2_tag)
    axs[2].set_ylabel(objective3_tag)
    axs[2].legend()

    plt.tight_layout()

    data_str = convert_to_base64(fig, data_type='matplotlib_figure')

    img_data = 'data:image/png;base64,' + data_str

    plt.close(fig)

    return img_data

def solution_files(individual):
    
    graph_eval, students_by_edge, students_list, modified = ie.create_solution(individual)

    for node in graph_eval.nodes:
        graph_eval.nodes[node]['Estudiantes'] = ', '.join(graph_eval.nodes[node]['Estudiantes'])

    graph_eval_str = convert_to_base64(graph_eval, 'graph')
    
    df_connections = pd.DataFrame(columns=["Clase 1", "Clase 2", "Estudiantes"])
    
    for edge, students in students_by_edge.items():
        temp_df = pd.DataFrame({
            "Clase 1": [edge[0]],
            "Clase 2": [edge[1]],
            "Estudiantes": [", ".join(student for student in sorted(students))]
        })

        df_connections = pd.concat([df_connections, temp_df], ignore_index=True)
    
    connections_str = convert_to_base64(df_connections, data_type='csv')

    df_students = pd.DataFrame(students_list)
    students_str = convert_to_base64(df_students, data_type='csv')


    components = list(nx.connected_components(graph_eval))
    unique_colors = generate_unique_colors(len(components))
    
    color_map = {}
    
    for i, component in enumerate(components):
        color = unique_colors[i]
        for node in component:
            color_map[node] = color
    
    node_colors = [color_map[node] for node in graph_eval.nodes()]

    plt.figure(figsize=(12, 12))
    pos = nx.circular_layout(graph_eval)
    nx.draw(graph_eval, pos, with_labels=True, node_size=1000, node_color=node_colors,
            font_size=15, font_color='black', edge_color='gray')

    edge_labels = nx.get_edge_attributes(graph_eval, 'weight')
    nx.draw_networkx_edge_labels(graph_eval, pos, edge_labels=edge_labels)

    from matplotlib.patches import Patch
    
    legend_elements = []
    for i, component in enumerate(components):
        color = unique_colors[i]
        subgraph = graph_eval.subgraph(component)
        num_nodes = len(component)
        num_edges = subgraph.size(weight='weight')
        
        label = f'{i+1} Tamaño: {num_nodes}, Enlaces: {int(num_edges)}'
        legend_elements.append(Patch(facecolor=color, edgecolor='black', label=label))
    
    plt.legend(handles=legend_elements, loc='upper right', title='Componentes')
    graph_image_str = convert_to_base64(plt, data_type='matplotlib_figure')
    
    plt.close()
    
    return ({
    "grafo_clases.gexf": graph_eval_str,
    "estudiantes.csv": students_str,
    "grafo_clases.png": graph_image_str,
    "par_clases.csv": connections_str
    }, modified)

def generate_unique_colors(num_colors):
    hues = [i / num_colors for i in range(num_colors)]
    random.shuffle(hues)  
    return [colorsys.hsv_to_rgb(hue, 0.7, 1.0) for hue in hues]


def generate_solutions_list(pareto_front):
    solutions = []

    for index, (individual, fitness) in enumerate(pareto_front):
        individual_id = index + 1
        rounded_fitness = (int(fitness[0]), float(round(fitness[1], 2)), float(round(fitness[2], 2)))
        row = {
            "Id": individual_id,
            "Individual": f"Solución {individual_id}",
            "Fitness": rounded_fitness,
            "Individual_data": individual
        }
        solutions.append(row)

    return solutions, individual_id

def solution_name(individual_id, fitness, modified, individual):
    if modified:
        fitness = ie.fitness(individual)
    
    modified_flag = "modified_" if modified else ""
    return f"{modified_flag}solution{individual_id}_{fitness}.zip"
