import networkx as nx
import random
import pandas as pd
from matplotlib import pyplot as plt

totalNodos = 200
G = nx.Graph()
siblings = []

def create_initial_network():
    initial_network = nx.Graph()
    initial_network.add_nodes_from(range(totalNodos))

    dicNombre = {}
    dicEtapa = {}
    dicCurso = {}
    dicClase = {}
    nodos = list(initial_network.nodes())
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
        
    nx.set_node_attributes(initial_network, dicNombre, 'Nombre')
    nx.set_node_attributes(initial_network, dicEtapa, 'Etapa')
    nx.set_node_attributes(initial_network, dicCurso, 'Curso')
    nx.set_node_attributes(initial_network, dicClase, 'Clase')
    
    
    copy = list(initial_network.nodes())
    num = 10
    for i in range(0,num):
        node1 = random.choice(copy)
        node2 = random.choice(copy)
        edge = (node1,node2)
        if edge not in initial_network.edges():
            initial_network.add_edge(node1,node2)
            siblings.append(edge)

    pos=nx.kamada_kawai_layout(initial_network)
    
    nx.draw(initial_network, pos)
    node_labels = nx.get_node_attributes(initial_network,'Nombre')
    nx.draw_networkx_labels(initial_network, pos, labels = node_labels)
    node_labels1 = nx.get_node_attributes(initial_network,'Etapa')
    nx.draw_networkx_labels(initial_network, pos, labels = node_labels1)
    node_labels2 = nx.get_node_attributes(initial_network,'Curso')
    nx.draw_networkx_labels(initial_network, pos, labels = node_labels2)
    node_labels3 = nx.get_node_attributes(initial_network,'Clase')
    nx.draw_networkx_labels(initial_network, pos, labels = node_labels3)
    
    plt.show()
    
    
    nx.write_gexf(initial_network, "randomGraph.gexf")
    nx.write_gexf(initial_network, "randomGraph2.gexf")
    nx.write_gexf(initial_network, "randomGraphuploaded.gexf")
    
    return initial_network

def create_siblings_matrix():
    initial = nx.Graph()
    initial = create_initial_network()
    
    siblings = []
    nombre_siblings = []
    etapa_siblings = []
    curso_siblings = []
    clase_siblings = []
    matriz_hermanos = []
    
    nombres = nx.get_node_attributes(initial,'Nombre')
    etapas = nx.get_node_attributes(initial,'Etapa')
    cursos = nx.get_node_attributes(initial,'Curso')
    clases = nx.get_node_attributes(initial,'Clase')
    
    for edge in initial.edges():
        for e in edge:
            if e not in siblings:
                siblings.append(e)
                nombre_siblings.append(nombres[e])
                etapa_siblings.append(etapas[e])
                curso_siblings.append(cursos[e])
                clase_siblings.append(clases[e])
                
    for i in range(0,len(nombre_siblings)):
        matriz_hermanos.append([nombre_siblings[i],etapa_siblings[i],curso_siblings[i],clase_siblings[i]])
        
    print(matriz_hermanos)
    
    data = {'nombre': nombre_siblings,
        'etapa': etapa_siblings,
        'curso' : curso_siblings,
        'clase': clase_siblings}
   
    df_siblings = pd.DataFrame(data, columns = ['nombre','etapa', 'curso', 'clase'])
    
    return initial, df_siblings
    
G, siblings = create_siblings_matrix()
print(siblings)
print(siblings.values)