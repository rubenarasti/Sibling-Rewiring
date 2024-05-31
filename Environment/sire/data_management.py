import base64
from io import BytesIO
import io
import os
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
    
    graph_eval = gd.graph_eval_ini.copy()
    seen = set() # Set to avoid repeating those already seen
    graph_students = gd.initial_network.copy()

    students_by_edge = {}

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

        sibling1_class = f"{sib_data1[1]}{sib_data1[2]}{gd.classrooms[classroom1]}"
        
        sib_data2 = gd.siblings_dict[sib_name2]
        classroom2 = individual[sib_data2[0]]

        sibling2_class = f"{sib_data2[1]}{sib_data2[2]}{gd.classrooms[classroom2]}"

        graph_students.nodes[str(sib_name1)]["Clase"] = gd.classrooms[classroom1]
        graph_students.nodes[str(sib_name2)]["Clase"] = gd.classrooms[classroom2]
        
        if sibling1_class < sibling2_class:
            edge = (sibling1_class, sibling2_class)
        else:
            edge = (sibling2_class, sibling1_class)
        if edge not in students_by_edge:
            students_by_edge[edge] = set()

        students_by_edge[edge].update([sib_name1, sib_name2])

        if graph_eval.has_edge(sibling1_class, sibling2_class):
            graph_eval.edges[sibling1_class, sibling2_class]["weight"] += 1
        else:
            graph_eval.add_edge(sibling1_class, sibling2_class)
            graph_eval.edges[sibling1_class, sibling2_class]["weight"] = 1

    df = pd.DataFrame(columns=["Clase 1", "Clase 2", "Estudiantes"])

    
    for edge, students in students_by_edge.items():
        df = df.append({
            "Clase 1": edge[0], 
            "Clase 2": edge[1], 
            "Estudiantes": ", ".join(str(student) for student in sorted(students))
        }, ignore_index=True)
    df = df.sort_values(by=["Clase 1", "Clase 2"])
    connections_buffer = BytesIO()
    df.to_csv(connections_buffer, index=False)
    connections_buffer.seek(0)
    connections_str = base64.b64encode(connections_buffer.read())

    data = []
    for nodo, datos in graph_students.nodes(data=True):
        row = {
            "Nombre": datos.get("Nombre"),
            "Etapa": datos.get("Etapa"),
            "Curso": datos.get("Curso"),
            "Clase": datos.get("Clase")
        }
        data.append(row)

    df_attributes = pd.DataFrame(data)
    attributes_buffer = BytesIO()
    df_attributes.to_csv(attributes_buffer, index=False)
    attributes_buffer.seek(0)
    attributes_str = base64.b64encode(attributes_buffer.read())

    plt.figure(figsize=(12, 12))
    pos = nx.circular_layout(graph_eval)
    nx.draw(graph_eval, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_color='black', edge_color='gray')
    edge_labels = nx.get_edge_attributes(graph_eval, 'weight')
    nx.draw_networkx_edge_labels(graph_eval, pos, edge_labels=edge_labels)
    
    graph_image_buffer = BytesIO()
    plt.savefig(graph_image_buffer, format="PNG")
    plt.close()
    graph_image_buffer.seek(0)
    graph_image_str = base64.b64encode(graph_image_buffer.read())
    
    return {
    "estudiantes.csv": attributes_str,
    "grafo.png": graph_image_str,
    "par_clases.csv": connections_str
    }

"""
if __name__ == "__main__":


    df_path = os.path.join("files to upload", "siblings.csv")
    df = pd.read_csv(df_path)
    mat = df.values[:, 1:]
    # Leer el grafo desde el archivo GEXF
    gexf_path = os.path.join("files to upload", "school_net.gexf")
    G = nx.read_gexf(gexf_path)
    load_data(mat, G)

    ind = [0]*gd.siblings_number
    solution_files(ind)

"""