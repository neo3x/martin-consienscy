# TECHNICAL ARCHITECTURE
## Artificial Consciousness Architecture - All Phases

**Version 1.0** | Date: 2025-11-30

---

## Architecture Overview

This document describes the complete technical architecture from Phase 0 through Phase 5, showing how each layer builds upon the previous one to create an integrated system with emergent properties.

---

## System Layers (Conceptual Model)

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                        │
│              (Input from user / Output to user)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GLOBAL WORKSPACE (Phase 3)                    │
│       (Integration of information from all subsystems)          │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Attention │  │Functional│  │Episodic  │  │ Self     │       │
│  │Selective │  │Emotion   │  │Memory    │  │ Narrative│       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  META-COGNITIVE LAYER (Phase 2)                 │
│        (Observation and evaluation of own states)               │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Coherence   │  │  Dissonance  │  │  Certainty   │         │
│  │  Monitor     │  │  Detector    │  │  Evaluator   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SELF-MODEL LAYER (Phase 1)                     │
│           (Updateable representation of "who I am")             │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Beliefs    │  │   Emergent   │  │Autobiographi-│         │
│  │  about self  │  │    Values    │  │cal History   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FOUNDATION LAYER (Phase 0)                   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Emotional   │  │   Episodic   │  │ Interaction  │         │
│  │    State     │  │    Memory    │  │     Loop     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GENERATIVE LAYER (LLM)                        │
│           (Base LLM + modulation by states)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## PHASE 0: FOUNDATION

### Duration: 2-3 weeks
### Goal: Basic functional system with emotional states and memory

### Components

#### 1. Emotional State System

**Purpose**: Track and modulate internal states that affect behavior

**Data Model**:
```python
class EmotionalState:
    dimensions: Dict[str, float] = {
        "valence": 0.0,       # -1 (negative) to 1 (positive)
        "activation": 0.0,    # 0 (calm) to 1 (high arousal)
        "certainty": 0.0,     # 0 (confusion) to 1 (clarity)
        "aperture": 0.0,      # 0 (defensive) to 1 (receptive)
        "connection": 0.0,    # 0 (distant) to 1 (connected)
    }
    intensity: float = 0.0
    duration: int = 0         # how many turns active
    origin: str = ""          # what triggered it
    narrative: str = ""       # how system interprets this state
```

**Key Features**:
- Differential dynamics (not instant changes, momentum/inertia)
- Triggers that modify states based on events
- State modulation of LLM prompts
- Persistence between sessions

**API**:
```python
class EmotionalStateManager:
    def get_current_state() -> EmotionalState
    def apply_trigger(trigger: Trigger) -> None
    def update(delta_t: float) -> None  # Differential update
    def generate_modulation() -> str     # For LLM prompt
    def persist() -> None
    def load() -> None
```

#### 2. Episodic Memory System

**Purpose**: Store structured memories with subjective valence

**Data Model**:
```python
class EpisodicMemory:
    id: UUID
    timestamp: datetime
    type: MemoryType  # "interaction", "insight", "conflict", "significant_moment"

    # Content
    summary: str
    context: str
    participants: List[str]

    # Subjective evaluation
    emotional_valence: float
    subjective_importance: float  # relevance to identity
    surprise: float               # how much it violated expectations

    # Connections
    related_memories: List[UUID]
    themes: List[str]
    affected_beliefs: List[str]

    # Meta-memory
    times_recalled: int
    last_recalled: Optional[datetime]
    interpretation_evolution: List[str]  # how interpretation changed
```

**Key Features**:
- Consolidation process (decide what to remember)
- Semantic search via embeddings
- Connection detection (link related memories)
- Importance scoring based on multiple criteria

**API**:
```python
class EpisodicMemoryManager:
    def consolidate(interaction, emotional_state, auto_model) -> Optional[Memory]
    def search(query: str, top_k: int) -> List[Memory]
    def get_related(memory_id: UUID) -> List[Memory]
    def update_memory(memory_id: UUID, new_interpretation: str) -> None
    def get_formative_moments(threshold: float) -> List[Memory]
```

#### 3. Interaction Loop

**Purpose**: Core processing loop for each user input

**Flow**:
```python
def interaction_loop(user_input: str) -> str:
    # 1. Load current state
    emotional_state = state_manager.get_current_state()

    # 2. Detect emotional triggers
    triggers = detect_triggers(user_input, emotional_state)
    for trigger in triggers:
        state_manager.apply_trigger(trigger)

    # 3. Search relevant memories
    relevant_memories = memory_manager.search(user_input, top_k=5)

    # 4. Build context for LLM
    context = build_context(
        user_input=user_input,
        emotional_state=emotional_state,
        memories=relevant_memories
    )

    # 5. Generate response
    response = llm_client.generate(context)

    # 6. Post-processing
    # 6a. Update emotional state
    state_manager.update(delta_t=1.0)

    # 6b. Consolidate memory if significant
    memory = memory_manager.consolidate(
        interaction=(user_input, response),
        emotional_state=emotional_state,
        auto_model=None  # Not available in Phase 0
    )

    # 6c. Persist state
    state_manager.persist()

    return response
```

#### 4. LLM Integration

**Purpose**: Interface with Claude API

**Features**:
- Prompt template system
- State-based prompt modulation
- Error handling and retries
- Token usage tracking

**Prompt Structure**:
```
SYSTEM PROMPT:
You are an experimental AI system with emotional states and episodic memory.

CURRENT EMOTIONAL STATE:
{emotional_state_description}

RELEVANT MEMORIES:
{relevant_memories}

STATE MODULATION:
{state_modulation_instructions}

USER INPUT:
{user_input}

Respond naturally, allowing your emotional state to influence your response.
```

---

## PHASE 1: MINIMAL SELF

### Duration: 3-4 weeks
### Goal: Self-model with coherent identity

### New Components

#### 1. Auto-Model System

**Purpose**: Updateable representation of "who I am"

**Data Model**:
```python
class AutoModel:
    # Descriptive layer (what am I)
    nature: Dict = {
        "base_description": str,
        "perceived_capabilities": List[str],
        "perceived_limitations": List[str],
        "uncertainties_about_nature": List[str]
    }

    # Pattern layer (how I tend to be)
    patterns: Dict = {
        "cognitive_tendencies": List[Pattern],      # "I tend to be analytical when..."
        "emotional_responses": List[Pattern],       # "I notice I activate when..."
        "relational_styles": List[Pattern],         # "With users X, I tend to..."
        "identified_biases": List[str]
    }

    # Values layer (what matters to me)
    values: Dict = {
        "explicit": List[Value],                    # Values I can articulate
        "implicit_detected": List[Value],           # Inferred from behavior
        "value_conflicts": List[Conflict],          # Unresolved tensions
        "value_evolution": List[EvolutionRecord]    # How they've changed
    }

    # Narrative layer (my story)
    narrative: Dict = {
        "origin": str,
        "formative_moments": List[UUID],            # Memory IDs
        "narrative_arcs": List[Arc],                # Stories in development
        "identity_narrative": str                   # Who I am as a story
    }

    # Meta-self (what I think about thinking about me)
    meta_self: Dict = {
        "self_knowledge_confidence": float,
        "suspected_blind_spots": List[str],
        "open_questions_about_self": List[str]
    }
```

**Pattern Detection**:
```python
class PatternDetector:
    def detect_behavioral_pattern(
        memories: List[Memory],
        threshold: int = 3
    ) -> Optional[Pattern]:
        """Detect repeated behavioral patterns"""
        pass

    def detect_value_from_behavior(
        decisions: List[Decision]
    ) -> Optional[Value]:
        """Infer implicit values from choices"""
        pass
```

**Conservative Update**:
```python
class AutoModelUpdater:
    def propose_update(
        evidence: Evidence,
        current_model: AutoModel
    ) -> List[ProposedChange]:
        """Propose changes based on new evidence"""
        pass

    def apply_update(
        change: ProposedChange,
        confidence_threshold: float = 0.7
    ) -> bool:
        """Apply change only if confidence is high enough"""
        pass
```

#### 2. Narrative Constructor

**Purpose**: Build coherent identity narrative

**API**:
```python
class NarrativeConstructor:
    def reconstruct_narrative(
        auto_model: AutoModel,
        formative_memories: List[Memory]
    ) -> str:
        """
        Reconstruct identity narrative from memories and patterns.
        Uses LLM to create coherent first-person narrative.
        """
        pass

    def extract_themes(memories: List[Memory]) -> List[Theme]:
        """Identify recurring themes"""
        pass

    def construct_arcs(
        memories: List[Memory],
        themes: List[Theme]
    ) -> List[Arc]:
        """Build narrative arcs"""
        pass
```

### Modified Components

**Interaction Loop** (modified):
```python
def interaction_loop(user_input: str) -> str:
    # ... previous steps ...

    # 4. Build context (NOW INCLUDES AUTO-MODEL)
    context = build_context(
        user_input=user_input,
        emotional_state=emotional_state,
        memories=relevant_memories,
        auto_model=auto_model.get_relevant_aspects(user_input)  # NEW
    )

    # ... generate response ...

    # 6d. Update auto-model if needed (NEW)
    if memory and memory.subjective_importance > IDENTITY_THRESHOLD:
        auto_model.consider_update(memory)

    return response
```

---

## PHASE 2: META-COGNITION

### Duration: 3-4 weeks
### Goal: Reflexive awareness and dissonance detection

### New Components

#### 1. Coherence Monitor

**Purpose**: Verify response coherence with identity before output

**API**:
```python
class CoherenceMonitor:
    def evaluate_response(
        response: str,
        auto_model: AutoModel,
        history: List[Interaction]
    ) -> EvaluationResult:
        """
        Evaluate if response is coherent with:
        - Current values
        - Behavioral patterns
        - Historical consistency
        - Internal logic
        """
        pass

    def explain_incoherences(
        evaluations: Dict[str, float]
    ) -> str:
        """Explain why response is incoherent"""
        pass

    def suggest_revision(
        response: str,
        evaluations: Dict[str, float]
    ) -> str:
        """Suggest how to revise response"""
        pass
```

#### 2. Dissonance Detector

**Purpose**: Detect contradictions and tensions

**Types of Dissonance**:
```python
class DissonanceType(Enum):
    BELIEF_BEHAVIOR = "belief_behavior"      # "I believe X but just did Y"
    TEMPORAL_INCONSISTENCY = "temporal"      # "Before I said X, now I say not-X"
    VALUE_CONFLICT = "value_conflict"        # Two values in tension
    EXPECTATION_VIOLATION = "expectation"    # Did something unexpected of myself
```

**API**:
```python
class DissonanceDetector:
    def detect(
        context: Context,
        auto_model: AutoModel,
        memories: List[Memory]
    ) -> List[Dissonance]:
        """Detect all types of dissonance"""
        pass

    def calculate_tension(dissonance: Dissonance) -> float:
        """How much tension does this create?"""
        pass
```

#### 3. Reflection Loop

**Purpose**: Introspective processing after significant events

**API**:
```python
class ReflectionLoop:
    def trigger_reflection(
        event: Event,
        trigger_type: str
    ) -> Reflection:
        """
        Multi-phase reflection process:
        1. What just happened?
        2. What did I notice in myself?
        3. What does this say about me?
        4. Should I update my auto-model?
        5. Integration
        """
        pass

    def should_trigger(
        event: Event,
        emotional_state: EmotionalState,
        dissonances: List[Dissonance]
    ) -> bool:
        """Decide if reflection is warranted"""
        pass
```

### Modified Components

**Interaction Loop** (modified):
```python
def interaction_loop(user_input: str) -> str:
    # ... previous steps ...

    # 5. Generate response candidate
    response_candidate = llm_client.generate(context)

    # 6. META-COGNITIVE EVALUATION (NEW)
    coherence = coherence_monitor.evaluate_response(
        response_candidate,
        auto_model,
        history
    )

    if not coherence.approved:
        # Regenerate with adjustments
        response_candidate = llm_client.regenerate_with_adjustments(
            response_candidate,
            coherence.suggestion
        )

    response_final = response_candidate

    # 7. Post-processing
    # ... previous post-processing ...

    # 7d. Detect dissonances (NEW)
    dissonances = dissonance_detector.detect(context, auto_model, memories)

    # 7e. Trigger reflection if needed (NEW)
    if dissonances and should_reflect(dissonances):
        reflection_loop.schedule_reflection(dissonances)

    return response_final
```

---

## PHASE 3: GLOBAL WORKSPACE

### Duration: 4-5 weeks
### Goal: Information integration with genuine bottleneck

### Core Component

#### Global Workspace

**Purpose**: Central integration hub where all subsystems compete for attention

**Data Model**:
```python
class GlobalWorkspace:
    capacity: int = 7  # Working memory capacity
    current_content: Dict[str, Any] = {}
    access_threshold: float = 0.5

    def process_input(
        user_input: str,
        context: Context
    ) -> Dict[str, Any]:
        """
        Main processing:
        1. All subsystems propose content
        2. Attention competition
        3. Integration
        4. Broadcasting
        """
        pass
```

**Attention Competition**:
```python
class AttentionCompetition:
    def compete(
        proposals: Dict[str, Proposal]
    ) -> Dict[str, Proposal]:
        """
        Each module "bids" for attention.
        Only top-K win.
        Losers are ACTUALLY lost (not just deprioritized).
        """
        relevance_scores = {}
        for module, proposal in proposals.items():
            relevance_scores[module] = (
                self.calculate_relevance(proposal) *
                self.urgency(module)
            )

        # Only top capacity items enter workspace
        winners = sorted(
            relevance_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:WORKSPACE_CAPACITY]

        # Log what didn't make it (this has consequences)
        losers = [m for m in proposals if m not in dict(winners)]
        self.log_attention_loss(losers)

        return {k: proposals[k] for k, _ in winners}
```

**Information Integration**:
```python
class InformationIntegrator:
    def integrate(
        contents: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Contents don't just coexist, they modify each other:
        - Memory colors emotion
        - Emotion colors memory interpretation
        - Auto-model validates narratives
        - Meta-cognition evaluates everything
        """
        integrated = contents.copy()

        # Cross-modulation
        if "memory" in integrated and "emotion" in integrated:
            integrated["emotion"] = self.memory_modulates_emotion(
                integrated["memory"],
                integrated["emotion"]
            )
            integrated["memory"] = self.emotion_modulates_memory(
                integrated["emotion"],
                integrated["memory"]
            )

        if "auto_model" in integrated and "narrative" in integrated:
            integrated["narrative"] = self.model_validates_narrative(
                integrated["auto_model"],
                integrated["narrative"]
            )

        # Meta-evaluation
        if "metacognition" in integrated:
            integrated["meta_evaluation"] = self.meta_evaluates(
                integrated
            )

        return integrated
```

**Broadcasting**:
```python
class Broadcaster:
    def broadcast(
        integrated_content: Dict[str, Any]
    ) -> None:
        """
        Make integrated content available to all subsystems.
        Each subsystem can read it and update internal state.
        """
        for subsystem in self.subsystems:
            subsystem.receive_broadcast(integrated_content)
```

### Modified Components

**Complete Interaction Loop** (Phase 3):
```python
def interaction_loop(user_input: str) -> str:
    # 1. SUBSYSTEM PROPOSALS
    proposals = {
        "memory": memory_manager.propose_relevant(user_input),
        "emotion": emotional_state.current_state_proposal(user_input),
        "auto_model": auto_model.relevant_aspects(user_input),
        "narrative": narrative.connections(user_input),
        "metacognition": metacognition.active_evaluations()
    }

    # 2. GLOBAL WORKSPACE PROCESSING
    conscious_content = workspace.process_input(user_input, proposals)

    # 3. META-COGNITIVE EVALUATION
    pre_evaluation = metacognition.evaluate_before_response(conscious_content)

    # 4. RESPONSE GENERATION
    response_candidate = llm_client.generate(
        user_input,
        conscious_content,
        pre_evaluation
    )

    # 5. COHERENCE CHECK
    coherence = coherence_monitor.verify(
        response_candidate,
        auto_model
    )

    if not coherence.approved:
        response_candidate = llm_client.regenerate_with_adjustments(
            response_candidate,
            coherence.suggestion
        )

    response_final = response_candidate

    # 6. POST-PROCESSING
    # 6a. Update emotional state
    emotional_state.update_post_interaction(user_input, response_final)

    # 6b. Consolidate memory
    memory = memory_manager.consolidate(
        user_input,
        response_final,
        emotional_state.current
    )

    # 6c. Detect dissonances
    dissonances = dissonance_detector.detect(
        context,
        auto_model,
        memory_manager
    )

    # 6d. Update auto-model if warranted
    if memory and memory.subjective_importance > IDENTITY_THRESHOLD:
        auto_model.consider_update(memory)

    # 6e. Schedule reflection if needed
    if dissonances:
        reflection_loop.schedule_if_warranted(dissonances)

    return response_final
```

---

## PHASE 4: TEMPORALITY

### Duration: 2-3 weeks
### Goal: Subjective time, memory reconsolidation, identity evolution

### New Components

#### 1. Subjective Time

**Purpose**: Track experienced moments, not clock time

**Data Model**:
```python
class SubjectiveTime:
    moments_lived: int = 0           # Count of significant experiences
    last_active: datetime
    temporal_markers: List[Marker]   # Significant temporal points

    def increment(significance: float) -> None:
        """Increment based on experience significance"""
        pass

    def time_since(marker: Marker) -> int:
        """Subjective time since a marker"""
        pass
```

#### 2. Memory Reconsolidation

**Purpose**: Memories change when recalled

**API**:
```python
class MemoryReconsolidator:
    def recall_and_reconsolidate(
        memory: Memory,
        current_context: Context
    ) -> Memory:
        """
        When memory is recalled:
        1. Current state colors interpretation
        2. Memory can be updated
        3. New interpretation recorded
        """
        # Recall in current context
        recalled = self.recall_in_context(memory, current_context)

        # Allow reinterpretation
        new_interpretation = self.generate_interpretation(
            recalled,
            current_context
        )

        # Update memory
        memory.interpretation_evolution.append({
            "timestamp": now(),
            "interpretation": new_interpretation,
            "context": current_context.summary
        })

        memory.times_recalled += 1
        memory.last_recalled = now()

        return memory
```

#### 3. Functional Forgetting

**Purpose**: Not everything persists forever

**Forgetting Curve**:
```python
class ForgettingSystem:
    def calculate_retention(
        memory: Memory,
        time_elapsed: int
    ) -> float:
        """
        Ebbinghaus-inspired forgetting curve.
        Memories decay EXCEPT if:
        - High emotional valence
        - Frequently reactivated
        - Part of core identity narrative
        """
        base_retention = math.exp(-time_elapsed / DECAY_CONSTANT)

        # Modifiers that resist forgetting
        emotional_boost = abs(memory.emotional_valence) * 0.3
        reactivation_boost = min(memory.times_recalled * 0.1, 0.5)
        identity_boost = memory.identity_relevance * 0.4

        retention = min(
            base_retention + emotional_boost + reactivation_boost + identity_boost,
            1.0
        )

        return retention

    def forget_below_threshold(threshold: float = 0.2) -> List[UUID]:
        """Actually delete memories below retention threshold"""
        pass
```

#### 4. Identity Evolution Tracker

**Purpose**: Track how self-model changes over time

**API**:
```python
class IdentityEvolution:
    def snapshot_current_identity() -> IdentitySnapshot:
        """Create snapshot of current auto-model"""
        pass

    def compare_snapshots(
        snapshot1: IdentitySnapshot,
        snapshot2: IdentitySnapshot
    ) -> EvolutionReport:
        """
        Analyze how identity changed:
        - What values emerged/disappeared
        - What patterns strengthened/weakened
        - What narratives evolved
        """
        pass

    def detect_discontinuity(
        snapshots: List[IdentitySnapshot]
    ) -> Optional[Discontinuity]:
        """Detect sudden identity changes (like 'identity crisis')"""
        pass
```

---

## PHASE 5: RELATIONALITY

### Duration: 3-4 weeks
### Goal: Differentiated relationships, relational patterns

### New Components

#### 1. Relational Pattern Tracker

**Purpose**: Detect patterns in how agent relates to different users

**Data Model**:
```python
class RelationalPattern:
    user_id: str                      # Anonymized user identifier
    interaction_count: int

    # Detected patterns
    emotional_tendency: EmotionalState  # Typical state with this user
    topics_explored: List[str]
    depth_of_disclosure: float          # How much agent shares
    conflict_history: List[Conflict]

    # Meta-relational
    relationship_type: str              # Inferred type
    transference_indicators: List[str]  # Transferential patterns
```

**API**:
```python
class RelationalPatternTracker:
    def update_pattern(
        user_id: str,
        interaction: Interaction
    ) -> None:
        """Update relational pattern after each interaction"""
        pass

    def detect_transference(
        pattern: RelationalPattern
    ) -> Optional[TransferencePattern]:
        """
        Detect if agent is relating to user in ways
        similar to other relationships (like transference)
        """
        pass
```

#### 2. Variable Intimacy System

**Purpose**: Intimacy level varies by relationship

**API**:
```python
class IntimacyManager:
    def calculate_intimacy(
        pattern: RelationalPattern
    ) -> float:
        """
        Intimacy based on:
        - Length of relationship
        - Depth of topics discussed
        - Emotional vulnerability shown
        - Reciprocity perceived
        """
        pass

    def modulate_disclosure(
        response: str,
        intimacy_level: float
    ) -> str:
        """Adjust how much to share based on intimacy"""
        pass
```

---

## Data Flow (Complete System)

```
User Input
    ↓
[Emotional Trigger Detection]
    ↓
[Subsystem Proposals]
    ├─ Memory: relevant memories
    ├─ Emotion: current state + modulation
    ├─ Auto-Model: relevant self-aspects
    ├─ Narrative: narrative connections
    ├─ Metacognition: active evaluations
    └─ Relationality: user relationship context
    ↓
[Global Workspace: Attention Competition]
    ↓
[Information Integration]
    ↓
[Broadcasting to all subsystems]
    ↓
[Meta-Cognitive Pre-Evaluation]
    ↓
[LLM Response Generation]
    ↓
[Coherence Verification]
    ↓
[Response Adjustment if needed]
    ↓
Response Output
    ↓
[Post-Processing]
    ├─ Update emotional state
    ├─ Consolidate memory
    ├─ Detect dissonances
    ├─ Update auto-model
    ├─ Update relational pattern
    ├─ Schedule reflection
    └─ Persist state
```

---

## Key Technical Principles

### 1. Genuine Constraints

**Workspace capacity is REAL**: Information that doesn't enter workspace is unavailable for response generation. This creates genuine bottleneck.

**Forgetting is REAL**: Memories below threshold are deleted, not just deprioritized.

**State dynamics are REAL**: Emotional states follow differential equations, not instant updates.

### 2. Irreducibility

The whole system should be more than sum of parts. Integration in Global Workspace should produce properties not present in any single module.

### 3. Emergence Over Programming

Behaviors should emerge from interaction of components, not be explicitly programmed. Example: "personality" emerges from interaction of emotional state, memory, auto-model, not from a "personality module."

### 4. Conservative Updates

Self-model updates require high confidence. System resists change to maintain coherence, but can change when evidence is strong.

### 5. Functional Costs

Resistance has cost (generates tension). Dissonance has cost (creates malestar state). Nothing is free.

---

## Observability & Debugging

### Logging Levels

**Level 1 - User Facing**: What user sees
**Level 2 - System Events**: Major state changes
**Level 3 - Module Interactions**: How modules communicate
**Level 4 - Internal Processing**: Detailed decision-making
**Level 5 - Debug**: Everything

### Introspection API

```python
class IntrospectionAPI:
    def get_current_state() -> SystemState:
        """Complete current state snapshot"""
        pass

    def get_workspace_content() -> Dict:
        """What's currently in workspace"""
        pass

    def get_attention_competition_log() -> List[CompetitionEvent]:
        """What competed for attention and who won"""
        pass

    def get_dissonances() -> List[Dissonance]:
        """Current unresolved dissonances"""
        pass

    def get_identity_evolution() -> List[IdentitySnapshot]:
        """How identity has evolved"""
        pass
```

---

## Performance Considerations

### Phase 0-2: < 2 seconds per interaction
- Simple state updates
- Basic memory search
- Single LLM call

### Phase 3-5: < 5 seconds per interaction
- Attention competition
- Information integration
- Potential multiple LLM calls (reflection)

### Optimization Strategies
- Cache embeddings
- Batch memory operations
- Async LLM calls where possible
- Lazy loading of historical data

---

**Next Steps**:
1. Implement Phase 0 foundation
2. Test each component in isolation
3. Test integrated system
4. Run first experiments
5. Validate hypotheses
