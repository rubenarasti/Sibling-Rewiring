import pandas as pd
import numpy as np
import networkx as nx
import copy

import global_def as gd
import data_management as dm


def fitness (individual):

    graph_eval = fenotype(individual)

    components_size = []
    dicEstudiantes = nx.get_node_attributes(graph_eval, 'Estudiantes')
    contag_compo = 0

    for component in nx.connected_components(graph_eval):
        contag_compo += 1
        components_size.append(len(component))

    #print(components_size)
    components_size_np = np.array(components_size)
    contag_indiv = components_size_np.var()

    return contag_compo, contag_indiv

def fenotype (individual):

    graph_eval = copy.deepcopy(gd.graph_eval_ini)
    dicEstudiantes = nx.get_node_attributes(graph_eval, 'Estudiantes')

    for (classroom1, classroom2, sib1, sib2) in zip(
                                            individual[::2],
                                            individual[1::2],
                                            gd.siblings_matrix[::2],
                                            gd.siblings_matrix[1::2]):
        
        sibling1 = []
        sibling1.append(sib1[2])
        sibling1.append(sib1[3])
        sibling1.append(gd.classroom[classroom1])
        sibling1_name = ''.join(str(e) for e in sibling1)
        if sib1[1] not in dicEstudiantes[sibling1_name]:
            dicEstudiantes[sibling1_name].append(sib1[1])

        sibling2 = []
        sibling2.append(sib2[2])
        sibling2.append(sib2[3])
        sibling2.append(gd.classroom[classroom2])
        sibling2_name = ''.join(str(e) for e in sibling2)
        if sib2[1] not in dicEstudiantes[sibling2_name]:
            dicEstudiantes[sibling2_name].append(sib2[1])
		
        if (sibling1_name,sibling2_name) not in graph_eval.edges():
            graph_eval.add_edge(sibling1_name,sibling2_name)

    return graph_eval

"""

if __name__ == "__main__":
    import random
    df = pd.read_csv("../uploads/siblings.csv")
    G = nx.read_gexf("../uploads/school_net.gexf")

    dm.load_data(df, G, 50)
    n= gd.siblings_number
    
    indiv  = random.choices([0, 1, 2], k=n)
    indiv2 = [0] * n
    
    print('fitness single obj:',fitness(indiv2))
    

"""

