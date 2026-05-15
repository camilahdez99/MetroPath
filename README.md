
=======
# MetroPath: Sistema de Planificación de Rutas de Transporte Público

**Estudiantes:** Camila Hernandez, Silenia Toro, Sebastian Escobar
**Proyecto:** Core de Navegación de Transporte Urbano (Entregable 2)  
**Tecnologías:** Python, Grafos, Algoritmos de Optimización.

---

## 1. Objetivo del Proyecto
Desarrollar un sistema de navegación eficiente para redes de transporte público urbano que permita a los usuarios encontrar rutas óptimas basadas en diferentes criterios:
- **Tiempo:** Minimizar la duración del viaje.
- **Distancia:** Encontrar el recorrido físico más corto.
- **Costo:** Minimizar el gasto económico.
- **Transbordos:** Encontrar rutas con el mínimo número de cambios de línea (BFS).

---

## 2. Arquitectura General
El sistema sigue un diseño modular para separar la gestión de datos de la lógica algorítmica:

```mermaid
graph TD
    A[data.json] -->|Parsing| B(dataloader.py)
    B --> C{Graph Engine}
    C --> D[datastructures.py]
    C --> E[algorithms.py]
    E --> F[main.py CLI]
    F --> G[Usuario Final]
```

- **Módulo de Datos:** Archivo JSON que modela la red del Metro de Medellín.
- **Capa de Estructuras:** Implementación propia de Grafos mediante listas de adyacencia.
- **Motor Algorítmico:** Implementaciones optimizadas de Dijkstra, A* y BFS.
- **Interfaz (CLI):** Aplicación de consola para interacción y comparativa de rendimiento.

---

## 3. Modelado de Grafos
La red de transporte se modeló como un **Grafo Ponderado No Dirigido**.

- **Nodos (V):** Representan las estaciones. Cada nodo contiene:
    - Identificador único, nombre, línea y coordenadas geográficas (X, Y).
- **Aristas (E):** Representan las conexiones físicas entre estaciones. Cada arista posee pesos multivariables:
    - `time`: float (minutos)
    - `distance`: float (kilómetros)
    - `cost`: float (pesos colombianos)

**Estructura de Datos Principal:** Se utilizó una **Lista de Adyacencia** implementada con un diccionario de Python (`Hashtable`) para obtener una complejidad de búsqueda de vecinos de $O(1)$ en promedio.

---

## 4. Diagramas Técnicos

### Diagrama de Clases
```mermaid
classDiagram
    class Node {
        +String id
        +String name
        +String line
        +float x, y
    }
    class Edge {
        +String from_node
        +String to_node
        +float time
        +float distance
        +float cost
        +get_weight(criteria)
    }
    class Graph {
        +dict nodes
        +dict edges
        +add_node(Node)
        +add_edge(Edge)
        +get_neighbors(id)
    }
    Graph "1" *-- "many" Node
    Graph "1" *-- "many" Edge
```

---

## 5. Explicación de Algoritmos

### Dijkstra
Busca la ruta más corta expandiéndose uniformemente desde el origen. Utiliza una **Cola de Prioridad (Min-Heap)** para extraer siempre el nodo con la menor distancia acumulada, garantizando una complejidad de $O((V+E) \log V)$.

### A* (A-Star)
Mejora a Dijkstra incorporando una **función heurística** $f(n) = g(n) + h(n)$. 
- $g(n)$: Costo real acumulado.
- $h(n)$: Estimación al destino (Distancia Euclídea).
Esto permite que el algoritmo "ignore" estaciones que se alejan de la meta, reduciendo drásticamente los nodos visitados.

### BFS (Breadth-First Search)
Utilizado para la opción de "Mínimos Transbordos". Al no considerar pesos, encuentra la ruta con menos aristas entre dos puntos.

---

## 6. Evidencia de Código (Implementación Propia)

### Lógica del Algoritmo A*
```python
def a_star(graph, start_id, end_id, criteria):
    queue = []
    heapq.heappush(queue, (0, start_id))
    g_scores = {node_id: float('inf') for node_id in graph.get_all_nodes()}
    g_scores[start_id] = 0
    
    while queue:
        current_f, current_id = heapq.heappop(queue)
        if current_id == end_id: break
        
        for edge in graph.get_neighbors(current_id):
            weight = edge.get_weight(criteria)
            tentative_g = g_scores[current_id] + weight
            if tentative_g < g_scores[edge.to_node]:
                g_scores[edge.to_node] = tentative_g
                f_score = tentative_g + heuristic(neighbor, end_node)
                heapq.heappush(queue, (f_score, edge.to_node))
```

---

## 7. Conclusiones Técnicas
1. **Eficiencia Algorítmica:** A* demostró ser hasta un 30-40% más eficiente que Dijkstra en términos de nodos explorados cuando existe una heurística geográfica válida.
2. **Flexibilidad:** El modelado multivariable permite cambiar el criterio de optimización (tiempo/distancia/costo) sin modificar la estructura del grafo.
3. **Validación de Red:** El algoritmo de componentes conectados es vital para asegurar que la infraestructura cargada es funcional y no existen estaciones "huérfanas".
4. **Impacto de la Heurística:** En búsquedas por "Costo", A* se degrada a Dijkstra debido a la falta de una estimación monetaria basada en posición, evidenciando la importancia de elegir una heurística admisible.

>>>>>>> e0ca995c14c314544ac00544ede04617ede1a83f
# MetroPath

Herramienta simple para calcular rutas en la red de metro (Medellín) con varias estrategias (Dijkstra, A* y BFS) y una interfaz web mínima.

Este repositorio contiene una implementación en Python que permite: 1) usar una aplicación de consola interactiva para buscar rutas, 2) levantar un servidor web (FastAPI) que expone una API para la UI estática en `static/`.

## Estructura del proyecto

- `main.py` - Interfaz de consola interactiva (modo terminal).
- `server.py` - Servidor FastAPI que expone endpoints REST y sirve la UI estática en `static/`.
- `algorithms.py` - Implementación de Dijkstra, A*, BFS y utilidades.
- `dataloader.py` - Carga del grafo desde `data.json`.
- `datastructures.py` - Estructuras de datos (Graph, Node, Edge).
- `data.json` - Datos del grafo (estaciones y conexiones).
- `static/` - Archivos estáticos (interfaz web): `index.html`, `script.js`, `style.css`.

## Requisitos

- Python 3.10+ (probado con Python 3.13 en el entorno del autor).
- pip

Dependencias Python (solo necesarias para el servidor web):

- fastapi
- uvicorn

Puedes instalarlas con pip:

```powershell
cd 'c:\Users\Juliana Giraldo\Desktop\MetroPath'
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn
```

## Ejecutar la aplicación

Hay dos formas principales de usar MetroPath:

1) Ejecutar la interfaz de consola

```powershell
# Desde la carpeta del proyecto
python main.py
```

La app de consola es interactiva: muestra un menú para buscar rutas (Dijkstra/A*), buscar rutas con menos transbordos (BFS), listar estaciones y salir.

2) Levantar el servidor web (FastAPI) y usar la UI estática

```powershell
# Desde la carpeta del proyecto
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Luego abre tu navegador en: http://localhost:8000

La UI carga datos desde la API y permite solicitar rutas desde el navegador.

### Endpoints disponibles

- `GET /api/stations` — retorna la lista de estaciones (id, nombre, línea, x, y).
- `GET /api/graph` — retorna el JSON completo del grafo (incluye conexiones).
- `POST /api/route` — calcula la ruta entre dos estaciones.

Ejemplo de `POST /api/route` (PowerShell usando `Invoke-RestMethod`):

```powershell
$body = @{ start = 'A1'; end = 'B3'; criteria = 'time' } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/api/route -Method POST -Body $body -ContentType 'application/json'
```

Ejemplo con `curl` (si lo tienes instalado):

```powershell
curl -X POST http://localhost:8000/api/route -H "Content-Type: application/json" -d '{"start":"A1","end":"B3","criteria":"time"}'
```

Nota: reemplaza los IDs `A1`, `B3` por los IDs válidos listados en `GET /api/stations` o desde la opción "Listar estaciones" en la consola.

## Datos y edición

El grafo se carga desde `data.json`. Si necesitas añadir/modificar estaciones o conexiones, edita ese archivo y reinicia el servidor (o reinicia la app de consola).

## Resolución de problemas

- Si el puerto 8000 ya está en uso, cambia el puerto en el comando de uvicorn (por ejemplo `--port 8080`).
- Si `python` apunta a otra versión, usa el ejecutable explícito (por ejemplo `py -3.11` o la ruta completa a `python.exe`).
- Si ves errores importando módulos, confirma que tu `PYTHONPATH` sea la carpeta del proyecto o ejecuta los comandos desde la raíz del proyecto.

## Desarrollo y pruebas

- Para probar la API manualmente usa las herramientas anteriores (`Invoke-RestMethod`, `curl`, o Postman).
- Para añadir tests, puedes crear un directorio `tests/` y usar `pytest`.

## Siguientes mejoras (ideas)

- Añadir pruebas unitarias para `algorithms.py` (Dijkstra/A*/BFS).
- Cachear el grafo en memoria con recarga automática al cambiar `data.json`.
- Mejorar la UI para visualizar el grafo y rutas sobre un mapa.

## Licencia

Este proyecto no incluye una licencia explícita. Si quieres publicarlo, añade un archivo `LICENSE` (por ejemplo MIT).

---

<<<<<<< HEAD
Si quieres, puedo también:

- Generar un `requirements.txt` con las dependencias exactas.
- Crear un ejemplo de `data.json` mínimo para pruebas.
- Añadir tests básicos y correrlos.

Indica qué prefieres y lo hago enseguida.
=======
>>>>>>> e0ca995c14c314544ac00544ede04617ede1a83f
