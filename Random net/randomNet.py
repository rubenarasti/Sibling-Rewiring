import networkx as nx
from math import e
import random
import pandas as pd
from matplotlib import pyplot as plt

totalAlumnos = 784
#975
G = nx.Graph()
G_siblings = nx.Graph()
siblings = []

def create_initial_network():
    initial_network = nx.Graph()
    initial_network.add_nodes_from(range(totalAlumnos))

    dicNombre = {}
    dicEtapa = {}
    dicCurso = {}
    dicClase = {}
    etapa = (['infantil', 'primaria', 'secundaria'])
    clase = (['A', 'B', 'C'])
    alumnos_clase = 0
    
    if totalAlumnos//(3*len(clase)+6*len(clase)+4*len(clase)) == totalAlumnos/(3*len(clase)+6*len(clase)+4*len(clase)):
        alumnos_clase = totalAlumnos//(3*len(clase)+6*len(clase)+4*len(clase))
    else:
        alumnos_clase = (totalAlumnos//(3*len(clase)+6*len(clase)+4*len(clase))) + 1
        
    
    x = 0
    for et in etapa:
        letra = 0
        if et == etapa[0]:
            for curso in range(1,4):
                for alumno1 in range(alumnos_clase):
                    for letra in clase:
                        dicEtapa[x] = et
                        dicCurso[x] = curso
                        dicClase[x] = letra 
                        dicNombre[x] = x
                        x+=1
        elif et==etapa[1]:
            for curso in range(1,7):
                for alumno2 in range(alumnos_clase):
                    for letra in clase:
                        dicEtapa[x] = et
                        dicCurso[x] = curso
                        dicClase[x] = letra 
                        dicNombre[x] = x
                        x += 1
        elif et==etapa[2]:
            for curso in range(1,5):
                for alumno3 in range(alumnos_clase):
                    for letra in clase:
                        #print('etapa', et,'curso', curso,'clase', letra, 'alumno', x,sep=',')
                        dicEtapa[x] = et
                        dicCurso[x] = curso
                        dicClase[x] = letra 
                        dicNombre[x] = x
                        x += 1
            
            
    nx.set_node_attributes(initial_network, dicNombre, 'Nombre')
    nx.set_node_attributes(initial_network, dicEtapa, 'Etapa')
    nx.set_node_attributes(initial_network, dicCurso, 'Curso')
    nx.set_node_attributes(initial_network, dicClase, 'Clase')
    
    nombres =  nx.get_node_attributes(initial_network,'Nombre')
    etapas =  nx.get_node_attributes(initial_network,'Etapa')
    cursos =  nx.get_node_attributes(initial_network,'Curso')
    clases =  nx.get_node_attributes(initial_network,'Clase')
    
    for nodex in initial_network.nodes():
        for nodey in initial_network.nodes():
            if nombres[nodex] != nombres[nodey] and etapas[nodex]==etapas[nodey] and cursos[nodex]==cursos[nodey] and clases[nodex]==clases[nodey]:
                enlace = (nodex, nodey)
                if enlace not in initial_network.edges():
                    initial_network.add_edge(nodex,nodey)
                      
    copy = list(initial_network.nodes())
    num = 50
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
    #node_labels1 = nx.get_node_attributes(initial_network,'Etapa')
    #nx.draw_networkx_labels(initial_network, pos, labels = node_labels1)
    #node_labels2 = nx.get_node_attributes(initial_network,'Curso')
    #nx.draw_networkx_labels(initial_network, pos, labels = node_labels2)
    #node_labels3 = nx.get_node_attributes(initial_network,'Clase')
    #nx.draw_networkx_labels(initial_network, pos, labels = node_labels3)
    
    plt.show()
    
    
    #nx.write_gexf(initial_network, "randomGraph.gexf")
    #nx.write_gexf(initial_network, "randomGraph2.gexf")
    #nx.write_gexf(initial_network, "randomGraphuploaded.gexf")
    
    return initial_network, siblings
   

def create_siblings_matrix():
    initial = nx.Graph()
    initial, hermanos = create_initial_network()
    
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
    
    
    for edge in hermanos:
        for ed in edge:
            if ed not in siblings:
                siblings.append(ed)
                nombre_siblings.append(nombres[ed])
                etapa_siblings.append(etapas[ed])
                curso_siblings.append(cursos[ed])
                clase_siblings.append(clases[ed])
                
    for i in range(0,len(nombre_siblings)):
        matriz_hermanos.append([nombre_siblings[i],etapa_siblings[i],curso_siblings[i],clase_siblings[i]])
    #print('Es la matriz de hermanos')   
    #print(matriz_hermanos)
    
    data = {'nombre': nombre_siblings,
        'etapa': etapa_siblings,
        'curso' : curso_siblings,
        'clase': clase_siblings}
   
    df_siblings = pd.DataFrame(data, columns = ['nombre','etapa', 'curso', 'clase'])
    
    return initial, hermanos, matriz_hermanos, df_siblings

def create_schoolyear_class_network(G, hermanos):
    initial = G
    schoolyear_class = nx.Graph()
    dicNombre = {}
    dicEtapa = {}
    dicCurso = {}
    dicClase = {}
    dicEstudiantes = {}
    etapas = nx.get_node_attributes(initial,'Etapa')
    clases = nx.get_node_attributes(initial,'Clase')
    cursos = nx.get_node_attributes(initial,'Curso')
    
    for node in initial.nodes():
        name = []
        name.append(etapas[node])
        name.append(cursos[node])
        name.append(clases[node])
        node_name = ''.join(str(e) for e in name)
    
        if node_name not in schoolyear_class.nodes():
            schoolyear_class.add_node(node_name)
            dicNombre[node_name] = node_name
            dicEtapa[node_name] = etapas[node]
            dicCurso[node_name] = cursos[node]
            dicClase[node_name] = clases[node]
            dicEstudiantes[node_name] = []    
            
    nx.set_node_attributes(schoolyear_class, dicNombre, 'Nombre')
    nx.set_node_attributes(schoolyear_class, dicEtapa, 'Etapa')
    nx.set_node_attributes(schoolyear_class, dicCurso, 'Curso')
    nx.set_node_attributes(schoolyear_class, dicClase, 'Clase')
    nx.set_node_attributes(schoolyear_class, dicEstudiantes, 'Estudiantes')
    
        
    for edge in hermanos: #para poner los enlaces 
        sibling1 = []
        sibling1.append(etapas[edge[0]])
        sibling1.append(cursos[edge[0]])
        sibling1.append(clases[edge[0]])
        sibling1_name = ''.join(str(e) for e in sibling1)
        if edge[0] not in dicEstudiantes[sibling1_name]:
            dicEstudiantes[sibling1_name].append(edge[0])
        
        sibling2 = []
        sibling2.append(etapas[edge[1]])
        sibling2.append(cursos[edge[1]])
        sibling2.append(clases[edge[1]])
        sibling2_name = ''.join(str(e) for e in sibling2)
        if edge[1] not in dicEstudiantes[sibling2_name]:
            dicEstudiantes[sibling2_name].append(edge[1])
        
        if (sibling1_name,sibling2_name) not in schoolyear_class.edges():
            schoolyear_class.add_edge(sibling1_name,sibling2_name)
            schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] = 0
        else:
            schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] += 1
    
        #print('peso del enlace', schoolyear_class.get_edge_data(sibling1_name, sibling2_name), (sibling1_name,sibling2_name))
    #print('enlaces de schoolyear_class')
    #print(schoolyear_class.edges(data=True))
    #print(len(schoolyear_class.edges()))
    #print(nx.get_node_attributes(schoolyear_class,'Estudiantes'))
    
    pos=nx.circular_layout(schoolyear_class)
    
    nx.draw(schoolyear_class, pos)
    node_labels = nx.get_node_attributes(schoolyear_class,'Nombre')
    nx.draw_networkx_labels(schoolyear_class, pos, labels = node_labels)
    edge_labels = nx.get_edge_attributes(schoolyear_class,'peso')
    nx.draw_networkx_edge_labels(schoolyear_class, pos, labels = edge_labels)
    
    plt.show()

    return schoolyear_class



def generate_neighbor(matrix, net):
    clase = (['A', 'B', 'C'])
    pos = random.randint(0,(len(matrix)-1))
    sibling_to_change = matrix[pos]
    edges_to_remove = []
    
    sibling_name = sibling_to_change[0]
    
    name = []
    name.append(sibling_to_change[1])
    name.append(sibling_to_change[2])
    name.append(sibling_to_change[3])
    node_name_ini = ''.join(str(e) for e in name)
    
    new_class = random.choice(clase)
    matrix[pos][3] = new_class
    
    name = []
    name.append(sibling_to_change[1])
    name.append(sibling_to_change[2])
    name.append(sibling_to_change[3])
    node_name_fin = ''.join(str(e) for e in name)
    
    dicEstudiantes = nx.get_node_attributes(net,'Estudiantes')
    
    if node_name_ini != node_name_fin:
        dicEstudiantes[node_name_ini].remove(sibling_name)
        dicEstudiantes[node_name_fin].append(sibling_name)
        
        for edge in net.edges:
            if node_name_ini in edge:
                
                edges_to_remove.append(edge)
                #print(node_name_ini, edge[0], edge[1])
                peso = net.edges[edge[0], edge[1]]["peso"] 
                if peso > 0:
                    net.edges[edge[0], edge[1]]["peso"] -= 1
                
    
    for rem in edges_to_remove:  
        net.remove_edge(rem[0], rem[1])
        
        if rem[0] == node_name_ini:
            if (node_name_fin, rem[1]) not in net.edges():
                net.add_edge(node_name_fin, rem[1])
                net.edges[node_name_fin, rem[1]]["peso"] = 0
            else:
                net.edges[node_name_fin, rem[1]]["peso"] += 1
        elif rem[1] == node_name_ini:
            if (rem[0], node_name_fin) not in net.edges():
                net.add_edge(rem[0], node_name_fin)
                net.edges[rem[0], node_name_fin]["peso"] = 0
            else:
                net.edges[rem[0], node_name_fin]["peso"] += 1
            
    
    
    return net


def solve(G_siblings):
    return (sum(dict(G_siblings.degree()).values())/G_siblings.number_of_nodes())
    
    
def solve_simulated_annealing(G, matrix):
    
    tf = random.uniform(0.05, 0.01)
    alpha = random.uniform(0.8, 0.99)
    l = random.randint(10,50)
    current_solution = generate_neighbor(matrix,G)
    t = solve(G) * 0.4
    candidate_solution = current_solution
        
    vecino_inicial = current_solution
        
        
    while t >= tf:
        for i in range(l):
            aux = generate_neighbor(matrix,current_solution)
            candidate_solution = aux
            candidate_fmax = solve(candidate_solution)
            current_fmax = solve(current_solution)
            diff = candidate_fmax - current_fmax

            if diff < 0 or random.random() < e**(-diff/t):
                current_solution = candidate_solution
                
            if vecino_inicial is not current_solution:
                print('\n*******ha cambiado*********************')
                #print('VECINO ACTUAL -', current_solution.edges)
                print('diff', diff)
            #print(current_fmax, candidate_fmax)
        t = alpha * t
        
        
    print('\n****************************')
    print('MEJOR VECINO ENCONTRADO -', current_solution)
    print(current_solution.edges)
    print('Fmax -', current_fmax)
        
    
G, hermanos, siblings_matrix, df_siblings = create_siblings_matrix()
#print(df_siblings)
#print(siblings)
#print(siblings.values)
G_siblings = create_schoolyear_class_network(G, hermanos)
#create_initial_network()
#generate_neighbor(siblings_matrix, G_siblings)

#solve_simulated_annealing(G_siblings, siblings_matrix)
