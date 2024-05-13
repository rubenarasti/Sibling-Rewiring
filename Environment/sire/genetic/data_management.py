import numpy as np
import pandas as pd
import networkx as nx
import global_def as gd

def load_data(siblings_df, graph):

    gd.initial_network = graph
    gd.total_students = len(graph.nodes())
    gd.siblings_number = len(siblings_df)

    for index, row in siblings_df.iterrows():
        gd.siblings_dict[row[1]] = [row[0]] + row[2:].tolist()

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


def save(file_path, result):

    with open(file_path, "w+") as file:
        for r in result[1:]:
            r_str = str(r)[1:-1].replace(',','')
            file.write("{} {}\n".format(len(r), r_str))

"""


if __name__ == "__main__":
    df = pd.read_csv("../uploads/siblings.csv")
    G = nx.read_gexf("../uploads/school_net.gexf")

    load_data(df, G)
    print("total students: ", gd.total_students)
    print("siblings: ",gd.siblings_number)

"""
