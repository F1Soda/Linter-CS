import networkx as nx

# Создаем направленный граф
G = nx.DiGraph()

# Добавляем узлы
G.add_node(1)
G.add_node(2)

# Добавляем ребра с условиями
G.add_edge(1, 2, condition=True)

# Выводим данные ребер
print(G.edges(data=True))

# Выводим атрибуты ребра между вершинами 1 и 2
print(G.get_edge_data(1, 2))