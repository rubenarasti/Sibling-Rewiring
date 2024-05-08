import networkx as nx

stage = ['infantil', 'primaria', 'secundaria']
classroom = ['A', 'B', 'C']

initial_network = nx.Graph()
siblings_matrix = []

total_students = 0
siblings_number = 0

percentage_component = 0
percentage_individual = 0

graph_eval_ini = nx.Graph()