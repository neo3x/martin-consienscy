"""Common data models used across the project.

This module contains base models and common types that are used throughout
the artificial consciousness architecture.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PhaseType(str, Enum):
    """Development phases of the system."""

    PHASE_0_FOUNDATION = "phase_0_foundation"
    PHASE_1_MINIMAL_SELF = "phase_1_minimal_self"
    PHASE_2_METACOGNITION = "phase_2_metacognition"
    PHASE_3_WORKSPACE = "phase_3_workspace"
    PHASE_4_TEMPORALITY = "phase_4_temporality"
    PHASE_5_RELATIONALITY = "phase_5_relationality"


class TimestampedModel(BaseModel):
    """Base model with automatic timestamping."""

    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to now."""
        self.updated_at = datetime.now()


class Trigger(BaseModel):
    """Represents an event that triggers emotional or cognitive responses."""

    name: str = Field(..., description="Name/type of the trigger")
    description: str = Field(..., description="Description of what triggered this")
    intensity: float = Field(default=1.0, ge=0.0, le=1.0, description="Intensity of the trigger")
    dimensions: Dict[str, float] = Field(
        default_factory=dict, description="Dimensional changes caused by trigger"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class InteractionContext(BaseModel):
    """Context for a single interaction."""

    user_input: str = Field(..., description="User's input text")
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = Field(None, description="Session identifier if applicable")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class SystemResponse(BaseModel):
    """System's response to an interaction."""

    content: str = Field(..., description="Response content")
    emotional_state_snapshot: Optional[Dict[str, Any]] = Field(
        None, description="Emotional state at response time"
    )
    memories_accessed: List[UUID] = Field(
        default_factory=list, description="IDs of memories accessed for this response"
    )
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Evidence(BaseModel):
    """Evidence for updating self-model or detecting patterns."""

    type: str = Field(..., description="Type of evidence (e.g., 'behavioral_pattern', 'contradiction')")
    description: str = Field(..., description="Description of the evidence")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this evidence")
    source: str = Field(..., description="Source of evidence (e.g., memory_id, observation)")
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any] = Field(default_factory=dict, description="Supporting data")
