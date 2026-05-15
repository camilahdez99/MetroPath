from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time
import os

# Reuse existing logic
from dataloader import load_graph
from algorithms import dijkstra, a_star, bfs

app = FastAPI()

# Global graph instance
GRAPH_PATH = "data.json"
graph = load_graph(GRAPH_PATH)

class RouteRequest(BaseModel):
    start: str
    end: str
    criteria: str

@app.get("/api/stations")
async def get_stations():
    stations = []
    for node_id in graph.get_all_nodes():
        node = graph.get_node(node_id)
        stations.append({
            "id": node.id,
            "name": node.name,
            "line": node.line,
            "x": node.x,
            "y": node.y
        })
    return stations

@app.get("/api/graph")
async def get_graph():
    # Load raw JSON to get connections as well
    import json
    with open(GRAPH_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.post("/api/route")
async def calculate_route(request: RouteRequest):
    if request.start not in graph.nodes or request.end not in graph.nodes:
        raise HTTPException(status_code=400, detail="Invalid stations")

    # Metrics for Dijkstra
    t0 = time.perf_counter()
    d_path, d_cost, d_nodes = dijkstra(graph, request.start, request.end, request.criteria)
    d_time = (time.perf_counter() - t0) * 1000

    # Metrics for A*
    t0 = time.perf_counter()
    a_path, a_cost, a_nodes = a_star(graph, request.start, request.end, request.criteria)
    a_time = (time.perf_counter() - t0) * 1000

    return {
        "path": a_path,  # Use A* path as primary
        "cost": a_cost,
        "criteria": request.criteria,
        "comparison": {
            "dijkstra": {"time_ms": d_time, "nodes": d_nodes},
            "a_star": {"time_ms": a_time, "nodes": a_nodes}
        }
    }

# Mount static files
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
