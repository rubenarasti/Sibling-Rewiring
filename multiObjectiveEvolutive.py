from deap import base, creator
from deap import tools
from deap import algorithms
import random
import randomNetCreation as rN
import function as fn

def configurePopulation(toolbox):
    
	''' Al configurar el fitness que se va a emplear, se configuraría para:
		1. buscar un objetivo único
		2. Minimizar tanto el riesgo individual como el colectivo '''
	print('Entra a la población')
	creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0))
    
	creator.create("Individual", list, fitness=creator.FitnessMin)
	print('Entra a la network')
	toolbox.register("network", rN.generate_similar_net())
	print('acaba')
	''' El individuo se crea como una lista (o repeticion) de "network", definido justo antes
	Tendrá una longitud igual al numero deseado'''
	toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.network)
	print('Entra a la population') 
	''' La población se crea como una lista de "individual", definido justo antes'''
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluation(individual):
	totalStudents = rN.__initial_network.nodes()
	percentage_component = 0.5
	percentage_individual = 0.5
	score = fn.solve(individual, percentage_component, percentage_individual, totalStudents)
	
	return score, totalStudents

def configureAlgorithm(toolbox):
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)
    toolbox.register("select", tools.selSPEA2)
    
    toolbox.register("evaluate", evaluation)
    
    
def doEvolution (toolbox, stats):
	configurePopulation(toolbox)
	configureAlgorithm(toolbox)
	population = toolbox.population(n=50)
	population, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=150,lambda_=100, cxpb=0.5, mutpb=0.2, ngen=50, verbose=False, stats=stats)
	
	print("\nEl resultado de la evolución es: ")
	print(logbook,"\n")

	print("\nLa mejor solucion encontrada es: ")
	print(tools.selBest(population,1)[0])
    
	return logbook, tools.selBest(population,1)[0], population

rN.create_initial_network(100,5)
schoolyear_class = rN.create_schoolyear_class_network()
rN.create_siblings_matrix()
toolbox = base.Toolbox()
doEvolution(toolbox, None)