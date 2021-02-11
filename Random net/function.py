import random
import networkx as nx
from math import e
import numpy as np
from netCreation import RandomNet

class SimulatedAnnealing:
    """
    Class SimulatedAnnealing

    A class used to solve SimulatedAnnealing. 

    Methods
    -------
    generate_neighbor(matrix, net)
        Generates a new net changing one of the edges
    solve(net)
        Generates a solution based of the introduced net
    solve_simulated_annealing(net, matrix)
        Solves the Flow Shop problem with simulated annealing
    """
    
    def generate_neighbor(self,matrix, net_to_change, numberSiblings):
        """
        Generates a net changing one of the edges

        Parameters
        ----------
        matrix : matrix
            matrix of siblings
        net : net
            net of schoolyear_class
        numberSiblings : int
            number of siblings
        
        Returns
        --------
        net: net
            the new net after changing
        """
        
        net = nx.Graph()
        net = net_to_change.copy()
        clases = nx.get_node_attributes(net,'Clase')
        
        clase = np.unique(list((clases.values())))
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
            if len(dicEstudiantes[node_name_fin]) < numberSiblings:
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
            
        return net
    
    def solve(self, G_siblings, percentage_component, percentage_individual, totalStudents):
        """
        Generates a solution

        Parameters
        ----------
        G_siblings : net
            net of schoolyear_class, edges are siblings
        percentage_component: int
            probability of component infection
        percentage_individual: int
            probability of student's infection
        totalStudents : int
            total number of students
        Returns
        --------
        total: int
            the solution
        """
        total_component = 0
        for component in nx.connected_components(G_siblings):
            total_component += (len(component)**2)
            
        total_individual = 0
        individual = []
        dicEstudents = nx.get_node_attributes(G_siblings, 'Estudiantes')
        for component in nx.connected_components(G_siblings):
            for node in component:
                individual.append((len(dicEstudents[node])/totalStudents)*len(component))
        indv = np.array(individual)
        total_individual = indv.var()
        
        total = (percentage_component*0.1)*total_component + (percentage_individual*0.1)*total_individual
        
        return total
    
    def solve_simulated_annealing(self, G, matrix, siblings, totalStudents,alpha, l, tf):
        """
        Generates the solution

        Parameters
        ----------
        G : net
            net of schoolyear_class
        matrix : matrix
            matrix of siblings
        siblings : int
            number of siblings
        totalStudents : int
            totalNumber of nodes of initial network
        """
        print('\t\t Selección de porcentajes para las métricas')
        print('***************************************************************')
        print('\t1 - Seleccionados por usuario')
        print('\t2 - Por defecto')
        option = input('Selecciona una opción: ')
        
        if option == "1":
            print('Se va a pedir la importancia que tiene la probabilidad de contagio por componente, el resto será la probabilidad individual')
            percentage_component = int(input('Introduce el peso que deseas darle a la probabilidad por componente [0-100]: '))
            if percentage_component < 0 or percentage_component >100:
                print('El valor introducido no se encuentra entre los valores establecidos')
                print('Se dará un valor por defecto')
                percentage_component = 60
            percentage_individual = 100 - percentage_component
        elif option != "1":
            print('\tSe toman valores por defecto')
            percentage_component = 60
            percentage_individual =  40
            
        t = self.solve(G, percentage_component, percentage_individual, totalStudents) * 0.4
        current_solution = G
        
        ini_fmax = self.solve(G, percentage_component, percentage_individual, totalStudents)
        
        while t >= tf:
            for i in range(l):
                candidate_solution = self.generate_neighbor(matrix,current_solution, siblings)
                
                candidate_fmax = self.solve(candidate_solution, percentage_component, percentage_individual, totalStudents)
                current_fmax = self.solve(current_solution, percentage_component, percentage_individual, totalStudents)
                diff = candidate_fmax - current_fmax
                ranm = (random.random())
                div =  e**(-diff/t)
                num = ranm < div
                ##########################################################
                #print(diff, ranm, div, num)
                if candidate_fmax < current_fmax or num:
                    current_solution = candidate_solution
                    #print('cambia')
                    
            t = alpha * t
            
        print('\n****************************')
        print('VECINO INICIAL -')
        print(G.edges)
        print('Fmax -', ini_fmax)    
        print('\n****************************')
        print('MEJOR VECINO ENCONTRADO -')
        print(current_solution.edges)
        print('Fmax -', current_fmax)