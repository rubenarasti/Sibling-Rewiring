import pandas as pd
import numpy as np
import networkx as nx
import copy

import global_def as gd
import data_management as dm


def fitness (individual):

    graph_eval = fenotype(individual)

    components_sizes = []
    components_edges = []
    contag_compo = 0

    for component in nx.connected_components(graph_eval):
        contag_compo += 1
        components_sizes.append(len(component))
        subgraph = graph_eval.subgraph(component)
        total_weight = subgraph.size(weight='weight')
        components_edges.append(total_weight)

    comp_size_var = np.var(components_sizes)

    comp_edges_var = np.var(components_edges)

    return contag_compo, comp_size_var, comp_edges_var

def fenotype (individual):

    graph_eval = copy.deepcopy(gd.graph_eval_ini)
    seen = set() # Set to avoid repeating those already seen
    dicEstudiantes = nx.get_node_attributes(graph_eval,'Estudiantes')

    for (sib_name1, sib_data1) in gd.siblings_dict.items():

        classroom1 = individual[sib_data1[0]]
        sibling1_class = f"{sib_data1[1]}{sib_data1[2]}{gd.classrooms[classroom1]}"
        if sib_name1 not in dicEstudiantes[sibling1_class]:
            dicEstudiantes[sibling1_class].append(sib_name1)

        sib_names = sib_data1[4]
        for sib_name2 in sib_names:
            # Order the pair 
            if sib_name2 > sib_name1:
                siblings_pair = (sib_name1, sib_name2)
            else:
                siblings_pair = (sib_name2, sib_name1)

            if siblings_pair in seen:
                continue

            seen.add(siblings_pair)

            sib_data2 = gd.siblings_dict[sib_name2]
            classroom2 = individual[sib_data2[0]]

            sibling2_class = f"{sib_data2[1]}{sib_data2[2]}{gd.classrooms[classroom2]}"
            if sib_name2 not in dicEstudiantes[sibling2_class]:
                dicEstudiantes[sibling2_class].append(sib_name2)
            
            if graph_eval.has_edge(sibling1_class, sibling2_class):
                graph_eval.edges[sibling1_class, sibling2_class]["weight"] += 1
            else:
                graph_eval.add_edge(sibling1_class, sibling2_class)
                graph_eval.edges[sibling1_class, sibling2_class]["weight"] = 1

    return graph_eval

def convert_to_feasible(individual):
    new_individual = individual[:]
    modified = False # Flag to know when a solution is modified

    while True:
        graph_eval = fenotype(new_individual)
        dicEstudiantes = nx.get_node_attributes(graph_eval,'Estudiantes')
        solution_feasible = True
        print(solution_feasible)
        for students in dicEstudiantes.values():
            k = len(students) - gd.capacity # leftover students
            if k > 0:
                solution_feasible = False
                modified = True
                sibs_to_change = students[:k]
                for sib in sibs_to_change:
                    sib_data = gd.siblings_dict[sib]
                    classroom = new_individual[sib_data[0]]
                    # the new class is the previous letter 
                    if classroom == 0:
                        new_classroom = len(gd.classrooms) - 1
                    else:
                        new_classroom = classroom - 1
                    new_individual[sib_data[0]] = new_classroom

        if solution_feasible:
            break

    return new_individual, graph_eval, modified


def create_solution(individual):

    individual, graph_eval, modified = convert_to_feasible(individual)
    seen = set() # Set to avoid repeating those already seen
    graph_students = gd.initial_network.copy()
    students_by_edge = {}
    dicEstudiantes = nx.get_node_attributes(graph_eval,'Estudiantes')

    for (sib_name1, sib_data1) in gd.siblings_dict.items():

        classroom1 = individual[sib_data1[0]]
        sibling1_class = f"{sib_data1[1]}{sib_data1[2]}{gd.classrooms[classroom1]}"
        if sib_name1 not in dicEstudiantes[sibling1_class]:
            dicEstudiantes[sibling1_class].append(sib_name1)
        graph_students.nodes[sib_name1]["Clase"] = gd.classrooms[classroom1]

        sib_names = sib_data1[4]
        for sib_name2 in sib_names:
            # Order the pair 
            if sib_name2 > sib_name1:
                siblings_pair = (sib_name1, sib_name2)
            else:
                siblings_pair = (sib_name2, sib_name1)

            if siblings_pair in seen:
                continue

            seen.add(siblings_pair)

            sib_data2 = gd.siblings_dict[sib_name2]
            classroom2 = individual[sib_data2[0]]

            sibling2_class = f"{sib_data2[1]}{sib_data2[2]}{gd.classrooms[classroom2]}"
            if sib_name2 not in dicEstudiantes[sibling2_class]:
                dicEstudiantes[sibling2_class].append(sib_name2)

            graph_students.nodes[sib_name2]["Clase"] = gd.classrooms[classroom2]
    
            if sibling1_class < sibling2_class:
                edge = (sibling1_class, sibling2_class)
            else:
                edge = (sibling2_class, sibling1_class)
            if edge not in students_by_edge:
                students_by_edge[edge] = set()

            students_by_edge[edge].update([sib_name1, sib_name2])


    students_list = []
    siblings_set = set(gd.siblings_dict.keys())

        
    for nodo, datos in graph_students.nodes(data=True):
        nombre = nodo
        etapa = datos.get("Etapa")
        curso = datos.get("Curso")

        if nombre not in siblings_set:
            
            posible_classrooms = [f"{etapa}{curso}{clase}" for clase in gd.classrooms]
            for classroom in posible_classrooms:
                if len(dicEstudiantes[classroom]) < gd.capacity:
                    
                    dicEstudiantes[classroom].append(nombre)
                
                    row = {
                        "Nombre": nombre,
                        "Etapa": etapa,
                        "Curso": curso,
                        "Clase": classroom[-1]
                    }
                    students_list.append(row)
                    break
        else:
            clase = datos.get("Clase")
            row = {
                "Nombre": nombre,
                "Etapa": etapa,
                "Curso": curso,
                "Clase": clase
            }
            students_list.append(row)

    return graph_eval, students_by_edge, students_list, modified


