import time
import sys
from dataloader import load_graph
from algorithms import dijkstra, a_star, bfs, connected_components

def print_path(graph, path, cost, metric):
    if not path:
        print("No se encontró una ruta.")
        return

    print("\nRuta Recomendada:")
    for i, node_id in enumerate(path):
        node = graph.get_node(node_id)
        if i == 0:
            print(f"  [Inicio] {node.name} (Línea {node.line})")
        else:
            prev_node = graph.get_node(path[i-1])
            if prev_node.line != node.line:
                print(f"  [Transbordo] Cambiar a Línea {node.line}")
            print(f"  -> {node.name}")
    
    # Definir unidades
    units = ""
    if metric == "distance": units = " km"
    elif metric == "time": units = " min"
    elif metric == "cost": units = " COP"
    elif metric == "transbordos/estaciones recorridas": units = " tramos"
    
    print(f"\nCosto Total ({metric}): {cost:.2f}{units}")

def main():
    try:
        graph = load_graph("data.json")
    except Exception as e:
        print(f"Error cargando los datos: {e}")
        return

    nodes = graph.get_all_nodes()
    
    print("=" * 40)
    print("Bienvenido a MetroPath - Medellín")
    print("=" * 40)
    
    # Comprobar conectividad
    components = connected_components(graph)
    if len(components) > 1:
        print(f"[Advertencia] La red de transporte está dividida en {len(components)} componentes desconectados.")
    else:
        print("[Info] La red está completamente conectada.\n")

    while True:
        print("Opciones:")
        print("1. Buscar ruta óptima (Dijkstra vs A*)")
        print("2. Buscar ruta con menos transbordos (BFS)")
        print("3. Listar estaciones")
        print("4. Salir")
        
        choice = input("Selecciona una opción: ").strip()
        
        if choice == '4':
            print("Saliendo de MetroPath...")
            break
        elif choice == '3':
            print("\nEstaciones Disponibles:")
            for node_id in nodes:
                node = graph.get_node(node_id)
                print(f"- {node.name} ({node_id}) [Línea {node.line}]")
            print()
        elif choice == '1':
            start = input("ID estación origen: ").strip()
            end = input("ID estación destino: ").strip()
            
            if start not in nodes or end not in nodes:
                print("Estaciones inválidas. Usa la opción 3 para ver los IDs válidos.\n")
                continue
                
            print("Criterio de optimización:")
            print("a) time (tiempo)")
            print("b) distance (distancia)")
            print("c) cost (costo)")
            
            crit_choice = input("Selecciona criterio: ").strip().lower()
            criteria = "time"
            if crit_choice == 'b':
                criteria = "distance"
            elif crit_choice == 'c':
                criteria = "cost"
            
            print(f"\nCalculando ruta desde {start} hasta {end} optimizando {criteria}...")
            
            # Dijkstra
            start_time = time.perf_counter()
            d_path, d_cost, d_nodes = dijkstra(graph, start, end, criteria)
            d_time = (time.perf_counter() - start_time) * 1000
            
            # A*
            start_time = time.perf_counter()
            a_path, a_cost, a_nodes = a_star(graph, start, end, criteria)
            a_time = (time.perf_counter() - start_time) * 1000
            
            print_path(graph, d_path, d_cost, criteria)
            
            print("\n--- Comparativa de Rendimiento ---")
            print(f"Dijkstra : {d_time:.3f} ms | Nodos visitados: {d_nodes}")
            print(f"A*       : {a_time:.3f} ms | Nodos visitados: {a_nodes}")
            print("----------------------------------\n")
            
        elif choice == '2':
            start = input("ID estación origen: ").strip()
            end = input("ID estación destino: ").strip()
            
            if start not in nodes or end not in nodes:
                print("Estaciones inválidas.\n")
                continue
                
            path, cost, visited = bfs(graph, start, end)
            print_path(graph, path, cost, "transbordos/estaciones recorridas")
            print(f"Nodos visitados por BFS: {visited}\n")
        else:
            print("Opción inválida.\n")

if __name__ == "__main__":
    main()
