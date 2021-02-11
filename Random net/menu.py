import os
from netCreation import RandomNet
from function import SimulatedAnnealing
import platform
import random

class Menu:
    """
    Displays a menu.

    Methods
    -------
    display_menu()
        Displays a menu with all the available options
    print_menu()
        Prints the menu
    clear()
        Cleans the terminal
    """
    
    def display_menu(self):
        """
        Displays a menu to select defect values or user ones
        """
        
        option = None
        it = 0
        while option != "0":
            if it == 0:
                print('Se procede a la creación de la red')
                net = RandomNet()
                net.create_initial_network()
                net.create_schoolyear_class_network()
                net.create_siblings_matrix()
                simAn = SimulatedAnnealing()
            
            self.print_menu()
            option = input('Selecciona una opción: ')
            
            if option == "1":
                print('Se procede a introducir los valores necesarios para resolver el recocido simulado\n')
                
                alpha = float(input('\nIntroduce un valor para Alpha (entre 0.8 y 0.99): '))
                if alpha < 0.8 or alpha > 0.99:
                    print('El valor no estaba entre los permitidos, se escoge valor por defecto')
                    alpha = random.uniform(0.8, 0.99)
                l = int(input('Introduce un valor para L (numero entero positivo): '))
                if l < 0:
                    print('El valor no es entero positivo, se escoge uno por defecto')
                    l = random.randint(10,50)
                tf = float(input('Introduce un valor para Tf (no puede ser 0): '))
                if tf == 0:
                    print('El valor introducido es 0, se escoge uno por defecto')
                    tf = random.uniform(0.05, 0.01)
                simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents, alpha,l,tf)
            
            elif option == "2":
                tf = random.uniform(0.05, 0.01)
                alpha = random.uniform(0.8, 0.99)
                l = random.randint(10,50)
                simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents, alpha,l,tf)
            
            elif option != "0":
                print('ERROR, esa opción no existe!')

            if option != "0":
                input('\nPulsa cualquier tecla para volver al menú...')
            
            it += 1

    def print_menu(self):
        """
        Prints the menu
        """
        self.clear()
        print('\t\t MENU')
        print('******************************************')
        print('\t 1- Opciones avanzadas')
        print('\t 2- Valores por defecto')
        print('\t 0- Salir del programa\n')

    
    def clear(self):
        """
        Cleans the terminal
        """
        system = platform.system()
        if system == 'Windows':
            os.system('cls')
        elif system == 'Linux':
            os.system('clear')
        