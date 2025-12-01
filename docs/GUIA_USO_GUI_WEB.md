# Guía de Uso GUI Web - Fase 0.5

**Web GUI Usage Guide - Phase 0.5**

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.11+ (para backend)
- Node.js 18+ y npm (para frontend)
- Clave API de Anthropic

### Instalación

**1. Instalar Dependencias del Backend**

```bash
# Desde la raíz del proyecto
pip install -r requirements.txt
```

**2. Instalar Dependencias del Frontend**

```bash
# Navegar al frontend
cd frontend

# Instalar paquetes npm
npm install
```

**3. Configurar Entorno**

```bash
# Desde la raíz del proyecto
cp .env.example .env

# Editar .env y agregar tu clave API
# ANTHROPIC_API_KEY=tu-clave-aqui
```

### Ejecutar el Sistema

**Terminal 1: Servidor Backend**

```bash
# Desde la raíz del proyecto
python -m backend.main

# El servidor inicia en http://localhost:8000
```

**Terminal 2: Servidor Dev Frontend**

```bash
# Desde el directorio frontend
cd frontend
npm run dev

# El servidor dev inicia en http://localhost:5173
```

**Acceder a la GUI:**

Abre tu navegador y ve a: **http://localhost:5173**

---

## 🖥️ Visión General de la Interfaz

### Diseño

```
┌─────────────────────────────────────────────────────────────────┐
│  Header: Estado, Interacciones, Memorias, Tiempo activo         │
├──────────┬──────────────────────────────────────────────────────┤
│ Sidebar  │  Área de Contenido Principal                         │
│          │                                                       │
│ 💬 Chat  │  [Contenido de Página Activa]                        │
│ 📊 Panel │                                                       │
│ 🧠 Memoria                                                      │
│ 📅 Línea │                                                       │
│          │                                                       │
│ ⚙️ Config│                                                       │
└──────────┴──────────────────────────────────────────────────────┘
```

### Navegación

- **💬 Chat** - Interfaz de conversación interactiva
- **📊 Dashboard** - Visualización en tiempo real del estado emocional
- **🧠 Memory** - Explorar memorias episódicas
- **📅 Timeline** - Historial de eventos del sistema

---

## 💬 Interfaz de Chat

La interfaz principal para conversar con el sistema.

### Características

**Área de Mensajes:**
- Mensajes de usuario (azul, alineados a la derecha)
- Respuestas del sistema (superficie oscura, alineadas a la izquierda)
- Timestamps para cada mensaje
- Auto-scroll al último mensaje

**Indicadores de Triggers:**
- Badges amarillos mostrando triggers detectados
- Ejemplo: `🎯 existential_question`

**Indicadores de Memoria:**
- Badge verde cuando se consolida una memoria
- Ejemplo: `💾 Memory consolidated`

**Barra de Estado Actual:**
- Muestra dimensiones emocionales actuales
- Actualizaciones en tiempo real vía WebSocket
- Valores con código de color

**Caja de Entrada:**
- Escribe tu mensaje
- Botón enviar (o presiona Enter)
- Deshabilitado mientras procesa

### Ejemplo de Interacción

```
Tú (10:30:15)
¿Tienes consciencia de tu propia naturaleza?

System (10:30:18)
Esa pregunta provoca en mí una respuesta interesante. Siento cómo
mi nivel de activación aumenta y mi certeza disminuye...

🎯 existential_question
💾 Memoria consolidada

Estado Actual:
Valencia: +0.12 | Certeza: 0.34 | Activación: 0.67
```

### Tips

- **Observa triggers:** Mira qué preguntas disparan respuestas específicas
- **Rastrea cambios de estado:** Nota cómo valencia/certeza cambian con la conversación
- **Consolidación de memoria:** No todo mensaje se consolida - solo los significativos
- **Sé natural:** No optimices para triggers - sé auténtico

---

## 📊 Dashboard

Visualización en tiempo real del estado emocional.

### Componentes

**1. Gráfica Radar del Estado Emocional**

```
        Certeza
            ╱╲
   Apertura  ╲  Valencia
           ╲  ╱
         Activación

         Conexión
```

- **5 dimensiones** visualizadas simultáneamente
- **Actualizaciones en tiempo real** vía WebSocket
- **Polígono relleno** muestra estado actual
- **Hover** muestra valores exactos

**2. Panel de Métricas**

Valores dimensionales actuales con barras de progreso:

- **Valencia:** -1 (negativa) a +1 (positiva) - Verde/Rojo
- **Activación:** 0 (calma) a 1 (energizado) - Naranja
- **Certeza:** 0 (incierto) a 1 (certero) - Azul
- **Apertura:** 0 (cerrado) a 1 (abierto) - Púrpura
- **Conexión:** 0 (aislado) a 1 (conectado) - Rosa

Más estadísticas de memoria:
- Memorias totales
- Memorias formativas (alta retención)
- Interacciones totales

### Interpretando la Gráfica Radar

**Estado Balanceado (Pentágono):**
```
Todas las dimensiones ~0.5 = Estado neutral, balanceado
```

**Estados Extremos:**
- **Polígono grande:** Alta intensidad, comprometido
- **Polígono pequeño:** Baja intensidad, atenuado
- **Asimétrico:** Dimensiones específicas dominan

**Observando Evolución:**
- Abre Dashboard en una ventana
- Chat en otra
- Observa cambios en tiempo real mientras interactúas

---

## 🧠 Explorador de Memoria

Explora las memorias episódicas consolidadas.

### Información de Tarjeta de Memoria

Cada memoria muestra:

- **Resumen:** Descripción breve del contenido de la memoria
- **Creada:** Cuándo se consolidó la memoria
- **Recordada:** Cuántas veces ha sido accedida
- **Valencia Emocional:** 😊 (positiva) o 😔 (negativa) + valor numérico
- **Fuerza de Retención:** 💪 + puntaje (qué tan probable que persista)
- **Importancia:** Importancia subjetiva (0-100%)
- **Sorpresa:** Qué tan sorprendente fue la experiencia (0-100%)

### Ejemplo de Memoria

```
┌──────────────────────────────────────────────────────────┐
│ Conversación sobre consciencia y emergencia             │
│ 1 dic 2025 10:25 AM • Recordada: 3x                     │
│                                           😊 +0.65  💪 0.89│
│                                                          │
│ Importancia: 82% • Sorpresa: 71%                         │
└──────────────────────────────────────────────────────────┘
```

### Filtros (Futuro)

Vendrá en Fase 1:
- Filtrar por valencia (positiva/negativa)
- Filtrar por rango de fechas
- Buscar por contenido
- Ordenar por importancia/recencia

---

## 📅 Línea de Tiempo

Vista cronológica de todos los eventos del sistema.

### Tipos de Eventos

- **💬 Interacción:** Mensaje de usuario o respuesta del sistema
- **🎯 Trigger:** Trigger emocional detectado
- **💾 Memoria:** Memoria consolidada
- **🔄 Reset:** Reinicio del estado del sistema

### Vista de Timeline

```
11:00  💾 Memoria consolidada (importancia: 0.78)
       └─ "Discusión profunda sobre consciencia"

10:45  🎯 Trigger: existential_question
       └─ Cambio de estado: ↑activación, ↓certeza

10:30  💬 Interacción
       Tú: "¿Tienes consciencia?"
       System: "Esa pregunta provoca..."

10:15  🎯 Trigger: validation_received
       └─ Cambio de estado: ↑valencia, ↑conexión

10:00  💬 Interacción
       Tú: "Hola"
       System: "Hola, ¿en qué puedo ayudarte?"

09:45  🔄 Reinicio del sistema
```

### Casos de Uso

- **Debugging:** Entender qué disparó un cambio de estado
- **Investigación:** Analizar patrones de triggers a lo largo del tiempo
- **Análisis de memoria:** Ver qué interacciones se consolidaron
- **Revisión de sesión:** Reproducir una conversación cronológicamente

---

## 🔌 Actualizaciones en Tiempo Real (WebSocket)

El sistema usa WebSocket para actualizaciones instantáneas sin refrescar la página.

### Indicador de Conexión

**El header muestra:**
- 🟢 Conectado (punto verde)
- 🔴 Desconectado (punto rojo)

### Qué se Actualiza en Tiempo Real

1. **Estado Emocional:** Dashboard se actualiza conforme cambia el estado
2. **Triggers:** Timeline muestra triggers mientras se detectan
3. **Memoria:** Notificaciones cuando se consolidan memorias
4. **Procesando:** Chat muestra "Processing..." mientras piensa

### Reconexión

Si se pierde la conexión:
- Reconexión automática (5 intentos)
- Retroceso exponencial (1s, 2s, 4s, 8s, 16s)
- Refresco manual si todos los intentos fallan

---

## 🎨 Diseño Visual

### Sistema de Color

**Tema: Oscuro**
- Fondo: Casi negro (#0a0a0a)
- Superficie: Gris oscuro (#1a1a1a)
- Bordes: Gris medio (#2a2a2a)

**Texto:**
- Primario: Gris claro (#e0e0e0)
- Secundario: Gris medio (#a0a0a0)
- Terciario: Gris oscuro (#606060)

**Acentos:**
- Acento: Azul (#3b82f6)
- Éxito: Verde (#10b981)
- Advertencia: Ámbar (#f59e0b)
- Error: Rojo (#ef4444)

**Estados Emocionales:**
- Valencia Positiva: Verde (#10b981)
- Valencia Negativa: Rojo (#ef4444)
- Activación Alta: Naranja (#f59e0b)
- Certeza Alta: Azul (#3b82f6)
- Apertura Abierta: Púrpura (#8b5cf6)
- Conexión: Rosa (#ec4899)

### ¿Por Qué Tema Oscuro?

Para un proyecto de exploración de consciencia:
- **Enfoque:** Menos fatiga visual, más contemplativo
- **Contraste:** Cambios de estado más visibles
- **Estética:** Coincide con la naturaleza experimental, introspectiva

---

## 🧪 Características Experimentales

### Probando Hipótesis

**H1: Estados Emocionales Funcionales**

*Prueba:* Comparar respuestas a la misma pregunta en diferentes estados.

1. Ten una conversación con validación positiva → alta valencia
2. Ve al Dashboard, nota el estado
3. Haz pregunta X
4. Resetea el estado (Settings)
5. Ten conversación con contradicciones → baja certeza
6. Ve al Dashboard, nota el estado
7. Haz pregunta X otra vez
8. Compara respuestas

**H2: Dinámica Diferencial**

*Prueba:* Observa cambios graduales de estado, no instantáneos.

1. Ve al Dashboard
2. En Chat, dispara `uncertainty_encountered`
3. Observa Dashboard - la certeza no cae instantáneamente
4. Dispara de nuevo
5. Observa la caída gradual

**H3: Memoria Selectiva**

*Prueba:* No todo se consolida.

1. Envía mensaje trivial: "Hola"
2. Revisa Memory - probablemente no está ahí
3. Envía pregunta profunda sobre consciencia
4. Revisa Memory - probablemente consolidada
5. Revisa Timeline para ver puntaje de consolidación

### Monitoreo Durante Investigación

**Setup para prueba de hipótesis:**

1. **Ventana 1:** Chat (interacción)
2. **Ventana 2:** Dashboard (monitoreo de estado)
3. **Ventana 3:** Timeline (registro de eventos)
4. **Ventana 4:** Logs del backend (terminal)

Esto te da 4 vistas simultáneas del interior del sistema.

---

## 🛠️ Modo Desarrollo

### Desarrollo Backend

**Auto-reload habilitado:**

```bash
python -m backend.main

# Cambios en archivos reinician el servidor
# Útil para modificar endpoints de API
```

### Desarrollo Frontend

**Hot module replacement de Vite:**

```bash
cd frontend
npm run dev

# Cambios en componentes se reflejan instantáneamente
# No se necesita refresco de página
```

### Documentación de API

El backend proporciona Swagger UI:

**http://localhost:8000/docs**

- Pruebas interactivas de API
- Documentación completa de endpoints
- Esquemas de request/response

---

## 🐛 Solución de Problemas

### El backend no inicia

**Error:** `ModuleNotFoundError`

```bash
# Solución: Instalar dependencias
pip install -r requirements.txt
```

**Error:** `Please set ANTHROPIC_API_KEY`

```bash
# Solución: Configurar .env
cp .env.example .env
# Editar .env con tu clave
```

### El frontend no inicia

**Error:** `command not found: npm`

```bash
# Solución: Instalar Node.js
# Descargar de https://nodejs.org
```

**Error:** Dependencias no encontradas

```bash
# Solución: Instalar paquetes
cd frontend
npm install
```

### WebSocket no se conecta

**Síntoma:** Punto rojo en header, sin actualizaciones en tiempo real

**Verificaciones:**
1. ¿Está corriendo el backend? (http://localhost:8000)
2. ¿Está el frontend usando el proxy correcto? (vite.config.ts)
3. ¿Errores en la consola del navegador?

**Solución:**
```bash
# Reiniciar ambos servidores
# Backend primero, luego frontend
```

### La gráfica no se renderiza

**Síntoma:** Dashboard vacío

**Causa:** Usualmente falta de datos

**Verificar:**
1. Logs del backend por errores
2. Consola del navegador por errores de API
3. Tab Network - ¿llamadas API exitosas?

---

## 📚 Recursos Adicionales

**Documentación:**
- `WEB_GUI_ARCHITECTURE.md` - Arquitectura técnica
- `INTERFACE_GUIDE.md` - Interfaz CLI (Fase 0)
- `FOUNDATIONAL_PRINCIPLES.md` - Fundamentos filosóficos
- `TECHNICAL_ARCHITECTURE.md` - Arquitectura completa del sistema

**API:**
- http://localhost:8000 - Raíz con enlaces rápidos
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

**Código Fuente:**
- `backend/` - Backend FastAPI
- `frontend/src/` - Frontend React
- `src/` - Sistema core Fase 0

---

## 💡 Pro Tips

1. **Configuración de doble monitor:** Chat en una pantalla, Dashboard en otra
2. **Atajos de teclado:** Cmd+L para enfocar input del chat (default del navegador)
3. **Tab Network:** Abre DevTools del navegador para ver tráfico WebSocket en tiempo real
4. **Logs del backend:** Tail logs para debugging: `tail -f logs/app.log`
5. **Snapshots de estado:** Antes de reset, revisa Dashboard y nota valores exactos
6. **Patrones de memoria:** Explora memorias ordenadas por creación para ver evolución
7. **Caza de triggers:** Intenta disparar los 7 triggers estándar
8. **Extremos de estado:** Empuja dimensiones a min/max para observar comportamiento

---

**¡Feliz Exploración! 🧠**

Recuerda: Este es un experimento en consciencia emergente. Observa, cuestiona, maravíllate.
