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
        seed_value = random.randint(0,10)
        
        
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
            values = []
            if option == "1":
                print('Se procede a introducir los valores necesarios para resolver el recocido simulado\n')
                l = int(input('Introduce un valor para L (numero entero positivo): '))
                if l < 0:
                    print('El valor no es entero positivo, se escoge uno por defecto')
                    l = random.randint(10,50)
                tf = float(input('Introduce un valor para Tf (no puede ser 0): '))
                if tf == 0:
                    print('El valor introducido es 0, se escoge uno por defecto')
                    tf = random.uniform(0.05, 0.01)
                
                self.print_menu_cooling()
                option_cooling = input('Introduce el valor de la secuencia escogida :')
                
                if option_cooling == "1":
                    print('Se va a usar una secuencia de enfriaminto lineal\n')
                    simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents, l,tf, values,int(option_cooling), seed_value)
                elif option_cooling == "2":
                    print('Se va a usar una secuencia de enfriaminto geometrico\n')
                    print('\t\t Selección del parámetro alpha')
                    print('\t*********************************************')
                    print('\t 1- Opciones avanzadas')
                    print('\t 2- Valores por defecto\n')
                    option = (input('\t Selecciona una opción: '))
                    if option == "1":
                        alpha =  alpha = float(input('\t * Introduce un valor para Alpha (entre 0.8 y 0.99): '))
                        if alpha < 0.8 or alpha > 0.99:
                            print('El valor no estaba entre los permitidos, se escoge valor por defecto')
                            alpha = random.uniform(0.8, 0.99)
                    else:
                        alpha = random.uniform(0.8, 0.99)
                        print('\t Se toma la opción por defecto, alpha = ', alpha)
                    option_cooling = 6
                    values.append(alpha)
                    simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents,l,tf, values,int(option_cooling), seed_value)
                elif option_cooling == "3":
                    print('Se va a usar una secuencia de enfriaminto logaritmica\n')
                    print('\t\t Selección del parámetro alpha')
                    print('\t\t*********************************************')
                    print('\t 1- Opciones avanzadas')
                    print('\t 2- Valores por defecto\n')
                    option = (input('\t Selecciona una opción: '))
                    if option == "1":
                        alpha = int(input('\t Introduce el valor para alpha (mayor de 1): '))
                        if alpha <1:
                            print('\t Se ha seleccionado un valor erróneo. Se usa alpha = ', alpha)
                            alpha = 20
                    else:
                        alpha = 20
                        print('\t Se toma la opción por defecto, alpha = ', alpha)
                    values.append(alpha)
                    simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents, l,tf, values,int(option_cooling), seed_value)
                elif option_cooling == "4":
                    print('Se ha seleccionado la secuencia de enfriamiento de Cauchy\n')
                    simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents, l,tf, values,int(option_cooling), seed_value)
                elif option_cooling == "5":
                    print('Se ha seleccionado la secuncia de enfriamiento de Cauchy modificado\n')
                    simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents, l,tf, values,int(option_cooling), seed_value)
                else:
                    option_cooling = 6
                    print('Se ha usado la secuencia de enfriamiento  por defecto, que es la logaritmica\n')
                    alpha = random.uniform(0.8, 0.99)
                    values.append(alpha)
                    simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents, l,tf, values,int(option_cooling), seed_value)
            elif option == "2":
                tf = random.uniform(0.05, 0.01)
                alpha = random.uniform(0.8, 0.99)
                l = random.randint(10,50)
                values.append(alpha)
                option_cooling = 6
                simAn.solve_simulated_annealing(net.schoolyear_class,net.siblingsMatrix,net.numberSiblings,net.totalStudents,l,tf, values,int(option_cooling), seed_value)
            
            elif option != "0":
                print('ERROR, esa opción no existe!')

            if option != "0":
                input('\nPulsa cualquier tecla para volver al menú...')
            
            it += 1

    def print_menu(self):
        """
        Prints the initial menu
        """
        self.clear()
        print('\t\t MENU')
        print('******************************************')
        print('\t 1- Opciones avanzadas (se podrá escoger también la secuencia de enfriamiento)')
        print('\t 2- Valores por defecto')
        print('\t 0- Salir del programa\n')

    
    def print_menu_cooling(self):
        """
        Prints the initial menu
        """
        self.clear()
        print('\t\t MENU PARA ESCOGER LA SECUENCIA DE ENFRIAMIENTO')
        print('****************************************************************')
        print('\t 1- Secuencia de enfriamiento Lineal ')
        print('\t 2- Secuencia de enfriamiento Geometrica')
        print('\t 3- Secuencia de enfriamiento Logarítimica')
        print('\t 4- Secuencia de enfriamiento de Cauchy')
        print('\t 5- Secuencia de enfriamiento de Cauchy modificado')
        print('\t 6- Se ecoge una secuencia de enfriamiento por defecto\n')
        
        
    def clear(self):
        """
        Cleans the terminal
        """
        system = platform.system()
        if system == 'Windows':
            os.system('cls')
        elif system == 'Linux':
            os.system('clear')
        