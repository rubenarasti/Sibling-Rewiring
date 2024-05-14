import pandas as pd
import numpy as np
import networkx as nx
import copy

from . import global_def as gd
from . import data_management as dm


def fitness (individual):

    graph_eval = fenotype(individual)

    components_size = []
    contag_compo = 0

    for component in nx.connected_components(graph_eval):
        contag_compo += 1
        components_size.append(len(component))

    components_size_np = np.array(components_size)
    contag_indiv = components_size_np.var()
    #print(contag_compo, contag_indiv)

    return contag_compo, contag_indiv

def fenotype (individual):

    graph_eval = copy.deepcopy(gd.graph_eval_ini)
    dicEstudiantes = nx.get_node_attributes(graph_eval, 'Estudiantes')
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
        if sib_name1 not in dicEstudiantes[sibling1_class]:
            dicEstudiantes[sibling1_class].append(sib_name1)

        sib_data2 = gd.siblings_dict[sib_name2]
        classroom2 = individual[sib_data2[0]] # Obtain the sibling2 classroom with the index

        sibling2 = []
        sibling2.append(sib_data2[1])
        sibling2.append(sib_data2[2])
        sibling2.append(gd.classrooms[classroom2])
        sibling2_class = ''.join(str(e) for e in sibling2)
        if sib_name2 not in dicEstudiantes[sibling2_class]:
            dicEstudiantes[sibling2_class].append(sib_name2)

        #if (sibling1_class,sibling2_class) not in graph_eval.edges():
        graph_eval.add_edge(sibling1_class, sibling2_class)

    return graph_eval

"""

if __name__ == "__main__":
    import random
    df = pd.read_csv("../uploads/siblings.csv")
    G = nx.read_gexf("../uploads/school_net.gexf")

    dm.load_data(df, G)
    n= gd.siblings_number
    
    indiv  = random.choices([0, 1, 2], k=n)
    indiv2 = [0] * n
    
    print('fitness:',fitness(indiv2))
    
"""


