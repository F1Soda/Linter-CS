import networkx as nx

# Создание графа
G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(2, 3)


def direct_successors(graph, node):
	descendants = list(graph.successors(node))
	direct_successors = [n for n in descendants if graph.has_edge(node, n)]
	return direct_successors


print(direct_successors(G, 3))  # Выведет [3]


def check_tokens_by_graph(graph: nx.DiGraph):
	index_node = 0
	while index_node < len(graph.nodes):
		neighbors = list(direct_successors(graph, index_node))
		print(index_node, neighbors)

		index_node += 1


graph = nx.convert_node_labels_to_integers(nx.read_gml("Graphs/DiGraph.gml"))
print(graph.is_directed())
check_tokens_by_graph(graph)
