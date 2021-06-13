import networkx as nx


def create_schoolyear_class_network(siblings_df, initial_network):
	"""
	Creates the net of classes, where edges are siblings.

	Returns
	-------
	network
		Net of schoolYear-class.
	"""
	initial = initial_network
	df_siblings = siblings_df
	siblings = df_siblings.values
	
	dicNombre = {}
	dicEtapa = {}
	dicCurso = {}
	dicClase = {}
	dicEstudiantes = {}
	etapas = nx.get_node_attributes(initial,'Etapa')
	clases = nx.get_node_attributes(initial,'Clase')
	cursos = nx.get_node_attributes(initial,'Curso')
	
	for node in initial.nodes():
		name = []
		name.append(etapas[node])
		name.append(cursos[node])
		name.append(clases[node])
		node_name = ''.join(str(e) for e in name)
	
		if node_name not in schoolyear_class.nodes():
			schoolyear_class.add_node(node_name)
			dicNombre[node_name] = node_name
			dicEtapa[node_name] = etapas[node]
			dicCurso[node_name] = cursos[node]
			dicClase[node_name] = clases[node]
			dicEstudiantes[node_name] = []    
			
	nx.set_node_attributes(schoolyear_class, dicNombre, 'Nombre')
	nx.set_node_attributes(schoolyear_class, dicEtapa, 'Etapa')
	nx.set_node_attributes(schoolyear_class, dicCurso, 'Curso')
	nx.set_node_attributes(schoolyear_class, dicClase, 'Clase')
	nx.set_node_attributes(schoolyear_class, dicEstudiantes, 'Estudiantes')
	
		
	for sib in self.siblings: 
		sibling = []
		sibling.append(etapas[str(sib[0])])
		sibling.append(cursos[str(sib[0])])
		sibling.append(clases[str(sib[0])])
		sibling1_name = ''.join(str(e) for e in sibling)
		if sib[0] not in dicEstudiantes[sibling1_name]:
			dicEstudiantes[sibling1_name].append(sib[0])
		
		
		sibling2 = []
		sibling2.append(etapas[str(sib[4])])
		sibling2.append(cursos[str(sib[4])])
		sibling2.append(clases[str(sib[4])])
		sibling2_name = ''.join(str(e) for e in sibling2)
		if sib[4] not in dicEstudiantes[sibling2_name]:
			dicEstudiantes[sibling2_name].append(sib[4])
			
		if (sibling1_name,sibling2_name) not in schoolyear_class.edges():
			schoolyear_class.add_edge(sibling1_name,sibling2_name)
			schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] = 0
		else:
			schoolyear_class.edges[sibling1_name, sibling2_name]["peso"] += 1
		
		
	return schoolyear_class
	
	

