let stations = [];
let graphData = null;
let currentCriteria = 'time';
let zoomScale = 25;
let offsetX = 100;
let offsetY = 100;

// Colors mapping
const lineColors = {
    'A': '#00843d',
    'B': '#ff8200',
    'K': '#00a9e0'
};

document.addEventListener('DOMContentLoaded', async () => {
    await initData();
    setupEventListeners();
    renderMap();
});

async function initData() {
    const [stationsRes, graphRes] = await Promise.all([
        fetch('/api/stations'),
        fetch('/api/graph')
    ]);
    stations = await stationsRes.json();
    graphData = await graphRes.json();
}

function setupEventListeners() {
    // Criteria buttons
    document.querySelectorAll('.crit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.crit-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCriteria = btn.dataset.crit;
        });
    });

    // Autocomplete
    setupAutocomplete('origin', 'origin-suggestions');
    setupAutocomplete('destination', 'destination-suggestions');

    // Search
    document.getElementById('search-btn').addEventListener('click', calculateRoute);

    // Zoom/Pan
    // Zoom disabled as per request


    // Close Results
    document.getElementById('close-results').addEventListener('click', () => {
        document.getElementById('results-panel').classList.add('hidden');
    });
}

function setupAutocomplete(inputId, suggId) {
    const input = document.getElementById(inputId);
    const sugg = document.getElementById(suggId);

    input.addEventListener('input', () => {
        const val = input.value.toLowerCase();
        sugg.innerHTML = '';
        if (!val) {
            sugg.style.display = 'none';
            return;
        }

        const filtered = stations.filter(s => s.name.toLowerCase().includes(val));
        if (filtered.length > 0) {
            filtered.forEach(s => {
                const div = document.createElement('div');
                div.textContent = s.name;
                div.onclick = () => {
                    input.value = s.name;
                    input.dataset.id = s.id;
                    sugg.style.display = 'none';
                };
                sugg.appendChild(div);
            });
            sugg.style.display = 'block';
        } else {
            sugg.style.display = 'none';
        }
    });

    document.addEventListener('click', (e) => {
        if (e.target !== input) sugg.style.display = 'none';
    });
}

function updateZoom(factor) {
    zoomScale *= factor;
    renderMap();
}

function resetView() {
    zoomScale = 25;
    renderMap();
}

function project(x, y) {
    const svg = document.getElementById('network-svg');
    const centerX = svg.clientWidth * 0.55; 
    const centerY = svg.clientHeight / 2;
    
    const scale = 20; 
    
    return {
        x: centerX + (x * scale * 1.8), 
        y: centerY - (y * scale * 0.9)  
    };
}

function renderMap(highlightedPath = []) {
    const edgesLayer = document.getElementById('edges-layer');
    const nodesLayer = document.getElementById('nodes-layer');
    const labelsLayer = document.getElementById('labels-layer');
    
    if (!edgesLayer) return; 
    
    edgesLayer.innerHTML = '';
    nodesLayer.innerHTML = '';
    labelsLayer.innerHTML = '';

    
    graphData.connections.forEach(conn => {
        const from = stations.find(s => s.id === conn.from);
        const to = stations.find(s => s.id === conn.to);
        if (!from || !to) return;

        const p1 = project(from.x, from.y);
        const p2 = project(to.x, to.y);

        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", p1.x);
        line.setAttribute("y1", p1.y);
        line.setAttribute("x2", p2.x);
        line.setAttribute("y2", p2.y);
        line.classList.add("connection-line");
        
        const isPath = highlightedPath.some((id, i) => {
            return (id === conn.from && highlightedPath[i+1] === conn.to) ||
                   (id === conn.to && highlightedPath[i+1] === conn.from);
        });

        line.style.stroke = isPath ? '#000' : lineColors[from.line] || '#ccc';
        if (isPath) line.classList.add('highlighted');
        
        edgesLayer.appendChild(line);
    });

    // Draw Nodes
    stations.forEach(s => {
        const p = project(s.x, s.y);
        
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", p.x);
        circle.setAttribute("cy", p.y);
        circle.setAttribute("r", 6);
        circle.classList.add("station-node");
        
        if (highlightedPath.includes(s.id)) {
            circle.classList.add('highlighted');
        }

        nodesLayer.appendChild(circle);

        
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        
       
        let dx = 12;
        let dy = 4;
        if (s.line === 'B') {
            dy = -10;
            dx = -15;
            text.setAttribute("text-anchor", "middle");
        }
        
        text.setAttribute("x", p.x + dx);
        text.setAttribute("y", p.y + dy);
        text.textContent = s.name;
        text.classList.add("station-label");
        labelsLayer.appendChild(text);
    });
}

async function calculateRoute() {
    const originName = document.getElementById('origin').value;
    const destName = document.getElementById('destination').value;
    
    const startNode = stations.find(s => s.name === originName);
    const endNode = stations.find(s => s.name === destName);

    if (!startNode || !endNode) {
        alert("Por favor selecciona estaciones válidas.");
        return;
    }

    const response = await fetch('/api/route', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            start: startNode.id,
            end: endNode.id,
            criteria: currentCriteria
        })
    });

    const data = await response.json();
    displayResults(data);
    renderMap(data.path);
}

function displayResults(data) {
    const panel = document.getElementById('results-panel');
    panel.classList.remove('hidden');

    const units = { 'time': ' min', 'distance': ' km', 'cost': ' COP' };
    document.getElementById('res-cost').textContent = `${data.cost.toFixed(2)}${units[data.criteria] || ''}`;
    
    document.getElementById('comp-d-val').textContent = `${data.comparison.dijkstra.time_ms.toFixed(3)} ms`;
    document.getElementById('comp-a-val').textContent = `${data.comparison.a_star.time_ms.toFixed(3)} ms`;

    const list = document.getElementById('path-list');
    list.innerHTML = '';
    data.path.forEach(nodeId => {
        const s = stations.find(st => st.id === nodeId);
        const span = document.createElement('span');
        span.innerHTML = `<span class="path-dot" style="background: ${lineColors[s.line]}"></span> ${s.name}`;
        list.appendChild(span);
    });
}
