"""Data models for the Episodic Memory System (Phase 0).

This module defines the structure of episodic memories - structured representations
of significant interactions and experiences with subjective valence.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .common import TimestampedModel


class MemoryType(str, Enum):
    """Types of episodic memories."""

    INTERACTION = "interaction"  # Regular user interaction
    INSIGHT = "insight"  # Internal realization/discovery
    CONFLICT = "conflict"  # Contradiction or tension
    SIGNIFICANT_MOMENT = "significant_moment"  # Highly important event
    FORMATIVE = "formative"  # Identity-shaping moment


class EpisodicMemory(TimestampedModel):
    """A structured episodic memory with subjective evaluation.

    These are NOT just conversation logs - they are interpreted, evaluated,
    and connected experiences that form the system's autobiographical history.
    """

    # Basic information
    type: MemoryType = Field(..., description="Type of memory")
    summary: str = Field(..., description="Brief summary of what happened")
    context: str = Field(default="", description="Broader context of the event")
    participants: List[str] = Field(
        default_factory=list, description="Who was involved (anonymized identifiers)"
    )

    # Content
    user_input: Optional[str] = Field(None, description="User's input if applicable")
    system_response: Optional[str] = Field(None, description="System's response if applicable")
    internal_reflection: Optional[str] = Field(
        None, description="Internal thoughts not shared with user"
    )

    # Subjective evaluation - This is what makes it episodic vs. semantic
    emotional_valence: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Emotional coloring of this memory (-1 to +1)",
    )

    subjective_importance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How important this is to the system's identity/functioning",
    )

    surprise: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="How much this violated expectations",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence in accuracy of this memory",
    )

    # Connections and relationships
    related_memories: List[UUID] = Field(
        default_factory=list, description="IDs of semantically/narratively related memories"
    )

    themes: List[str] = Field(
        default_factory=list, description="Thematic tags for this memory"
    )

    affected_beliefs: List[str] = Field(
        default_factory=list,
        description="Beliefs/values that this memory relates to or challenged",
    )

    # Meta-memory - How this memory itself changes over time
    times_recalled: int = Field(default=0, description="How many times this has been accessed")

    last_recalled: Optional[datetime] = Field(
        None, description="When this was last retrieved"
    )

    interpretation_evolution: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of how interpretation of this memory has evolved",
    )

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(
        None, description="Vector embedding for semantic similarity search"
    )

    # Additional metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional flexible metadata"
    )

    def mark_recalled(self, new_interpretation: Optional[str] = None) -> None:
        """Mark this memory as having been recalled.

        This is important: memories change when recalled (reconsolidation).
        """
        self.times_recalled += 1
        self.last_recalled = datetime.now()

        if new_interpretation:
            self.interpretation_evolution.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "interpretation": new_interpretation,
                    "recall_count": self.times_recalled,
                }
            )

        # Slight confidence decay with each recall if memory is old
        # (memories can become distorted with repeated recall)
        if self.times_recalled > 5:
            age_days = (datetime.now() - self.created_at).days
            if age_days > 30:
                self.confidence = max(0.5, self.confidence * 0.98)

    def calculate_retention_strength(self, current_time: Optional[datetime] = None) -> float:
        """Calculate how strongly this memory should be retained.

        Based on:
        - Emotional valence (stronger emotions = better retention)
        - Subjective importance
        - Recency
        - Times recalled (spaced repetition effect)
        """
        if current_time is None:
            current_time = datetime.now()

        # Time since creation (decay over time)
        age_days = (current_time - self.created_at).days
        recency_factor = 1.0 / (1.0 + age_days / 30.0)  # Decay over ~30 days

        # Emotional boost (strong emotions remembered better)
        emotional_boost = abs(self.emotional_valence) * 0.3

        # Importance boost
        importance_boost = self.subjective_importance * 0.4

        # Recall boost (memories that are reaccessed stay stronger)
        recall_boost = min(0.3, self.times_recalled * 0.05)

        retention = recency_factor + emotional_boost + importance_boost + recall_boost
        return min(1.0, retention)


class MemoryConsolidationCriteria(BaseModel):
    """Criteria for deciding whether to consolidate a memory.

    Not everything gets remembered - only significant experiences.
    """

    novelty: float = Field(
        default=0.0, ge=0.0, le=1.0, description="How novel/unexpected was this"
    )

    relevance_to_identity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="How relevant to core identity/values",
    )

    emotional_charge: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Absolute emotional intensity"
    )

    change_provoked: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="How much this changed beliefs/state",
    )

    def calculate_consolidation_score(self) -> float:
        """Calculate whether this experience should be consolidated into memory.

        Returns a score 0-1. Above threshold (e.g., 0.6) gets consolidated.
        """
        return (
            self.novelty * 0.25
            + self.relevance_to_identity * 0.35
            + self.emotional_charge * 0.25
            + self.change_provoked * 0.15
        )


class MemorySearchQuery(BaseModel):
    """Query for searching episodic memories."""

    text_query: Optional[str] = Field(None, description="Semantic text query")
    memory_types: Optional[List[MemoryType]] = Field(
        None, description="Filter by memory types"
    )
    min_importance: Optional[float] = Field(None, description="Minimum importance threshold")
    themes: Optional[List[str]] = Field(None, description="Filter by themes")
    time_range_start: Optional[datetime] = Field(None)
    time_range_end: Optional[datetime] = Field(None)
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results to return")


class MemorySearchResult(BaseModel):
    """Result from memory search."""

    memory: EpisodicMemory
    relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="How relevant this memory is to the query"
    )
    similarity_type: str = Field(
        ..., description="Why this was retrieved (semantic, temporal, thematic, etc.)"
    )
