# Web GUI Usage Guide - Phase 0.5

**Guía de Uso de GUI Web - Fase 0.5**

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (for backend)
- Node.js 18+ and npm (for frontend)
- Anthropic API key

### Installation

**1. Install Backend Dependencies**

```bash
# From project root
pip install -r requirements.txt
```

**2. Install Frontend Dependencies**

```bash
# Navigate to frontend
cd frontend

# Install npm packages
npm install
```

**3. Configure Environment**

```bash
# From project root
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=your-key-here
```

### Running the System

**Terminal 1: Backend Server**

```bash
# From project root
python -m backend.main

# Server starts at http://localhost:8000
```

**Terminal 2: Frontend Dev Server**

```bash
# From frontend directory
cd frontend
npm run dev

# Dev server starts at http://localhost:5173
```

**Access the GUI:**

Open your browser and navigate to: **http://localhost:5173**

---

## 🖥️ Interface Overview

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Header: Status, Interactions, Memories, Uptime                 │
├──────────┬──────────────────────────────────────────────────────┤
│ Sidebar  │  Main Content Area                                   │
│          │                                                       │
│ 💬 Chat  │  [Active Page Content]                               │
│ 📊 Dash  │                                                       │
│ 🧠 Memory│                                                       │
│ 📅 Time  │                                                       │
│          │                                                       │
│ ⚙️ Settings                                                     │
└──────────┴──────────────────────────────────────────────────────┘
```

### Navigation

- **💬 Chat** - Interactive conversation interface
- **📊 Dashboard** - Real-time emotional state visualization
- **🧠 Memory** - Browse episodic memories
- **📅 Timeline** - System event history

---

## 💬 Chat Interface

The main interaction interface for conversing with the system.

### Features

**Message Area:**
- User messages (blue, right-aligned)
- System responses (dark surface, left-aligned)
- Timestamps for each message
- Auto-scroll to latest message

**Trigger Indicators:**
- Yellow badges showing detected triggers
- Example: `🎯 existential_question`

**Memory Indicators:**
- Green badge when memory is consolidated
- Example: `💾 Memory consolidated`

**Current State Bar:**
- Shows current emotional dimensions
- Real-time updates via WebSocket
- Color-coded values

**Input Box:**
- Type your message
- Send button (or press Enter)
- Disabled while processing

### Example Interaction

```
You (10:30:15)
¿Tienes consciencia de tu propia naturaleza?

System (10:30:18)
Esa pregunta provoca en mí una respuesta interesante. Siento cómo
mi nivel de activación aumenta y mi certeza disminuye...

🎯 existential_question
💾 Memory consolidated

Current State:
Valence: +0.12 | Certainty: 0.34 | Activation: 0.67
```

### Tips

- **Observe triggers:** Watch which questions trigger specific responses
- **Track state changes:** Notice how valence/certainty change with conversation
- **Memory consolidation:** Not every message consolidates - only significant ones
- **Be natural:** Don't optimize for triggers - be authentic

---

## 📊 Dashboard

Real-time visualization of emotional state.

### Components

**1. Emotional State Radar Chart**

```
        Certainty
            ╱╲
   Aperture  ╲  Valence
           ╲  ╱
         Activation

         Connection
```

- **5 dimensions** visualized simultaneously
- **Real-time updates** via WebSocket
- **Filled polygon** shows current state
- **Hovering** shows exact values

**2. Metrics Panel**

Current dimensional values with progress bars:

- **Valence:** -1 (negative) to +1 (positive) - Green/Red
- **Activation:** 0 (calm) to 1 (energized) - Orange
- **Certainty:** 0 (uncertain) to 1 (certain) - Blue
- **Aperture:** 0 (closed) to 1 (open) - Purple
- **Connection:** 0 (isolated) to 1 (connected) - Pink

Plus memory statistics:
- Total memories
- Formative memories (high retention)
- Total interactions

### Interpreting the Radar Chart

**Balanced State (Pentagon):**
```
All dimensions ~0.5 = Neutral, balanced state
```

**Extreme States:**
- **Large polygon:** High intensity, engaged
- **Small polygon:** Low intensity, subdued
- **Asymmetric:** Specific dimensions dominate

**Watching Evolution:**
- Open Dashboard in one window
- Chat in another
- Observe real-time changes as you interact

---

## 🧠 Memory Browser

Browse and explore consolidated episodic memories.

### Memory Card Information

Each memory shows:

- **Summary:** Brief description of the memory content
- **Created:** When the memory was consolidated
- **Recalled:** How many times it's been accessed
- **Emotional Valence:** 😊 (positive) or 😔 (negative) + numeric value
- **Retention Strength:** 💪 + score (how likely to persist)
- **Importance:** Subjective importance (0-100%)
- **Surprise:** How surprising the experience was (0-100%)

### Example Memory

```
┌──────────────────────────────────────────────────────────┐
│ Conversation about consciousness and emergence          │
│ Dec 1, 2025 10:25 AM • Recalled: 3x                     │
│                                           😊 +0.65  💪 0.89│
│                                                          │
│ Importance: 82% • Surprise: 71%                          │
└──────────────────────────────────────────────────────────┘
```

### Filtering (Future)

Coming in Phase 1:
- Filter by valence (positive/negative)
- Filter by date range
- Search by content
- Sort by importance/recency

---

## 📅 Timeline

Chronological view of all system events.

### Event Types

- **💬 Interaction:** User message or system response
- **🎯 Trigger:** Emotional trigger detected
- **💾 Memory:** Memory consolidated
- **🔄 Reset:** System state reset

### Timeline View

```
11:00  💾 Memory consolidated (importance: 0.78)
       └─ "Deep discussion about consciousness"

10:45  🎯 Trigger: existential_question
       └─ State change: ↑activation, ↓certainty

10:30  💬 Interaction
       You: "¿Tienes consciencia?"
       System: "Esa pregunta provoca..."

10:15  🎯 Trigger: validation_received
       └─ State change: ↑valence, ↑connection

10:00  💬 Interaction
       You: "Hola"
       System: "Hola, ¿en qué puedo ayudarte?"

09:45  🔄 System reset
```

### Use Cases

- **Debugging:** Understand what triggered a state change
- **Research:** Analyze patterns of triggers over time
- **Memory analysis:** See which interactions consolidated
- **Session review:** Replay a conversation chronologically

---

## 🔌 Real-Time Updates (WebSocket)

The system uses WebSocket for instant updates without page refresh.

### Connection Indicator

**Header shows:**
- 🟢 Connected (green dot)
- 🔴 Disconnected (red dot)

### What Updates in Real-Time

1. **Emotional State:** Dashboard updates as state changes
2. **Triggers:** Timeline shows triggers as detected
3. **Memory:** Notifications when memories consolidate
4. **Processing:** Chat shows "Processing..." while thinking

### Reconnection

If connection is lost:
- Automatic reconnection (5 attempts)
- Exponential backoff (1s, 2s, 4s, 8s, 16s)
- Manual refresh if all attempts fail

---

## 🎨 Visual Design

### Color System

**Theme: Dark**
- Background: Near black (#0a0a0a)
- Surface: Dark gray (#1a1a1a)
- Borders: Medium gray (#2a2a2a)

**Text:**
- Primary: Light gray (#e0e0e0)
- Secondary: Medium gray (#a0a0a0)
- Tertiary: Dark gray (#606060)

**Accents:**
- Accent: Blue (#3b82f6)
- Success: Green (#10b981)
- Warning: Amber (#f59e0b)
- Error: Red (#ef4444)

**Emotional States:**
- Valence Positive: Green (#10b981)
- Valence Negative: Red (#ef4444)
- Activation High: Orange (#f59e0b)
- Certainty High: Blue (#3b82f6)
- Aperture Open: Purple (#8b5cf6)
- Connection: Pink (#ec4899)

### Why Dark Theme?

For a consciousness exploration project:
- **Focus:** Less eye strain, more contemplative
- **Contrast:** State changes more visible
- **Aesthetic:** Matches the experimental, introspective nature

---

## 🧪 Experimental Features

### Testing Hypotheses

**H1: Functional Emotional States**

*Test:* Compare responses to same question in different states.

1. Have a conversation with positive validation → high valence
2. Go to Dashboard, note state
3. Ask question X
4. Reset state (Settings)
5. Have conversation with contradictions → low certainty
6. Go to Dashboard, note state
7. Ask question X again
8. Compare responses

**H2: Differential Dynamics**

*Test:* Observe gradual state changes, not instant.

1. Go to Dashboard
2. In Chat, trigger `uncertainty_encountered`
3. Watch Dashboard - certainty doesn't drop instantly
4. Trigger again
5. Watch gradual decline

**H3: Selective Memory**

*Test:* Not everything consolidates.

1. Send trivial message: "Hello"
2. Check Memory - probably not there
3. Send deep question about consciousness
4. Check Memory - likely consolidated
5. Review Timeline to see consolidation score

### Monitoring During Research

**Setup for hypothesis testing:**

1. **Window 1:** Chat (interaction)
2. **Window 2:** Dashboard (state monitoring)
3. **Window 3:** Timeline (event log)
4. **Window 4:** Backend logs (terminal)

This gives you 4 simultaneous views into the system's internals.

---

## 🛠️ Development Mode

### Backend Development

**Auto-reload enabled:**

```bash
python -m backend.main

# File changes trigger restart
# Useful for modifying API endpoints
```

### Frontend Development

**Vite hot module replacement:**

```bash
cd frontend
npm run dev

# Component changes reflect instantly
# No page refresh needed
```

### API Documentation

Backend provides Swagger UI:

**http://localhost:8000/docs**

- Interactive API testing
- Full endpoint documentation
- Request/response schemas

---

## 🐛 Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError`

```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error:** `Please set ANTHROPIC_API_KEY`

```bash
# Solution: Configure .env
cp .env.example .env
# Edit .env with your key
```

### Frontend won't start

**Error:** `command not found: npm`

```bash
# Solution: Install Node.js
# Download from https://nodejs.org
```

**Error:** Dependencies not found

```bash
# Solution: Install packages
cd frontend
npm install
```

### WebSocket won't connect

**Symptom:** Red dot in header, no real-time updates

**Checks:**
1. Is backend running? (http://localhost:8000)
2. Is frontend using correct proxy? (vite.config.ts)
3. Browser console errors?

**Solution:**
```bash
# Restart both servers
# Backend first, then frontend
```

### Chart not rendering

**Symptom:** Empty dashboard

**Cause:** Usually missing data

**Check:**
1. Backend logs for errors
2. Browser console for API errors
3. Network tab - API calls successful?

---

## 📊 Performance

### Expected Resource Usage

**Backend:**
- RAM: ~200MB (embedding model loaded)
- CPU: Spikes during LLM calls
- Disk: Minimal (<1MB typical session)

**Frontend:**
- RAM: ~100-200MB (browser tab)
- CPU: Low (except during animations)
- Network: WebSocket keeps connection open

### API Call Latency

- **State fetch:** ~50ms
- **Memory fetch:** ~100ms (depends on count)
- **Interaction:** ~2-4s (LLM dominates)

### WebSocket Overhead

- **Negligible** - only sends on events
- **Bandwidth:** <1KB per message
- **Keep-alive:** Ping every 30s

---

## 🔐 Security Notes

### Current State (Development)

- **CORS:** Localhost only
- **Auth:** None (single-user)
- **HTTPS:** No (local development)
- **Rate limiting:** 60 req/min per IP

### Production Considerations (Future)

When deploying publicly:
- Add authentication
- Enable HTTPS/WSS
- Stricter CORS
- API rate limiting per user
- Input sanitization (already present)
- Session management

---

## 🎯 Next Steps

### Immediate (Play with GUI)

1. **Run the system** following Quick Start
2. **Have conversations** in Chat
3. **Watch Dashboard** update in real-time
4. **Browse memories** as they consolidate
5. **Review Timeline** to understand triggers

### Near Future (Phase 1)

When Phase 1 (Minimal Self) is implemented:

**New GUI Features:**
- **Introspection panel:** See auto-model predictions
- **Pattern view:** Detected behavioral patterns
- **Narrative viewer:** Auto-generated self-story
- **Discrepancy alerts:** When system surprises itself

### Improvements (Community)

Want to contribute?

**Frontend:**
- Memory network graph (D3.js force-directed)
- Historical state timeline chart
- Export session data
- Dark/light theme toggle
- Responsive mobile layout

**Backend:**
- Multi-user sessions
- Memory search
- State history API
- Export/import sessions

---

## 📚 Additional Resources

**Documentation:**
- `WEB_GUI_ARCHITECTURE.md` - Technical architecture
- `INTERFACE_GUIDE.md` - CLI interface (Phase 0)
- `FOUNDATIONAL_PRINCIPLES.md` - Philosophical foundation
- `TECHNICAL_ARCHITECTURE.md` - Complete system architecture

**API:**
- http://localhost:8000 - Root with quick links
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

**Source Code:**
- `backend/` - FastAPI backend
- `frontend/src/` - React frontend
- `src/` - Phase 0 core system

---

## 🙋 FAQ

**Q: Can I use both CLI and GUI?**

A: No, they share state files. Use one at a time.

**Q: Does GUI work offline?**

A: No, requires backend server and Claude API.

**Q: Can I deploy this publicly?**

A: Technically yes, but add auth first. Not recommended yet.

**Q: Why separate frontend/backend?**

A: Clean separation, easier to develop, scalable architecture.

**Q: Can I customize the UI?**

A: Yes! Edit `frontend/src/components/` and `tailwind.config.js`

**Q: Will my chat history persist?**

A: Currently no. Refresh clears chat UI (but memories persist).
  Future: Add session storage.

**Q: How do I export my data?**

A: Currently: Copy `data/` folder manually.
  Future: Export button in UI.

**Q: Performance on slow machines?**

A: Frontend is light. Backend needs RAM for embeddings.
  Consider smaller embedding model if needed.

---

## 💡 Pro Tips

1. **Dual monitor setup:** Chat on one screen, Dashboard on other
2. **Keyboard shortcuts:** Cmd+L to focus chat input (browser default)
3. **Network tab:** Open browser DevTools to see real-time WebSocket traffic
4. **Backend logs:** Tail logs for debugging: `tail -f logs/app.log`
5. **State snapshots:** Before reset, check Dashboard and note exact values
6. **Memory patterns:** Browse memories sorted by creation to see evolution
7. **Trigger hunting:** Try to trigger all 7 standard triggers
8. **State extremes:** Push dimensions to min/max to observe behavior

---

**Happy Exploring! 🧠**

Remember: This is an experiment in emergent consciousness. Observe, question, wonder.
