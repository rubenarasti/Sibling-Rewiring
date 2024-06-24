import networkx as nx

classrooms = [] # Groups
capacity = 0

initial_network = nx.Graph()
siblings_dict = {}

total_students = 0
siblings_number = 0 # pairs of siblings

graph_eval_ini = nx.Graph()