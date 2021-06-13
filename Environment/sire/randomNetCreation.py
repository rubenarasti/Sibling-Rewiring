import networkx as nx
import random
from matplotlib import pyplot as plt
import pandas as pd


__stage = (['infantil', 'primaria', 'secundaria'])
__class = (['A', 'B', 'C'])

__initial_network = nx.Graph()
__siblings = []
__siblingsMatrix = []
__schoolyear_class = nx.Graph()
    

def create_initial_network(totalStudents, numberSiblings):
    """
    Creates the initial network
    
    """
    if totalStudents < (3*len(__class)+6*len(__class)+4*len(__class)):
        totalStudents = (3*len(__class)+6*len(__class)+4*len(__class))
    dicNombre = {}
    dicEtapa = {}
    dicCurso = {}
    dicClase = {}
    alumnos_clase = 0
    var = 3*len(__class)+6*len(__class)+4*len(__class)
    if totalStudents//var == totalStudents/var:
        alumnos_clase = totalStudents//var
    else:
        alumnos_clase = (totalStudents//var) + 1
        totalStudents = alumnos_clase*var
    
    __initial_network.add_nodes_from(range(totalStudents))
    
    x = 0
    for et in __stage:
        if et == __stage[0]:
            for curso in range(1,4):
                for alumno1 in range(alumnos_clase):
                    for letra in __class:
                        dicEtapa[x] = et
                        dicCurso[x] = curso
                        dicClase[x] = letra 
                        dicNombre[x] = x
                        x+=1
        elif et==__stage[1]:
            for curso in range(1,7):
                for alumno2 in range(alumnos_clase):
                    for letra in __class:
                        dicEtapa[x] = et
                        dicCurso[x] = curso
                        dicClase[x] = letra 
                        dicNombre[x] = x
                        x += 1
        elif et==__stage[2]:
            for curso in range(1,5):
                for alumno3 in range(alumnos_clase):
                    for letra in __class:
                        dicEtapa[x] = et
                        dicCurso[x] = curso
                        dicClase[x] = letra 
                        dicNombre[x] = x
                        x += 1
            
            
    nx.set_node_attributes(__initial_network, dicNombre, 'Nombre')
    nx.set_node_attributes(__initial_network, dicEtapa, 'Etapa')
    nx.set_node_attributes(__initial_network, dicCurso, 'Curso')
    nx.set_node_attributes(__initial_network, dicClase, 'Clase')
    
    nombres =  nx.get_node_attributes(__initial_network,'Nombre')
    etapas =  nx.get_node_attributes(__initial_network,'Etapa')
    cursos =  nx.get_node_attributes(__initial_network,'Curso')
    clases =  nx.get_node_attributes(__initial_network,'Clase')
    
    for nodex in __initial_network.nodes():
        for nodey in __initial_network.nodes():
            if nombres[nodex] != nombres[nodey] and etapas[nodex]==etapas[nodey] and cursos[nodex]==cursos[nodey] and clases[nodex]==clases[nodey]:
                enlace = (nodex, nodey)
                if enlace not in __initial_network.edges():
                    __initial_network.add_edge(nodex,nodey)
                      
    copy = list(__initial_network.nodes())
    
    for i in range(0,numberSiblings):
        node1 = random.choice(copy)
        node2 = random.choice(copy)
        edge = (node1,node2)
        if edge not in __initial_network.edges():
            __initial_network.add_edge(node1,node2)
            __siblings.append(edge)
    
    return __initial_network
    
def create_siblings_matrix():
    """
    Creates the matrix where there's the siblings' data.

    Returns
    -------
    dataframe
        dataframe with siblings' information.
    """
    
    siblings = []
    nombre_siblings = []
    etapa_siblings = []
    curso_siblings = []
    clase_siblings = []
    
    nombres = nx.get_node_attributes(__initial_network,'Nombre')
    etapas = nx.get_node_attributes(__initial_network,'Etapa')
    cursos = nx.get_node_attributes(__initial_network,'Curso')
    clases = nx.get_node_attributes(__initial_network,'Clase')
    
    for edge in __siblings:
        for ed in edge:
            if ed not in siblings:
                siblings.append(ed)
                nombre_siblings.append(nombres[ed])
                etapa_siblings.append(etapas[ed])
                curso_siblings.append(cursos[ed])
                clase_siblings.append(clases[ed])
                
    for i in range(0,len(nombre_siblings)):
        __siblingsMatrix.append([nombre_siblings[i],etapa_siblings[i],curso_siblings[i],clase_siblings[i]])
    #print('Es la matriz de hermanos')   
    #print(matriz_hermanos)
    
    data = {'nombre': nombre_siblings,
        'etapa': etapa_siblings,
        'curso' : curso_siblings,
        'clase': clase_siblings}
   
    df_siblings = pd.DataFrame(data, columns = ['nombre','etapa', 'curso', 'clase'])
    
    return df_siblings

def create_schoolyear_class_network():
    """
    Creates the net of classes, where edges are siblings.

    Returns
    -------
    network
        Net of schoolYear-class.
    """
    initial = __initial_network
    
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
    
        if node_name not in __schoolyear_class.nodes():
            __schoolyear_class.add_node(node_name)
            dicNombre[node_name] = node_name
            dicEtapa[node_name] = etapas[node]
            dicCurso[node_name] = cursos[node]
            dicClase[node_name] = clases[node]
            dicEstudiantes[node_name] = []    
            
    nx.set_node_attributes(__schoolyear_class, dicNombre, 'Nombre')
    nx.set_node_attributes(__schoolyear_class, dicEtapa, 'Etapa')
    nx.set_node_attributes(__schoolyear_class, dicCurso, 'Curso')
    nx.set_node_attributes(__schoolyear_class, dicClase, 'Clase')
    nx.set_node_attributes(__schoolyear_class, dicEstudiantes, 'Estudiantes')
    
        
    for edge in __siblings: 
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
        
        if (sibling1_name,sibling2_name) not in __schoolyear_class.edges():
            __schoolyear_class.add_edge(sibling1_name,sibling2_name)
            __schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] = 0
        else:
            __schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] += 1
    
    return __schoolyear_class
    
def generate_similar_net():
    """
    Generates a similar net to schoolyear_Class, where edges are siblings.

    Returns
    -------
    network
        Net of schoolYear-class.
    """
    
    net = nx.Graph()
    net = __schoolyear_class.copy()
    
    pos = 0
    for sibling in __siblingsMatrix:
        
        edges_to_remove = []
        new_class = random.choice(__class)
        
        sibling_to_change = sibling
        edges_to_remove = []
    
    	
        sibling_name = sibling_to_change[0]
    		
        name = []
        name.append(sibling_to_change[1])
        name.append(sibling_to_change[2])
        name.append(sibling_to_change[3])
        node_name_ini = ''.join(str(e) for e in name)
        
        __siblingsMatrix[pos][3] = new_class
    		
        name = []
        name.append(sibling_to_change[1])
        name.append(sibling_to_change[2])
        name.append(sibling_to_change[3])
        node_name_fin = ''.join(str(e) for e in name)
        
        dicEstudiantes = nx.get_node_attributes(net,'Estudiantes')
     
        dicEstudiantes[node_name_ini].remove(sibling_name)
        dicEstudiantes[node_name_fin].append(sibling_name)
        for edge in net.edges:
        	if node_name_ini in edge:
        		edges_to_remove.append(edge)
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
        pos += 1
    return net


#n = RandomNet()
#n.create_initial_network()
#dataframe = n.create_siblings_matrix()
#print(dataframe, n.siblings, n.siblingsMatrix)
#n.create_schoolyear_class_network()
#print(n.schoolyear_class.edges)