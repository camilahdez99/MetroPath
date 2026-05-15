import heapq
import math
from datastructures import Graph

def dijkstra(graph: Graph, start_id: str, end_id: str, criteria: str):
    queue = []
    heapq.heappush(queue, (0, start_id))
    distances = {node_id: float('inf') for node_id in graph.get_all_nodes()}
    distances[start_id] = 0
    previous = {node_id: None for node_id in graph.get_all_nodes()}
    nodes_visited = 0

    while queue:
        current_distance, current_id = heapq.heappop(queue)
        nodes_visited += 1

        if current_id == end_id:
            break

        if current_distance > distances[current_id]:
            continue

        for edge in graph.get_neighbors(current_id):
            weight = edge.get_weight(criteria)
            distance = current_distance + weight

            if distance < distances[edge.to_node]:
                distances[edge.to_node] = distance
                previous[edge.to_node] = current_id
                heapq.heappush(queue, (distance, edge.to_node))

    return _reconstruct_path(previous, end_id), distances[end_id], nodes_visited

def heuristic(node_a, node_b, criteria):
    dx = node_a.x - node_b.x
    dy = node_a.y - node_b.y
    dist = math.sqrt(dx**2 + dy**2)
    
    if criteria == "distance":
        return dist
    elif criteria == "time":
        # Assume an average speed to convert distance to time (e.g. 1 unit of distance ~= 1 unit of time)
        return dist * 0.8
    return 0  # For cost or other criteria, fallback to 0 (acts as Dijkstra)

def a_star(graph: Graph, start_id: str, end_id: str, criteria: str):
    queue = []
    heapq.heappush(queue, (0, start_id))
    g_scores = {node_id: float('inf') for node_id in graph.get_all_nodes()}
    g_scores[start_id] = 0
    f_scores = {node_id: float('inf') for node_id in graph.get_all_nodes()}
    
    start_node = graph.get_node(start_id)
    end_node = graph.get_node(end_id)
    f_scores[start_id] = heuristic(start_node, end_node, criteria)
    
    previous = {node_id: None for node_id in graph.get_all_nodes()}
    nodes_visited = 0

    while queue:
        current_f, current_id = heapq.heappop(queue)
        nodes_visited += 1

        if current_id == end_id:
            break

        current_node = graph.get_node(current_id)

        for edge in graph.get_neighbors(current_id):
            weight = edge.get_weight(criteria)
            tentative_g = g_scores[current_id] + weight

            if tentative_g < g_scores[edge.to_node]:
                previous[edge.to_node] = current_id
                g_scores[edge.to_node] = tentative_g
                neighbor_node = graph.get_node(edge.to_node)
                f_score = tentative_g + heuristic(neighbor_node, end_node, criteria)
                f_scores[edge.to_node] = f_score
                heapq.heappush(queue, (f_score, edge.to_node))

    return _reconstruct_path(previous, end_id), g_scores[end_id], nodes_visited

def bfs(graph: Graph, start_id: str, end_id: str):
    queue = [start_id]
    visited = {start_id}
    previous = {node_id: None for node_id in graph.get_all_nodes()}
    nodes_visited = 0

    while queue:
        current_id = queue.pop(0)
        nodes_visited += 1

        if current_id == end_id:
            break

        for edge in graph.get_neighbors(current_id):
            if edge.to_node not in visited:
                visited.add(edge.to_node)
                previous[edge.to_node] = current_id
                queue.append(edge.to_node)

    path = _reconstruct_path(previous, end_id)
    # The "cost" here is number of transfers/edges (len(path) - 1)
    cost = len(path) - 1 if path else float('inf')
    return path, cost, nodes_visited

def connected_components(graph: Graph):
    visited = set()
    components = []
    
    for node_id in graph.get_all_nodes():
        if node_id not in visited:
            component = []
            queue = [node_id]
            visited.add(node_id)
            
            while queue:
                current = queue.pop(0)
                component.append(current)
                for edge in graph.get_neighbors(current):
                    if edge.to_node not in visited:
                        visited.add(edge.to_node)
                        queue.append(edge.to_node)
            components.append(component)
            
    return components

def _reconstruct_path(previous, end_id):
    path = []
    current = end_id
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path if path[0] != end_id or len(path) > 1 else []
