from deap import base, creator
from deap import tools
from deap import algorithms
import random
import randomNetCreation as rN

def configurePopulation(toolbox):
    
    ''' Al configurar el fitness que se va a emplear, se configuraría para:
        1. buscar un objetivo único
        2. Minimizar tanto el riesgo individual como el colectivo '''
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0))
        
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    toolbox.register("network", random.randint, 0,rN.generate_similar_net() )
    
    ''' El individuo se crea como una lista (o repeticion) de "network", definido justo antes
	Tendrá una longitud igual al numero deseado'''
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.network, n=50)
     
    ''' La población se crea como una lista de "individual", definido justo antes'''
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def configureAlgorithm(toolbox):
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)
    toolbox.register("select", tools.selSPEA2)
    
    toolbox.register("evaluate", evaluation)
    
    
def doEvolution (toolbox, stats):
    configurePopulation(toolbox)
    
    configureAlgorithm(toolbox)
    
    population = toolbox.population(n=300)
    
    population, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=150,
                                                    lambda_=100, cxpb=0.5, mutpb=0.2,
                                                    ngen=50, verbose=False, stats=stats)
    
    return logbook, tools.selBest(population,1)[0], population


toolbox = base.Toolbox()
configurePopulation(toolbox)