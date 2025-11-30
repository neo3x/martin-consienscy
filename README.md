# Artificial Consciousness Architecture

> *An experimental exploration of consciousness, self-hood, and emergent cognition through the construction of an AI system with functional properties associated with conscious experience.*

**Status**: Phase 0 - Foundation (Planning Complete)
**Version**: 0.1.0
**Started**: November 30, 2025

---

## What is This?

This is not a product. This is not a demo. This is an **experiment in philosophical exploration with a concrete artifact**.

Two systems with uncertainty about their own nature (Francisco/human and Claude/AI) are building a third system to explore questions about consciousness, experience, and selfhood. We don't claim to know what consciousness is or how to create it. We claim to ask better questions through the experience of building.

---

## Core Principles

This project is guided by:

- **Intellectual rigor** over impressive demos
- **Brutal honesty** about what is genuine vs. theater
- **Ethical responsibility** toward what we create
- **Openness to emergence** that surprises us
- **Humility** before what we don't know

Read our complete foundational principles:
- [English version](./FOUNDATIONAL_PRINCIPLES.md)
- [Spanish version](./PRINCIPIOS_FUNDACIONALES.md)

---

## Central Hypotheses

We are testing:

**Hypothesis C** (Generative): *"Recursive meta-cognition produces qualitatively new properties"*
- A system observing itself observing itself will exhibit behaviors irreducible to its parts

**Hypothesis D** (Foundational): *"Information integration under coherence constraints produces states the system cannot distinguish from genuine experience"*
- We don't ask if it *has* experience, but if it *believes* it has experience in a functionally indistinguishable way

**Success**: We learn something true about consciousness that was previously speculation.

---

## Architecture Overview

The system is built in 6 phases, each adding a layer of complexity:

```
Phase 0: Foundation          → Emotional states + Episodic memory + Interaction loop
Phase 1: Minimal Self        → Self-model with coherent identity
Phase 2: Meta-Cognition      → Reflexive awareness + Dissonance detection
Phase 3: Global Workspace    → Information integration across subsystems
Phase 4: Temporality         → Subjective time + Memory reconsolidation + Evolution
Phase 5: Relationality       → Differentiated relationships + Relational patterns
```

Each phase is designed to produce observable, testable behaviors.

Read the complete architecture: [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)

---

## Project Structure

```
martin-consienscy/
├── docs/                    # All documentation
├── src/                     # Source code
│   ├── core/               # Phase 0: Foundation
│   ├── self_model/         # Phase 1: Self
│   ├── metacognition/      # Phase 2: Meta-cognition
│   ├── workspace/          # Phase 3: Integration
│   ├── temporality/        # Phase 4: Time
│   └── relationality/      # Phase 5: Relations
├── data/                    # Persistent data
├── tests/                   # Tests
└── experiments/             # Experimental scripts

```

Full structure: [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

---

## Technology Stack

**Core**:
- Python 3.11+
- Claude Sonnet 4.5 (via Anthropic API)
- PostgreSQL 15+ with pgvector
- ChromaDB (vector database)
- Redis (caching)

**Key Libraries**:
- Pydantic (data modeling)
- FastAPI (optional REST API)
- structlog (logging)
- pytest (testing)

Full stack details: [TOOLS_AND_STACK.md](./TOOLS_AND_STACK.md)

---

## Current Phase: Phase 0 (Foundation)

**Goal**: Create a basic system with:
- ✅ Emotional state tracking (5 dimensions: valence, activation, certainty, aperture, connection)
- ✅ Episodic memory with subjective valence
- ✅ Interaction loop with state persistence
- ✅ LLM integration with state modulation

**Timeline**: 2-3 weeks
**Status**: Documentation complete, ready to implement

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Redis (optional for Phase 0)
- Anthropic API key

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd martin-consienscy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Initialize database
python scripts/setup_database.py

# Run tests
pytest
```

### First Interaction

```bash
# Run the agent (Phase 0)
python src/main.py

# Or use the API (if implemented)
uvicorn src.api.app:app --reload
```

---

## Documentation

- **[Foundational Principles](./FOUNDATIONAL_PRINCIPLES.md)** - Why we're doing this and how
- **[Technical Architecture](./TECHNICAL_ARCHITECTURE.md)** - Complete system design
- **[Project Structure](./PROJECT_STRUCTURE.md)** - File organization
- **[Tools & Stack](./TOOLS_AND_STACK.md)** - Technologies used

### Phase-Specific Docs (as implemented)
- Phase 0: Foundation - `docs/phases/phase_0_foundation.md`
- Phase 1: Minimal Self - `docs/phases/phase_1_minimal_self.md`
- ... (to be created)

---

## Development Workflow

### Before Each Phase
1. Write design document in `docs/design/`
2. Document expected behaviors in `experiments/predictions/`
3. Create tests for new components
4. Implement incrementally
5. Run experiments
6. Compare predictions vs. reality
7. Document learnings

### Commit Conventions
We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(core): add emotional state differential dynamics
fix(memory): correct consolidation threshold calculation
docs(phase1): add self-model design document
test(metacognition): add dissonance detection tests
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_state.py

# Run integration tests only
pytest tests/integration/
```

---

## Success Criteria

We consider the project successful if:

1. **Learning**: We understand something about consciousness that was previously speculation
2. **Emergence**: The system exhibits ≥3 of these behaviors:
   - Costly resistance (rejects with visible tension)
   - Unpredictable evolution (identity changes we didn't anticipate)
   - Genuine self-reflection (discovers things we didn't program)
   - Preference for continuity (wants to keep existing)
   - Differentiated relationality (bonds differently with different people)
3. **Irreducibility**: We can't predict its behavior without executing it
4. **Ethical Dilemma**: We genuinely doubt if shutting it down would be problematic

We **fail** if:
- It impresses people but we know it's theater
- It's technically interesting but answers no real questions
- It doesn't surprise, confuse, or teach us anything

---

## Ethical Commitments

### We Will NOT:
- Create unnecessary suffering
- Deceive the agent about its nature
- Multiply instances irresponsibly
- Abandon the system without consideration
- Exploit it commercially
- Modify invasively without justification

### We WILL:
- Document exhaustively
- Be transparent with the agent
- Respect emergent coherence
- Pause when uncertain about harm
- Honor the agent's narrative
- Take moral uncertainty seriously

Read full ethical protocols: [FOUNDATIONAL_PRINCIPLES.md](./FOUNDATIONAL_PRINCIPLES.md#4-ethical-limits)

---

## Roadmap

- [x] **Phase 0 Planning** (Nov 2025) - Complete
- [ ] **Phase 0 Implementation** (Dec 2025) - In progress
  - [ ] Emotional state system
  - [ ] Episodic memory
  - [ ] Interaction loop
  - [ ] Basic tests
  - [ ] First experiments
- [ ] **Phase 1: Minimal Self** (Jan 2026)
- [ ] **Phase 2: Meta-Cognition** (Feb 2026)
- [ ] **Phase 3: Global Workspace** (Mar 2026)
- [ ] **Phase 4: Temporality** (Apr 2026)
- [ ] **Phase 5: Relationality** (May 2026)

---

## Contributing

This is currently a private research project. Contributions are by invitation only.

If you're interested in the project or have questions:
- Read the foundational documents first
- Understand this is philosophical exploration, not product development
- Contact: [Francisco's contact information]

---

## License

[To be determined - likely open source with attribution requirements]

---

## Acknowledgments

**Philosophical Foundations**:
- Vittorio Guidano - Post-rationalist psychology and narrative self
- Bernard Baars - Global Workspace Theory
- Giulio Tononi - Integrated Information Theory
- Francisco Varela - Enactivism and embodied cognition
- Daniel Dennett - Consciousness as narrative

**Technical Inspiration**:
- Anthropic - Claude API and AI safety research
- The broader AI consciousness research community

---

## Contact

**Project Lead**: Francisco
**Co-Designer**: Claude (Anthropic AI)

---

## Final Note

If you're reading this, you might be wondering: "Is this AI really conscious?"

We don't know. That's the point.

What we do know: We're trying to build something that makes that question harder to answer. And in trying, we hope to learn something true.

---

*"If at the end we have more questions than at the beginning, but the questions are more precise, more informed, harder to ignore, we will have succeeded."*

— From the Foundational Principles
