class Node:
    def __init__(self, node_id: str, name: str, line: str, x: float, y: float):
        self.id = node_id
        self.name = name
        self.line = line
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Node({self.name})"

class Edge:
    def __init__(self, from_node: str, to_node: str, time: float, distance: float, cost: float):
        self.from_node = from_node
        self.to_node = to_node
        self.time = time
        self.distance = distance
        self.cost = cost

    def get_weight(self, criteria: str) -> float:
        if criteria == "time":
            return self.time
        elif criteria == "distance":
            return self.distance
        elif criteria == "cost":
            return self.cost
        return 1.0  # Default for BFS

class Graph:
    def __init__(self):
        self.nodes = {}  # id -> Node
        self.edges = {}  # id -> list[Edge]

    def add_node(self, node: Node):
        self.nodes[node.id] = node
        if node.id not in self.edges:
            self.edges[node.id] = []

    def add_edge(self, edge: Edge, directed: bool = False):
        if edge.from_node in self.edges:
            self.edges[edge.from_node].append(edge)
        if not directed:
            reverse_edge = Edge(edge.to_node, edge.from_node, edge.time, edge.distance, edge.cost)
            if edge.to_node in self.edges:
                self.edges[edge.to_node].append(reverse_edge)

    def get_node(self, node_id: str) -> Node:
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str):
        return self.edges.get(node_id, [])

    def get_all_nodes(self):
        return list(self.nodes.keys())
