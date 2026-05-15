import json
from datastructures import Graph, Node, Edge

def load_graph(filepath: str) -> Graph:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    graph = Graph()

    # Load stations
    for st in data.get('stations', []):
        node = Node(
            node_id=st['id'],
            name=st['name'],
            line=st['line'],
            x=st.get('x', 0.0),
            y=st.get('y', 0.0)
        )
        graph.add_node(node)

    # Load connections
    for conn in data.get('connections', []):
        edge = Edge(
            from_node=conn['from'],
            to_node=conn['to'],
            time=conn['time'],
            distance=conn['distance'],
            cost=conn['cost']
        )
        # Assuming all physical transport connections are undirected (two-way)
        graph.add_edge(edge, directed=False)

    return graph
