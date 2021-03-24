import networkx as nx
import random
from matplotlib import pyplot as plt
import pandas as pd

class RandomNet:
    """
    Class randomNet
    
    A class to create the initial and schoolyear_Class nets.
    
    Attributes
    ----------
    totalStudents : int
        integer, total number of students

    Methods
    -------
    create_initial_network
        Creates the net of all students
    
    create_siblings_matrix
        Creates the matrix and dataframe of siblings
    
    create_schoolyear_class_network
        Creates the schoolyear-class
    """
    
    def __init__(self):
        """
        Parameters
        ----------
        totalStudents : int
            Total number of Students
        numberSiblings : int
            Number of couples of siblings
        """
        self.etapa = (['infantil', 'primaria', 'secundaria'])
        self.clase = (['A', 'B', 'C'])
        self.totalStudents = int(input('Introduce el total de alumnos: '))
        if self.totalStudents < (3*len(self.clase)+6*len(self.clase)+4*len(self.clase)):
            self.totalStudents = (3*len(self.clase)+6*len(self.clase)+4*len(self.clase))
        self.numberSiblings = int(input('Introduce el número de parejas de hermanos: '))
        self.initial_network = nx.Graph()
        self.siblings = []
        self.siblingsMatrix = []
        self.schoolyear_class = nx.Graph()
        
    
    def create_initial_network(self):
        """
        Creates the initial network
        
        """
        
        dicNombre = {}
        dicEtapa = {}
        dicCurso = {}
        dicClase = {}
        alumnos_clase = 0
        var = 3*len(self.clase)+6*len(self.clase)+4*len(self.clase)
        if self.totalStudents//var == self.totalStudents/var:
            alumnos_clase = self.totalStudents//var
        else:
            alumnos_clase = (self.totalStudents//var) + 1
            self.totalStudents = alumnos_clase*var
        
        self.initial_network.add_nodes_from(range(self.totalStudents))
        
        x = 0
        for et in self.etapa:
            if et == self.etapa[0]:
                for curso in range(1,4):
                    for alumno1 in range(alumnos_clase):
                        for letra in self.clase:
                            dicEtapa[x] = et
                            dicCurso[x] = curso
                            dicClase[x] = letra 
                            dicNombre[x] = x
                            x+=1
            elif et==self.etapa[1]:
                for curso in range(1,7):
                    for alumno2 in range(alumnos_clase):
                        for letra in self.clase:
                            dicEtapa[x] = et
                            dicCurso[x] = curso
                            dicClase[x] = letra 
                            dicNombre[x] = x
                            x += 1
            elif et==self.etapa[2]:
                for curso in range(1,5):
                    for alumno3 in range(alumnos_clase):
                        for letra in self.clase:
                            #print('etapa', et,'curso', curso,'clase', letra, 'alumno', x,sep=',')
                            dicEtapa[x] = et
                            dicCurso[x] = curso
                            dicClase[x] = letra 
                            dicNombre[x] = x
                            x += 1
                
                
        nx.set_node_attributes(self.initial_network, dicNombre, 'Nombre')
        nx.set_node_attributes(self.initial_network, dicEtapa, 'Etapa')
        nx.set_node_attributes(self.initial_network, dicCurso, 'Curso')
        nx.set_node_attributes(self.initial_network, dicClase, 'Clase')
        
        nombres =  nx.get_node_attributes(self.initial_network,'Nombre')
        etapas =  nx.get_node_attributes(self.initial_network,'Etapa')
        cursos =  nx.get_node_attributes(self.initial_network,'Curso')
        clases =  nx.get_node_attributes(self.initial_network,'Clase')
        
        for nodex in self.initial_network.nodes():
            for nodey in self.initial_network.nodes():
                if nombres[nodex] != nombres[nodey] and etapas[nodex]==etapas[nodey] and cursos[nodex]==cursos[nodey] and clases[nodex]==clases[nodey]:
                    enlace = (nodex, nodey)
                    if enlace not in self.initial_network.edges():
                        self.initial_network.add_edge(nodex,nodey)
                          
        copy = list(self.initial_network.nodes())
        
        for i in range(0,self.numberSiblings):
            node1 = random.choice(copy)
            node2 = random.choice(copy)
            edge = (node1,node2)
            if edge not in self.initial_network.edges():
                self.initial_network.add_edge(node1,node2)
                self.siblings.append(edge)
        
        pos=nx.kamada_kawai_layout(self.initial_network)
        
        nx.draw(self.initial_network, pos)
        node_labels = nx.get_node_attributes(self.initial_network,'Nombre')
        nx.draw_networkx_labels(self.initial_network, pos, labels = node_labels)
        #node_labels1 = nx.get_node_attributes(initial_network,'Etapa')
        #nx.draw_networkx_labels(initial_network, pos, labels = node_labels1)
        #node_labels2 = nx.get_node_attributes(initial_network,'Curso')
        #nx.draw_networkx_labels(initial_network, pos, labels = node_labels2)
        #node_labels3 = nx.get_node_attributes(initial_network,'Clase')
        #nx.draw_networkx_labels(initial_network, pos, labels = node_labels3)
        
        plt.show()
        
        
        nx.write_gexf(self.initial_network, "randomGraph.gexf")
        nx.write_gexf(self.initial_network, "randomGraphuploaded.gexf")
        nx.write_graphml(self.initial_network, "net.graphml")
        nx.write_graphml(self.initial_network, "netUploaded.graphml")
        
        
    def create_siblings_matrix(self):
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
        
        nombres = nx.get_node_attributes(self.initial_network,'Nombre')
        etapas = nx.get_node_attributes(self.initial_network,'Etapa')
        cursos = nx.get_node_attributes(self.initial_network,'Curso')
        clases = nx.get_node_attributes(self.initial_network,'Clase')
        
        for edge in self.siblings:
            for ed in edge:
                if ed not in siblings:
                    siblings.append(ed)
                    nombre_siblings.append(nombres[ed])
                    etapa_siblings.append(etapas[ed])
                    curso_siblings.append(cursos[ed])
                    clase_siblings.append(clases[ed])
                    
        for i in range(0,len(nombre_siblings)):
            self.siblingsMatrix.append([nombre_siblings[i],etapa_siblings[i],curso_siblings[i],clase_siblings[i]])
        #print('Es la matriz de hermanos')   
        #print(matriz_hermanos)
        
        data = {'nombre': nombre_siblings,
            'etapa': etapa_siblings,
            'curso' : curso_siblings,
            'clase': clase_siblings}
       
        df_siblings = pd.DataFrame(data, columns = ['nombre','etapa', 'curso', 'clase'])
        
        return df_siblings
    
    def create_schoolyear_class_network(self):
        """
        Creates the net of classes, where edges are siblings.

        Returns
        -------
        network
            Net of schoolYear-class.
        """
        initial = self.initial_network
        
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
        
            if node_name not in self.schoolyear_class.nodes():
                self.schoolyear_class.add_node(node_name)
                dicNombre[node_name] = node_name
                dicEtapa[node_name] = etapas[node]
                dicCurso[node_name] = cursos[node]
                dicClase[node_name] = clases[node]
                dicEstudiantes[node_name] = []    
                
        nx.set_node_attributes(self.schoolyear_class, dicNombre, 'Nombre')
        nx.set_node_attributes(self.schoolyear_class, dicEtapa, 'Etapa')
        nx.set_node_attributes(self.schoolyear_class, dicCurso, 'Curso')
        nx.set_node_attributes(self.schoolyear_class, dicClase, 'Clase')
        nx.set_node_attributes(self.schoolyear_class, dicEstudiantes, 'Estudiantes')
        
            
        for edge in self.siblings: 
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
            
            if (sibling1_name,sibling2_name) not in self.schoolyear_class.edges():
                self.schoolyear_class.add_edge(sibling1_name,sibling2_name)
                self.schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] = 0
            else:
                self.schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] += 1
        
            #print('peso del enlace', schoolyear_class.get_edge_data(sibling1_name, sibling2_name), (sibling1_name,sibling2_name))
        #print('enlaces de schoolyear_class')
        #print(schoolyear_class.edges(data=True))
        #print(len(schoolyear_class.edges()))
        #print(nx.get_node_attributes(schoolyear_class,'Estudiantes'))
        
        pos=nx.circular_layout(self.schoolyear_class)
        
        nx.draw(self.schoolyear_class, pos)
        node_labels = nx.get_node_attributes(self.schoolyear_class,'Nombre')
        nx.draw_networkx_labels(self.schoolyear_class, pos, labels = node_labels)
        edge_labels = nx.get_edge_attributes(self.schoolyear_class,'peso')
        nx.draw_networkx_edge_labels(self.schoolyear_class, pos, labels = edge_labels)
        print(type(self.schoolyear_class))
        
        plt.show()


#n = RandomNet()
#n.create_initial_network()
#dataframe = n.create_siblings_matrix()
#print(dataframe, n.siblings, n.siblingsMatrix)
#n.create_schoolyear_class_network()
#print(n.schoolyear_class.edges)