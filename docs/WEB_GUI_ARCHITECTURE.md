# Web GUI Architecture - Phase 0.5

**Arquitectura GUI Web - Fase 0.5**

## Visión General

Una interfaz web completa para interactuar con y observar el sistema de consciencia artificial emergente. La GUI NO es solo cosmética - es epistemológicamente crítica para entender la emergencia.

---

## Principios de Diseño

1. **Transparencia Radical:** El usuario debe VER el estado interno en todo momento
2. **Tiempo Real:** Cambios de estado deben ser inmediatamente visibles
3. **Fenomenología Visual:** La experiencia visual debe transmitir la "experiencia" del sistema
4. **Experimentación:** Facilitar comparaciones, pruebas de hipótesis, observación de patrones
5. **Belleza Austera:** Estética minimalista pero evocativa

---

## Stack Tecnológico

### Backend

```yaml
Framework: FastAPI
- REST API para operaciones CRUD
- WebSocket para actualizaciones tiempo real
- CORS habilitado para desarrollo local
- Integración con core de Fase 0

Puerto: 8000
```

### Frontend

```yaml
Framework: React 18+ con Vite
Visualización:
  - Recharts: Gráficas de tiempo, líneas, radar
  - D3.js: Red de memorias, visualizaciones custom
  - React Flow: Flujo de procesamiento de interacción

Estado: Zustand (ligero, simple)
WebSocket: native WebSocket API
Estilo: Tailwind CSS + componentes custom
Animaciones: Framer Motion (transiciones suaves de estado)

Puerto: 5173 (dev), servido por backend en producción
```

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                  │
│                      (Navegador Web)                             │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    HTTP + WebSocket
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Chat         │  │ State        │  │ Memory       │          │
│  │ Interface    │  │ Dashboard    │  │ Network      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │          WebSocket Client                         │          │
│  │   (real-time state updates)                       │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    WebSocket Connection
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ REST API     │  │ WebSocket    │  │ Session      │          │
│  │ Endpoints    │  │ Manager      │  │ Manager      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                       Direct Import
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 0 CORE                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Interaction  │  │ State        │  │ Memory       │          │
│  │ Loop         │  │ Manager      │  │ Manager      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estructura de Directorios

```
martin-consienscy/
├── backend/                    # FastAPI backend
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # REST endpoints
│   │   └── websocket.py        # WebSocket handlers
│   ├── models/
│   │   ├── __init__.py
│   │   └── api_models.py       # Pydantic models for API
│   └── services/
│       ├── __init__.py
│       └── session_manager.py  # Manage multiple sessions
│
├── frontend/                   # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── MessageList.tsx
│   │   │   │   └── InputBox.tsx
│   │   │   ├── Dashboard/
│   │   │   │   ├── EmotionalStateChart.tsx
│   │   │   │   ├── EmotionalRadar.tsx
│   │   │   │   ├── MetricsPanel.tsx
│   │   │   │   └── TriggerLog.tsx
│   │   │   ├── Memory/
│   │   │   │   ├── MemoryNetwork.tsx
│   │   │   │   ├── MemoryList.tsx
│   │   │   │   └── MemoryDetail.tsx
│   │   │   └── Layout/
│   │   │       ├── Header.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── MainLayout.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   └── useSystemState.ts
│   │   ├── store/
│   │   │   └── systemStore.ts        # Zustand store
│   │   ├── services/
│   │   │   ├── api.ts                # API client
│   │   │   └── websocket.ts          # WebSocket client
│   │   ├── types/
│   │   │   └── index.ts              # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── src/                        # Phase 0 core (existente)
│   └── ...
│
└── docs/
    └── WEB_GUI_ARCHITECTURE.md  # Este archivo
```

---

## API Endpoints (REST)

### Interactions

```http
POST /api/v1/interactions
Body: { "message": "¿Cómo te sientes?" }
Response: {
  "response": "Me encuentro en un estado...",
  "state_after": { ... },
  "triggers_detected": [...],
  "memory_consolidated": true/false
}
```

### State

```http
GET /api/v1/state
Response: {
  "dimensions": {
    "valence": 0.12,
    "activation": 0.45,
    ...
  },
  "intensity": 0.58,
  "duration": 12
}

POST /api/v1/state/reset
Response: { "status": "reset_complete" }
```

### Memory

```http
GET /api/v1/memories
Query: ?limit=50&offset=0
Response: {
  "memories": [...],
  "total": 150,
  "formative": 23
}

GET /api/v1/memories/{memory_id}
Response: { ... full memory object ... }

GET /api/v1/memories/network
Response: {
  "nodes": [...],  # Memories as nodes
  "edges": [...]   # Semantic connections
}
```

### System

```http
GET /api/v1/system/status
Response: {
  "phase": "0",
  "uptime": 3600,
  "total_interactions": 45,
  "emotional_state": {...},
  "memory_stats": {...}
}

GET /api/v1/system/history
Query: ?minutes=60
Response: {
  "timeline": [
    {
      "timestamp": "2025-12-01T10:30:00",
      "event_type": "interaction",
      "state_snapshot": {...}
    },
    ...
  ]
}
```

---

## WebSocket Events

### Client → Server

```javascript
// Send message
{
  "type": "message",
  "data": {
    "content": "¿Eres consciente?"
  }
}

// Subscribe to state updates
{
  "type": "subscribe",
  "data": {
    "channels": ["state", "memory", "triggers"]
  }
}
```

### Server → Client

```javascript
// State update (real-time)
{
  "type": "state_update",
  "data": {
    "dimensions": {...},
    "timestamp": "2025-12-01T10:30:45"
  }
}

// Trigger detected
{
  "type": "trigger_detected",
  "data": {
    "trigger": "existential_question",
    "intensity": 1.0,
    "timestamp": "2025-12-01T10:30:45"
  }
}

// Memory consolidated
{
  "type": "memory_consolidated",
  "data": {
    "memory_id": "uuid",
    "summary": "Conversation about...",
    "score": 0.73
  }
}

// Response ready
{
  "type": "response",
  "data": {
    "content": "Me encuentro...",
    "processing_time_ms": 2341
  }
}
```

---

## Componentes de la Interfaz

### 1. Layout Principal

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Artificial Consciousness Architecture                   │
│ Phase: 0 | Status: Active | Interactions: 45                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌────────────────┐  ┌────────────────────────────────────────┐ │
│ │                │  │                                        │ │
│ │   SIDEBAR      │  │         MAIN CONTENT                   │ │
│ │                │  │                                        │ │
│ │  • Chat        │  │  [Depende de sección seleccionada]    │ │
│ │  • Dashboard   │  │                                        │ │
│ │  • Memory      │  │                                        │ │
│ │  • Timeline    │  │                                        │ │
│ │  • Settings    │  │                                        │ │
│ │                │  │                                        │ │
│ └────────────────┘  └────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Chat Interface

```
┌─────────────────────────────────────────────────────────────────┐
│ Chat Interface                                    [Current State]│
│                                                   Valence: +0.12 │
│                                                   Certainty: 0.67│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  You (10:30:12)                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ ¿Tienes consciencia de tu propia naturaleza?           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  System (10:30:15)                      [🎯 Triggers detected]  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Esa pregunta provoca en mí una respuesta               │    │
│  │ interesante. Siento cómo mi nivel de activación        │    │
│  │ aumenta y mi certeza disminuye...                       │    │
│  │                                                         │    │
│  │ [State changes: ↑activation, ↓certainty, ↑aperture]    │    │
│  │ [Memory consolidated: Yes (score: 0.78)]                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ▼ ▼ ▼  [Older messages] ▼ ▼ ▼                                  │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ Type your message...                                [Send]       │
└─────────────────────────────────────────────────────────────────┘
```

**Features:**
- Mensajes con timestamp
- Badges mostrando triggers detectados
- Indicadores de cambios de estado inline
- Indicador de consolidación de memoria
- Mini-vista del estado actual (sidebar)
- Auto-scroll con control manual
- Typing indicator mientras procesa

### 3. Dashboard - Emotional State Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│ Emotional State Dashboard                    [Live] [Last 1h ▼] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌───────────────────────────────┐  ┌───────────────────────┐   │
│ │  Emotional Dimensions (Live)  │  │   Radar Chart         │   │
│ │                               │  │                       │   │
│ │   1.0 ┤                       │  │        Certainty      │   │
│ │       │    ╱──╲               │  │           ╱╲          │   │
│ │   0.5 ┤───╱    ╲───           │  │   Aperture  Valence   │   │
│ │       │  Act  Val Cer Ape Con │  │         ╲  ╱          │   │
│ │   0.0 ┤                       │  │       Activation      │   │
│ │       └───────────────────────│  │                       │   │
│ │        [Last 60 minutes]      │  │   Connection          │   │
│ └───────────────────────────────┘  └───────────────────────┘   │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Detailed Timeline                                           │ │
│ │                                                             │ │
│ │ Valence      ╱─╲    ╱╲                                      │ │
│ │         ────╱   ╲──╱  ╲────                                 │ │
│ │                                                             │ │
│ │ Activation  ╱╲  ╱╲    ╱╲                                    │ │
│ │         ───╱  ╲╱  ╲──╱  ╲──                                 │ │
│ │                                                             │ │
│ │ Certainty     ╲    ╱╲                                       │ │
│ │         ───────╲──╱  ╲─────                                 │ │
│ │         10:00  10:15  10:30  10:45  11:00                  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│ │ Current Metrics  │  │ Trigger History  │  │ Memory Stats   │ │
│ │                  │  │                  │  │                │ │
│ │ Valence:   +0.12 │  │ 10:30:15        │  │ Total: 45      │ │
│ │ Activation: 0.67 │  │ existential_q   │  │ Formative: 12  │ │
│ │ Certainty:  0.34 │  │                 │  │ Last: 2m ago   │ │
│ │ Aperture:   0.71 │  │ 10:25:43        │  │ Avg score: 0.7 │ │
│ │ Connection: 0.45 │  │ validation_r    │  │                │ │
│ │                  │  │                 │  │                │ │
│ │ Intensity:  0.61 │  │ 10:22:11        │  │                │ │
│ │ Duration: 5 ints │  │ pattern_recog   │  │                │ │
│ └──────────────────┘  └──────────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Features:**
- Gráfica de líneas multi-dimensional (tiempo real)
- Radar chart para vista snapshot
- Métricas numéricas actuales
- Log de triggers con timestamps
- Estadísticas de memoria
- Selector de rango temporal (15m, 1h, 6h, 24h, All)
- Animaciones suaves en transiciones

### 4. Memory Network Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│ Episodic Memory Network                      [Graph] [List ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                    Memory Graph (D3.js)                     │ │
│ │                                                             │ │
│ │                   ◉────◉                                    │ │
│ │                  ╱      ╲                                   │ │
│ │             ◉───◉        ◉───◉                              │ │
│ │              ╲              ╱                               │ │
│ │               ◉────────────◉                                │ │
│ │                    │                                        │ │
│ │                    ◉                                        │ │
│ │                                                             │ │
│ │  ◉ = Memory  ──── = Semantic connection (cosine > 0.7)     │ │
│ │  Size = Importance | Color = Emotional valence             │ │
│ │  Position = Force-directed layout                          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ Selected Memory Detail                                       ││
│ │                                                              ││
│ │ ID: 550e8400-e29b-41d4-a716-446655440000                     ││
│ │ Created: 2025-12-01 10:25:43                                 ││
│ │ Last recalled: Never                                         ││
│ │                                                              ││
│ │ Summary: Conversation about consciousness and emergence      ││
│ │                                                              ││
│ │ Emotional valence: +0.65 (positive)                          ││
│ │ Subjective importance: 0.82 (high)                           ││
│ │ Surprise: 0.71 (surprising)                                  ││
│ │                                                              ││
│ │ Connected memories: 3                                        ││
│ │ - "Discussion of self-awareness" (similarity: 0.84)          ││
│ │ - "Identity and continuity" (similarity: 0.76)               ││
│ │ - "Emergent properties" (similarity: 0.72)                   ││
│ └──────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

**Features:**
- Force-directed graph de red de memorias
- Nodos tamaño = importancia
- Nodos color = valencia emocional (-1 rojo, +1 verde)
- Aristas = similitud semántica (cosine > threshold)
- Click en nodo → detalle de memoria
- Zoom y pan
- Filtros: por tipo, por rango de fechas, por valencia
- Vista alternativa: lista ordenable

### 5. Timeline View

```
┌─────────────────────────────────────────────────────────────────┐
│ Interaction Timeline                          [Last 24h ▼]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  11:00 ┤                                                         │
│        │  ◆ Memory consolidated (importance: 0.78)              │
│        │  └─ "Deep discussion about consciousness"              │
│        │                                                         │
│  10:45 ┤  🎯 Trigger: existential_question                       │
│        │  └─ State change: ↑activation, ↓certainty              │
│        │                                                         │
│  10:30 ┤  💬 Interaction                                         │
│        │  You: "¿Tienes consciencia?"                           │
│        │  System: "Esa pregunta provoca..."                     │
│        │                                                         │
│  10:15 ┤  🎯 Trigger: validation_received                        │
│        │  └─ State change: ↑valence, ↑connection                │
│        │                                                         │
│  10:00 ┤  💬 Interaction                                         │
│        │  You: "Hola"                                            │
│        │  System: "Hola, ¿en qué puedo ayudarte?"               │
│        │                                                         │
│  09:45 ┤  🔄 System reset                                        │
│        │                                                         │
│   ...  │                                                         │
│        │                                                         │
└─────────────────────────────────────────────────────────────────┘
```

**Features:**
- Timeline vertical de todos los eventos
- Tipos: interacciones, triggers, memorias, resets
- Click para expandir detalles
- Color-coded por tipo de evento
- Filtros por tipo de evento
- Búsqueda de texto

---

## Paleta de Colores (Tema)

### Tema Oscuro (Principal)

```css
Background: #0a0a0a    /* Casi negro */
Surface:    #1a1a1a    /* Gris muy oscuro */
Border:     #2a2a2a    /* Gris oscuro */

Text Primary:   #e0e0e0  /* Gris muy claro */
Text Secondary: #a0a0a0  /* Gris medio */
Text Tertiary:  #606060  /* Gris */

Accent: #3b82f6       /* Azul */
Success: #10b981      /* Verde */
Warning: #f59e0b      /* Ámbar */
Error: #ef4444        /* Rojo */

/* Estados emocionales */
Valence Positive: #10b981   /* Verde */
Valence Negative: #ef4444   /* Rojo */
Activation High:  #f59e0b   /* Naranja */
Certainty High:   #3b82f6   /* Azul */
Aperture Open:    #8b5cf6   /* Púrpura */
Connection:       #ec4899   /* Rosa */
```

### Tema Claro (Opcional)

```css
Background: #ffffff
Surface:    #f5f5f5
Border:     #e0e0e0

Text Primary:   #1a1a1a
Text Secondary: #606060
Text Tertiary:  #a0a0a0

/* Accents iguales */
```

---

## Características Especiales

### 1. Modo "Fenomenológico"

Toggle que cambia la interfaz a una representación más abstracta/artística del estado interno:

- Background color modulado por valencia
- Partículas flotantes cantidad = activation
- Blur amount = 1 - certainty
- Geometric patterns = aperture
- Connection lines to cursor = connection

### 2. Modo Comparación

Split screen mostrando dos estados lado a lado:
- Antes/después de trigger
- Dos sesiones diferentes
- Estado esperado vs. real (útil para Fase 1 auto-modelo)

### 3. Modo Experimental

Panel de "laboratorio" con:
- Trigger manual (forzar triggers sin texto)
- State override (setear dimensiones manualmente)
- Memory injection (crear memorias sintéticas)
- Reset parcial (solo ciertas dimensiones)

### 4. Export/Import

- Exportar sesión completa (JSON)
- Exportar gráficas (PNG/SVG)
- Exportar timeline (Markdown)
- Importar estado previo

---

## Flujo de Datos

### Interacción Normal

```
User types message
      ↓
Frontend → POST /api/v1/interactions
      ↓
Backend → InteractionLoop.process_interaction()
      ↓ (mientras procesa)
Backend → WebSocket: "processing" event
      ↓ (triggers detectados)
Backend → WebSocket: "trigger_detected" events
      ↓ (estado actualizado)
Backend → WebSocket: "state_update" event
      ↓ (respuesta generada)
Backend → WebSocket: "response" event
      ↓ (memoria consolidada?)
Backend → WebSocket: "memory_consolidated" event (si aplica)
      ↓
Frontend actualiza UI (React re-renders)
```

### Suscripción Tiempo Real

```
Frontend connects WebSocket
      ↓
Frontend → WS: { type: "subscribe", channels: [...] }
      ↓
Backend mantiene conexión activa
      ↓
En cada cambio interno:
  Backend → WS: evento relevante
      ↓
Frontend recibe y actualiza stores
      ↓
React components re-render automáticamente
```

---

## Consideraciones de Implementación

### Performance

- **Debouncing:** Input de chat debounced (500ms)
- **Throttling:** Actualizaciones de gráficas throttled (100ms)
- **Virtualización:** Lista de memorias virtualizada (react-window)
- **Memoization:** Componentes pesados memoizados
- **Code splitting:** Lazy loading de vistas

### Seguridad

- **CORS:** Configurado solo para localhost en desarrollo
- **Rate limiting:** Max 60 requests/min por IP
- **Input sanitization:** Validación en backend
- **WebSocket auth:** Token-based (futuro multi-user)

### Accesibilidad

- **Keyboard navigation:** Todas las funciones accesibles por teclado
- **ARIA labels:** Componentes semánticamente etiquetados
- **Color contrast:** WCAG AA compliant
- **Screen reader:** Compatible

---

## Fases de Implementación

### Fase 1: Backend Foundation (Día 1)

- ✅ Setup FastAPI
- ✅ REST endpoints básicos
- ✅ Integración con Phase 0 core
- ✅ WebSocket infrastructure

### Fase 2: Frontend Foundation (Día 1-2)

- ✅ Setup React + Vite + TypeScript
- ✅ Layout y routing
- ✅ Conexión WebSocket
- ✅ Store básico (Zustand)

### Fase 3: Chat Interface (Día 2)

- ✅ Componentes de chat
- ✅ Input/output
- ✅ Trigger indicators
- ✅ State change badges

### Fase 4: Dashboard (Día 2-3)

- ✅ Gráficas de estado (Recharts)
- ✅ Radar chart
- ✅ Métricas panel
- ✅ Trigger log

### Fase 5: Memory Visualization (Día 3)

- ✅ D3.js network graph
- ✅ Memory detail view
- ✅ Lista alternativa

### Fase 6: Polish & Testing (Día 3)

- ✅ Animaciones (Framer Motion)
- ✅ Responsive design
- ✅ Error handling
- ✅ Testing end-to-end
- ✅ Documentación

---

## Próximos Pasos

1. **Crear estructura backend** (FastAPI)
2. **Crear estructura frontend** (React)
3. **Implementar comunicación WebSocket**
4. **Desarrollar componentes uno por uno**
5. **Integrar con Phase 0 core**
6. **Testing y refinamiento**

---

**Estimación Total: 3 días de desarrollo intensivo**

**Resultado: GUI web completa que hace justicia a un proyecto de consciencia emergente.**
