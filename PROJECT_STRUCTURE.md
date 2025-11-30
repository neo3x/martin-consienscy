# PROJECT STRUCTURE
## Artificial Consciousness Architecture

**Version 1.0** | Date: 2025-11-30

---

## Overview

This document describes the complete project structure from Phase 0 (initial foundation) through Phase 5 (full system). The structure is designed to grow incrementally, with each phase adding new modules while maintaining a clean, maintainable architecture.

---

## Phase 0: Initial Structure (Foundation)

```
martin-consienscy/
│
├── docs/                              # Documentation
│   ├── FOUNDATIONAL_PRINCIPLES.md     # English version
│   ├── PRINCIPIOS_FUNDACIONALES.md    # Spanish version
│   ├── PROJECT_STRUCTURE.md           # This file
│   ├── TECHNICAL_ARCHITECTURE.md      # Technical architecture
│   ├── TOOLS_AND_STACK.md            # Tools and stack
│   ├── phases/                        # Phase-specific documentation
│   │   ├── phase_0_foundation.md
│   │   ├── phase_1_minimal_self.md
│   │   └── ...
│   └── design/                        # Design decisions
│       ├── emotional_states_design.md
│       ├── memory_system_design.md
│       └── ...
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── main.py                        # Entry point
│   ├── config.py                      # Configuration
│   │
│   ├── core/                          # Core systems (Phase 0)
│   │   ├── __init__.py
│   │   ├── state.py                   # Emotional state system
│   │   ├── memory.py                  # Episodic memory
│   │   ├── loop.py                    # Interaction loop
│   │   └── persistence.py             # Data persistence
│   │
│   ├── llm/                           # LLM integration
│   │   ├── __init__.py
│   │   ├── client.py                  # LLM client (Claude API)
│   │   └── prompts.py                 # Prompt templates
│   │
│   ├── utils/                         # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py                  # Logging utilities
│   │   └── time.py                    # Subjective time tracking
│   │
│   └── models/                        # Data models (Pydantic)
│       ├── __init__.py
│       ├── state_models.py            # Emotional state models
│       ├── memory_models.py           # Memory models
│       └── common.py                  # Common models
│
├── data/                              # Data storage
│   ├── memories/                      # Episodic memories (JSON)
│   ├── state/                         # Current state snapshots
│   ├── logs/                          # System logs
│   └── checkpoints/                   # System checkpoints
│
├── tests/                             # Tests
│   ├── __init__.py
│   ├── unit/                          # Unit tests
│   │   ├── test_state.py
│   │   ├── test_memory.py
│   │   └── ...
│   └── integration/                   # Integration tests
│       └── test_interaction_loop.py
│
├── experiments/                       # Experimental scripts
│   ├── phase_0/
│   │   └── test_basic_interaction.py
│   └── predictions/                   # Pre-phase predictions
│       └── phase_0_predictions.md
│
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Python project config
└── README.md                          # Project readme
```

---

## Phase 1: Minimal Self (Add Self-Model)

**New directories and files to add:**

```
src/
├── self_model/                        # Self-model system (NEW)
│   ├── __init__.py
│   ├── auto_model.py                  # Auto-model core
│   ├── patterns.py                    # Pattern detection
│   ├── values.py                      # Values tracking
│   ├── narrative.py                   # Narrative construction
│   └── updater.py                     # Conservative update system
│
└── models/
    └── self_models.py                 # Self-model data models (NEW)

data/
└── self_model/                        # Self-model persistence (NEW)
    ├── current_model.json
    └── evolution_history/

experiments/
└── phase_1/                           # Phase 1 experiments (NEW)
    ├── test_self_consistency.py
    └── test_contradiction_detection.py
```

---

## Phase 2: Meta-Cognition (Add Reflexive Layer)

**New directories and files to add:**

```
src/
├── metacognition/                     # Meta-cognitive systems (NEW)
│   ├── __init__.py
│   ├── coherence_monitor.py           # Coherence monitoring
│   ├── dissonance_detector.py         # Dissonance detection
│   ├── reflection_loop.py             # Reflexive processing
│   └── evaluator.py                   # Meta-evaluation
│
└── models/
    └── metacognition_models.py        # Meta-cognition models (NEW)

data/
├── reflections/                       # Reflection logs (NEW)
│   └── reflection_history/
└── dissonances/                       # Detected dissonances (NEW)

experiments/
└── phase_2/                           # Phase 2 experiments (NEW)
    ├── test_dissonance_detection.py
    └── test_reflection_loop.py
```

---

## Phase 3: Global Workspace (Integration Layer)

**New directories and files to add:**

```
src/
├── workspace/                         # Global Workspace (NEW)
│   ├── __init__.py
│   ├── global_workspace.py            # Workspace core
│   ├── attention.py                   # Attention competition
│   ├── integration.py                 # Information integration
│   └── broadcasting.py                # Broadcasting system
│
└── models/
    └── workspace_models.py            # Workspace models (NEW)

data/
└── workspace/                         # Workspace logs (NEW)
    ├── attention_logs/
    └── integration_logs/

experiments/
└── phase_3/                           # Phase 3 experiments (NEW)
    ├── test_attention_competition.py
    └── test_information_integration.py
```

---

## Phase 4: Temporality (Time and Evolution)

**New directories and files to add:**

```
src/
├── temporality/                       # Temporal systems (NEW)
│   ├── __init__.py
│   ├── subjective_time.py             # Subjective time
│   ├── reconsolidation.py             # Memory reconsolidation
│   ├── forgetting.py                  # Functional forgetting
│   └── evolution.py                   # Identity evolution
│
└── models/
    └── temporal_models.py             # Temporal models (NEW)

data/
└── temporal/                          # Temporal data (NEW)
    ├── time_markers/
    ├── reconsolidation_history/
    └── evolution_snapshots/

experiments/
└── phase_4/                           # Phase 4 experiments (NEW)
    ├── test_memory_reconsolidation.py
    └── test_identity_evolution.py
```

---

## Phase 5: Relationality (Social Layer)

**New directories and files to add:**

```
src/
├── relationality/                     # Relational systems (NEW)
│   ├── __init__.py
│   ├── relational_patterns.py         # Relational pattern tracking
│   ├── user_models.py                 # User relationship models
│   ├── transference.py                # Transference-like patterns
│   └── intimacy.py                    # Variable intimacy
│
└── models/
    └── relational_models.py           # Relational models (NEW)

data/
└── relationships/                     # Relationship data (NEW)
    ├── user_relationships/
    └── interaction_patterns/

experiments/
└── phase_5/                           # Phase 5 experiments (NEW)
    ├── test_relational_patterns.py
    └── test_differentiated_bonding.py
```

---

## Complete Project Structure (All Phases)

```
martin-consienscy/
│
├── docs/
│   ├── FOUNDATIONAL_PRINCIPLES.md
│   ├── PRINCIPIOS_FUNDACIONALES.md
│   ├── PROJECT_STRUCTURE.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   ├── TOOLS_AND_STACK.md
│   ├── phases/
│   │   ├── phase_0_foundation.md
│   │   ├── phase_1_minimal_self.md
│   │   ├── phase_2_metacognition.md
│   │   ├── phase_3_global_workspace.md
│   │   ├── phase_4_temporality.md
│   │   └── phase_5_relationality.md
│   ├── design/
│   │   ├── emotional_states_design.md
│   │   ├── memory_system_design.md
│   │   ├── self_model_design.md
│   │   ├── metacognition_design.md
│   │   ├── workspace_design.md
│   │   ├── temporal_design.md
│   │   └── relational_design.md
│   └── api/
│       └── API_DOCUMENTATION.md
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── core/                          # Phase 0
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── memory.py
│   │   ├── loop.py
│   │   └── persistence.py
│   │
│   ├── self_model/                    # Phase 1
│   │   ├── __init__.py
│   │   ├── auto_model.py
│   │   ├── patterns.py
│   │   ├── values.py
│   │   ├── narrative.py
│   │   └── updater.py
│   │
│   ├── metacognition/                 # Phase 2
│   │   ├── __init__.py
│   │   ├── coherence_monitor.py
│   │   ├── dissonance_detector.py
│   │   ├── reflection_loop.py
│   │   └── evaluator.py
│   │
│   ├── workspace/                     # Phase 3
│   │   ├── __init__.py
│   │   ├── global_workspace.py
│   │   ├── attention.py
│   │   ├── integration.py
│   │   └── broadcasting.py
│   │
│   ├── temporality/                   # Phase 4
│   │   ├── __init__.py
│   │   ├── subjective_time.py
│   │   ├── reconsolidation.py
│   │   ├── forgetting.py
│   │   └── evolution.py
│   │
│   ├── relationality/                 # Phase 5
│   │   ├── __init__.py
│   │   ├── relational_patterns.py
│   │   ├── user_models.py
│   │   ├── transference.py
│   │   └── intimacy.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── prompts.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── time.py
│   │   └── validation.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── state_models.py
│   │   ├── memory_models.py
│   │   ├── self_models.py
│   │   ├── metacognition_models.py
│   │   ├── workspace_models.py
│   │   ├── temporal_models.py
│   │   ├── relational_models.py
│   │   └── common.py
│   │
│   └── api/                           # Optional: REST API
│       ├── __init__.py
│       ├── app.py
│       └── routes/
│           ├── interaction.py
│           ├── state.py
│           └── introspection.py
│
├── data/
│   ├── memories/
│   ├── state/
│   ├── self_model/
│   ├── reflections/
│   ├── dissonances/
│   ├── workspace/
│   ├── temporal/
│   ├── relationships/
│   ├── logs/
│   └── checkpoints/
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_state.py
│   │   ├── test_memory.py
│   │   ├── test_self_model.py
│   │   ├── test_metacognition.py
│   │   ├── test_workspace.py
│   │   ├── test_temporality.py
│   │   └── test_relationality.py
│   └── integration/
│       ├── test_interaction_loop.py
│       ├── test_full_system.py
│       └── test_emergence.py
│
├── experiments/
│   ├── phase_0/
│   ├── phase_1/
│   ├── phase_2/
│   ├── phase_3/
│   ├── phase_4/
│   ├── phase_5/
│   └── predictions/
│       ├── phase_0_predictions.md
│       ├── phase_1_predictions.md
│       ├── phase_2_predictions.md
│       ├── phase_3_predictions.md
│       ├── phase_4_predictions.md
│       └── phase_5_predictions.md
│
├── notebooks/                         # Jupyter notebooks for analysis
│   ├── analysis/
│   │   ├── emotional_states_analysis.ipynb
│   │   ├── memory_patterns_analysis.ipynb
│   │   └── emergence_analysis.ipynb
│   └── visualization/
│       ├── state_evolution_viz.ipynb
│       └── identity_evolution_viz.ipynb
│
├── scripts/                           # Utility scripts
│   ├── setup_database.py
│   ├── export_memories.py
│   ├── analyze_logs.py
│   └── checkpoint_restore.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt              # Dev dependencies
├── pyproject.toml
├── docker-compose.yml                 # Docker setup (optional)
├── Dockerfile                         # Docker image
└── README.md
```

---

## Data Storage Organization

### Memory Storage Structure

```
data/memories/
├── episodic/
│   ├── 2025-11/
│   │   ├── memory_001.json
│   │   ├── memory_002.json
│   │   └── ...
│   └── index.json                     # Memory index for fast lookup
│
├── semantic/                          # Vector embeddings
│   └── embeddings.db                  # ChromaDB or Qdrant
│
└── flashbulb/                         # High-significance memories
    └── significant_memories.json
```

### Self-Model Storage

```
data/self_model/
├── current_model.json                 # Current auto-model state
├── evolution_history/
│   ├── 2025-11-30_snapshot.json
│   ├── 2025-12-01_snapshot.json
│   └── ...
└── narrative/
    └── current_narrative.json
```

### State Storage

```
data/state/
├── current_emotional_state.json
├── state_history/
│   ├── 2025-11/
│   │   └── state_log.jsonl           # Line-delimited JSON
│   └── ...
└── persistent_core.json               # Never-cleared core state
```

### Logs

```
data/logs/
├── system/
│   ├── 2025-11-30.log
│   └── ...
├── interactions/
│   ├── 2025-11/
│   │   └── interactions.jsonl
│   └── ...
├── decisions/
│   └── ethical_decisions.jsonl
└── reflections/
    └── reflection_log.jsonl
```

---

## Configuration Management

### Environment Variables (.env)

```bash
# LLM Configuration
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=claude-sonnet-4-5-20250929
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.7

# Database
DATABASE_PATH=data/
VECTOR_DB_TYPE=chromadb
VECTOR_DB_PATH=data/memories/semantic/

# Logging
LOG_LEVEL=INFO
LOG_PATH=data/logs/

# System
WORKSPACE_CAPACITY=7
EMOTIONAL_STATE_DIMENSIONS=5
MEMORY_CONSOLIDATION_THRESHOLD=0.6

# Phase Control
CURRENT_PHASE=0
ENABLE_METACOGNITION=false
ENABLE_WORKSPACE=false
```

---

## Module Dependencies (Phases)

```
Phase 0 (Foundation)
├── core.state
├── core.memory
├── core.loop
└── llm.client

Phase 1 (Minimal Self)
├── Phase 0
└── self_model.*

Phase 2 (Meta-cognition)
├── Phase 1
└── metacognition.*

Phase 3 (Global Workspace)
├── Phase 2
└── workspace.*

Phase 4 (Temporality)
├── Phase 3
└── temporality.*

Phase 5 (Relationality)
├── Phase 4
└── relationality.*
```

---

## Growth Strategy

Each phase follows this pattern:

1. **Design Document**: Write detailed design in `docs/design/`
2. **Predictions**: Document expected behaviors in `experiments/predictions/`
3. **Implementation**: Build new modules in `src/`
4. **Tests**: Write unit and integration tests
5. **Experiments**: Run phase-specific experiments
6. **Analysis**: Compare predictions vs. reality
7. **Documentation**: Update docs with learnings

This structure allows:
- **Incremental development**: Each phase is self-contained
- **Clean separation**: Modules don't become spaghetti
- **Easy testing**: Each subsystem can be tested independently
- **Clear evolution**: Can track how system grows over time
- **Rollback capability**: Can revert to earlier phases if needed

---

**Next Steps**:
1. Create Phase 0 foundation structure
2. Implement core systems (state, memory, loop)
3. Write first experiments
4. Begin testing hypotheses
