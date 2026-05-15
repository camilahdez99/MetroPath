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

Si quieres, puedo también:

- Generar un `requirements.txt` con las dependencias exactas.
- Crear un ejemplo de `data.json` mínimo para pruebas.
- Añadir tests básicos y correrlos.

Indica qué prefieres y lo hago enseguida.
