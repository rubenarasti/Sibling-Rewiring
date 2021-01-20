import networkx as nx
import random
from matplotlib import pyplot as plt

totalNodos = 200
G = nx.Graph()
siblings = []

def create_initial_network():
    GG = nx.Graph()
    GG.add_nodes_from(range(totalNodos))

    dicNombre = {}
    dicEtapa = {}
    dicCurso = {}
    dicClase = {}
    nodos = list(GG.nodes())
    curso = 0
    etapa = (['infantil', 'primaria', 'secundaria'])
    clase = (['A', 'B', 'C'])
    
    for x in nodos:
        selectedEtapa= random.choice(etapa)
        
        if selectedEtapa == 'infantil':
            curso = random.randint(1,3)
        elif selectedEtapa == 'primaria':
            curso = random.randint(1,6)
        else: 
            curso = random.randint(1,4)  
        
        selectedClase = random.choice(clase)
        
        dicNombre[x] = x
        dicEtapa[x] = selectedEtapa
        dicCurso[x] = curso
        dicClase[x] = selectedClase
        
    nx.set_node_attributes(GG, dicNombre, 'Nombre')
    nx.set_node_attributes(GG, dicEtapa, 'Etapa')
    nx.set_node_attributes(GG, dicCurso, 'Curso')
    nx.set_node_attributes(GG, dicClase, 'Clase')
    
    
    copy = list(GG.nodes())
    num = 10
    for i in range(0,num):
        node1 = random.choice(copy)
        node2 = random.choice(copy)
        edge = (node1,node2)
        if edge not in GG.edges():
            GG.add_edge(node1,node2)
            siblings.append(edge)
    
    pos=nx.kamada_kawai_layout(GG)
    
    nx.draw(GG, pos)
    node_labels = nx.get_node_attributes(GG,'Nombre')
    nx.draw_networkx_labels(GG, pos, labels = node_labels)
    node_labels1 = nx.get_node_attributes(GG,'Etapa')
    nx.draw_networkx_labels(GG, pos, labels = node_labels1)
    node_labels2 = nx.get_node_attributes(GG,'Curso')
    nx.draw_networkx_labels(GG, pos, labels = node_labels2)
    node_labels3 = nx.get_node_attributes(GG,'Clase')
    nx.draw_networkx_labels(GG, pos, labels = node_labels3)
    
    plt.show()
    
    
    nx.write_gexf(GG, "randomGraph.gexf")
    nx.write_gexf(GG, "randomGraph2.gexf")
    nx.write_gexf(GG, "randomGraphuploaded.gexf")
    
    return GG


G = create_initial_network()
 
etapa = nx.get_node_attributes(G, 'Etapa')
print(etapa[1])
print(G.nodes())
print(siblings)