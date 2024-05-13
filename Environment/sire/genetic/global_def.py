import networkx as nx

stages = ['infantil', 'primaria', 'secundaria']
classrooms = ['A', 'B', 'C']

initial_network = nx.Graph()
siblings_dict = {}

total_students = 0
siblings_number = 0

graph_eval_ini = nx.Graph()