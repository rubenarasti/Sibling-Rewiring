import random
import networkx as nx
from math import e, log
import numpy as np

class SimulatedAnnealing:
    """
    Class SimulatedAnnealing

    A class used to solve SimulatedAnnealing. 

    Methods
    -------
    generate_neighbor(matrix, net, int)
        Generates a new net changing one of the edges
    solve(net, int, int, int)
        Generates a solution based of the introduced net
    solve_simulated_annealing(net, matrix, int, int, float, int, float)
        Solves the Flow Shop problem with simulated annealing
    """
    
    def generate_neighbor(self,matrix, net_to_change, numberSiblings, seed_value):
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
        seed_value : int
            seed value
        
        Returns
        --------
        net: net
            the new net after changing
        """
        
        random.seed(seed_value)
        net = nx.Graph()
        net = net_to_change.copy()
        clases = nx.get_node_attributes(net,'Clase')
        
        clase = np.unique(list((clases.values())))
        pos = random.randint(0,(len(matrix)-1))
        sibling_to_change = matrix[pos]
        edges_to_remove = []
        clase_to_change = list(clase[:])
        
        sibling_name = sibling_to_change[0]
            
        name = []
        name.append(sibling_to_change[1])
        name.append(sibling_to_change[2])
        name.append(sibling_to_change[3])
        node_name_ini = ''.join(str(e) for e in name)
        
        clase_to_change.remove(sibling_to_change[3])
        
        new_class = random.choice(clase_to_change)
        matrix[pos][3] = new_class
            
        name = []
        name.append(sibling_to_change[1])
        name.append(sibling_to_change[2])
        name.append(sibling_to_change[3])
        node_name_fin = ''.join(str(e) for e in name)
            
        dicEstudiantes = nx.get_node_attributes(net,'Estudiantes')
         
       
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
    
    def linear_cooling_sequence(self, t, it):
        """
        Calculates the new temperature per iteration using a linear function.

        Parameters
        ----------
        t : float
            temperature actual
        it: int
            actual iteration
        Returns
        --------
        tt: float
            new temperature
        """
        beta = random.uniform(0.8, 0.99)
        tt = t - it * beta 
        return tt
    
    def geometrical_cooling_sequence(self, alpha, t):
        """
        Calculates the new temperature per iteration using a geometrical function.

        Parameters
        ----------
        alpha : float
            contains the value of alpha
        t: float
            actual temperature
        Returns
        --------
        tt: float
            new temperature
        """
        tt = t* alpha
        return tt
    
    def  logarithmic_cooling_sequence(self, initial_t, it, alpha):
        """
        Calculates the new temperature per iteration using a logarithmic function.

        Parameters
        ----------
        initial_t : float
            initial temperature
        it: int
            actual iteration
        Returns
        --------
        tt: float
            new temperature
        """
        tt = initial_t/(1+(alpha*log(1+it)))
        return tt
    
    def cauchy_cooling_sequence(self,initial_t, it):
        """
        Calculates the new temperature per iteration using a cauchy progression.

        Parameters
        ----------
        initial_t : float
            initial temperature
        it: int
            actual iteration
        Returns
        --------
        tt: float
            new temperature
        """
        tt  = initial_t/(1+it)
        return tt
    
    def modified_cauchy_cooling_sequence(self, initial_t, tf, l, t):
        """
        Calculates the new temperature per iteration using a modified cauchy progression.

        Parameters
        ----------
        initial_t : float
            initial temperature
        tf: float
            final temperature
        l: int
            number of iterations
        t: float
            actual temperature
        Returns
        --------
        tt: float
            new temperature
        """
        betha = initial_t - tf/(l-1)*initial_t*tf
        tt = t/(1+betha*t)
        return tt
    
        
    def solve_simulated_annealing(self, G, matrix, siblings, totalStudents, l, tf, alpha, option_cooling, seed_value, percentage_component):
        """
        Generates the solution based on basic algorithm (uses Boltzmann probability)

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
        l : int
            total number of iterations
        tf : float
            final temperature
        alpha : float 
            if needed values to solve the cooling sequence
        option_cooling : int
            option to choose cooling sequence
        seed_value : int
            seed value
        percentage_component: int
            percentage to solve
        """
        random.seed(seed_value)
      
        
        percentage_individual =  100 - percentage_component
        
        initial_t = self.solve(G, percentage_component, percentage_individual, totalStudents) * 0.4
        t = initial_t
        current_solution = G
        it = 0
        ini_fmax = self.solve(G, percentage_component, percentage_individual, totalStudents)
        
        while t >= tf:
            for i in range(l):
                candidate_solution = self.generate_neighbor(matrix,current_solution, siblings, seed_value)
                
                candidate_fmax = self.solve(candidate_solution, percentage_component, percentage_individual, totalStudents)
                current_fmax = self.solve(current_solution, percentage_component, percentage_individual, totalStudents)
                diff = candidate_fmax - current_fmax
                
                if candidate_fmax < current_fmax or random.random() < e**(-diff/t):
                    current_solution = candidate_solution
                    
            if option_cooling == 1:        
                t = self.linear_cooling_sequence(t, it)
            elif option_cooling == 3:
                t = self.logarithmic_cooling_sequence(initial_t, it, alpha)
            elif option_cooling == 4:
                t = self.cauchy_cooling_sequence(initial_t, it)
            elif option_cooling == 5:
                t = self.modified_cauchy_cooling_sequence(initial_t, tf, l, t)
            elif option_cooling == 6:
                
                t = self.geometrical_cooling_sequence(alpha, t)
            
            it+=1
        
        initial_neighbour = G.edges
        best_neighbour = current_solution.edges
        
        return initial_t, initial_neighbour, ini_fmax, best_neighbour, current_fmax
        