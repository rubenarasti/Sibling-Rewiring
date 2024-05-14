import numpy as np
import pandas as pd
import networkx as nx
from . import global_def as gd

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


"""


if __name__ == "__main__":
    df = pd.read_csv("../uploads/siblings.csv")
    mat = df.values
    G = nx.read_gexf("../uploads/school_net.gexf")

    load_data(mat, G)
    print("Siblings: ", gd.siblings_dict)
    print("total students: ", gd.total_students)
    print("siblings: ",gd.siblings_number)
"""

