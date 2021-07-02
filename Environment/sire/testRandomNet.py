import networkx as nx

def test_same_graph_graphml():
        
    f1 = nx.read_graphml("net.graphml")
    f2 = nx.read_graphml("../Environment/sire/uploads/netUploaded.graphml")
    
    edges1 = f1.edges()
    edges2 = f2.edges()
    
    
    nodes1 = f1.nodes()
    nodes2 = f2.nodes()
    
    assert (nx.get_node_attributes(f1,'Nombre')) == (nx.get_node_attributes(f2,'Nombre')), "Los nodos no tienen los mismos nombres"
    assert (nx.get_node_attributes(f1,'Etapa')) == (nx.get_node_attributes(f2,'Etapa')), "No se corresponden las etapas"
    assert (nx.get_node_attributes(f1,'Curso')) == (nx.get_node_attributes(f2,'Curso')), "No se corresponden los cursos"
    assert (nx.get_node_attributes(f1,'Clase')) == (nx.get_node_attributes(f2,'Clase')), "No se correspondn las clases"
    assert (len([i for i, j in zip(edges1, edges2) if i == j])) == len(edges1) == len(edges2), "El número de vértices ha cambiado"
    assert (len([i for i, j in zip(nodes1, nodes2) if i == j])) == len(nodes1) == len(nodes2), "El número de nodos ha cambiado"

def test_same_graph_gexf():
        
    f1 = nx.read_gexf("randomGraphuploaded.gexf")
    f2 = nx.read_gexf("../Environment/sire/uploads/randomGraph.gexf")
    
    edges1 = f1.edges()
    edges2 = f2.edges()
    
    
    nodes1 = f1.nodes()
    nodes2 = f2.nodes()
    
    assert (nx.get_node_attributes(f1,'Nombre')) == (nx.get_node_attributes(f2,'Nombre')), "Los nodos no tienen los mismos nombres"
    assert (nx.get_node_attributes(f1,'Etapa')) == (nx.get_node_attributes(f2,'Etapa')), "No se corresponden las etapas"
    assert (nx.get_node_attributes(f1,'Curso')) == (nx.get_node_attributes(f2,'Curso')), "No se corresponden los cursos"
    assert (nx.get_node_attributes(f1,'Clase')) == (nx.get_node_attributes(f2,'Clase')), "No se correspondn las clases"
    assert (len([i for i, j in zip(edges1, edges2) if i == j])) == len(edges1) == len(edges2), "El número de vértices ha cambiado"
    assert (len([i for i, j in zip(nodes1, nodes2) if i == j])) == len(nodes1) == len(nodes2), "El número de nodos ha cambiado"
        

if __name__ == "__main__":
    test_same_graph_graphml()
    test_same_graph_gexf
    print("Graphs are exactly the same.")