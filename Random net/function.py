from netCreation import RandomNet
import random
import networkx as nx
from math import e

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
    
    def generate_neighbor(self,matrix, net, numberSiblings):
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
            if len(dicEstudiantes[node_name_fin]) < numberSiblings:
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
    
    def solve(self, G_siblings):
        """
        Generates a solution

        Parameters
        ----------
        G_siblings : net
            net of schoolyear_class, edges are siblings
            
        Returns
        --------
        total: int
            the solution
        """
        total = 0
        for component in nx.connected_components(G_siblings):
            total += (len(component)**2)
        
        return total
    
    def solve_simulated_annealing(self, G, matrix, siblings):
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
        """
        tf = random.uniform(0.05, 0.01)
        alpha = random.uniform(0.8, 0.99)
        l = random.randint(10,50)
        t = self.solve(G) * 0.4
        current_solution = G
        
        ini_fmax = self.solve(G)
        
        while t >= tf:
            for i in range(l):
                candidate_solution = self.generate_neighbor(matrix,current_solution, siblings)
                
                candidate_fmax = self.solve(candidate_solution)
                current_fmax = self.solve(current_solution)
                diff = candidate_fmax - current_fmax
                
                if candidate_fmax < current_fmax or random.random() < e**(-diff/t):
                    current_solution = candidate_solution
                    
            t = alpha * t
            
        print('\n****************************')
        print('VECINO INICIAL -')
        print(G.edges)
        print('Fmax -', ini_fmax)    
        print('\n****************************')
        print('MEJOR VECINO ENCONTRADO -')
        print(current_solution.edges)
        print('Fmax -', current_fmax)

n = RandomNet()
n.create_initial_network()
n.create_schoolyear_class_network()
n.create_siblings_matrix()
s = SimulatedAnnealing()
s.solve_simulated_annealing(n.schoolyear_class,n.siblingsMatrix,n.numberSiblings)