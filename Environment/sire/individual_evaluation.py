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

    #components_sizes_np = np.array(components_sizes)
    comp_size_var = np.var(components_sizes)

    #components_edges_np = np.array(components_edges)
    comp_edges_var = np.var(components_edges)

    return contag_compo, comp_size_var, comp_edges_var

def fenotype (individual):

    graph_eval = gd.graph_eval_ini.copy()
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
        
        sibling1_class = f"{sib_data1[1]}{sib_data1[2]}{gd.classrooms[classroom1]}"
        
        sib_data2 = gd.siblings_dict[sib_name2]
        classroom2 = individual[sib_data2[0]]

        sibling2_class = f"{sib_data2[1]}{sib_data2[2]}{gd.classrooms[classroom2]}"
        #CUIDADO CON EL ORDEN CREO QUE NO SE ESTA HACIENDO BIEN 
        if graph_eval.has_edge(sibling1_class, sibling2_class):
            graph_eval.edges[sibling1_class, sibling2_class]["weight"] += 1
        else:
            graph_eval.add_edge(sibling1_class, sibling2_class)
            graph_eval.edges[sibling1_class, sibling2_class]["weight"] = 1

    return graph_eval

"""

if __name__ == "__main__":
    import random
    df = pd.read_csv("../uploads/siblings.csv")
    G = nx.read_gexf("../uploads/school_net.gexf")
    matriz = df.values
    mat = matriz[:, 1:]
    dm.load_data(mat, G)
    n= gd.siblings_number
    indiv  = random.choices([0, 1, 2], k=n)
    indiv2 = [0] * n
    
    print('fitness:',fitness(indiv2))
    
"""


