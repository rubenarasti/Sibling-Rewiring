import networkx as nx

class FileNet:
    """
    Class FileNet
    
    A class to create the schoolyear_Class net.
    
    create_schoolyear_class_network
        Creates the schoolyear-class
    """
    
    def __init__(self, siblings_df, initial_network):
        """
        Parameters
        ----------
        totalStudents : int
            Total number of Students
        numberSiblings : int
            Number of couples of siblings
        """
        self.df_siblings = siblings_df
        self.initial_network = nx.Graph()
        self.initial_network = initial_network
        self.siblings = self.df_siblings.values
        self.schoolyear_class = nx.Graph()
  
    
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
        
            
        for sib in self.siblings: 
            sibling = []
            sibling.append(etapas[str(sib[0])])
            sibling.append(cursos[str(sib[0])])
            sibling.append(clases[str(sib[0])])
            sibling1_name = ''.join(str(e) for e in sibling)
            if sib[0] not in dicEstudiantes[sibling1_name]:
                dicEstudiantes[sibling1_name].append(sib[0])
            
            
            sibling2 = []
            sibling2.append(etapas[str(sib[4])])
            sibling2.append(cursos[str(sib[4])])
            sibling2.append(clases[str(sib[4])])
            sibling2_name = ''.join(str(e) for e in sibling2)
            if sib[4] not in dicEstudiantes[sibling2_name]:
                dicEstudiantes[sibling2_name].append(sib[4])
                
            if (sibling1_name,sibling2_name) not in self.schoolyear_class.edges():
                self.schoolyear_class.add_edge(sibling1_name,sibling2_name)
                self.schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] = 0
            else:
                self.schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] += 1
            
            
        return self.schoolyear_class
        
        

