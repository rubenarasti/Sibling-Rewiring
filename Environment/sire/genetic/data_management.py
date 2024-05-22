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


def final_graph(individual):

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

"""


if __name__ == "__main__":
    df = pd.read_csv("../uploads/siblings.csv")
    mat = df.values
    G = nx.read_gexf("../uploads/school_net.gexf")

    load_data(mat, G)
    #print("Siblings: ", gd.siblings_dict)
    #print("total students: ", gd.total_students)
    #print("siblings: ",gd.siblings_number)
    indiv2 = [0] * gd.siblings_number
    final_graph(indiv2)

"""