"""Pydantic models for API request/response schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class InteractionRequest(BaseModel):
    """Request schema for creating an interaction."""

    message: str = Field(..., min_length=1, max_length=10000)


class EmotionalDimensionsAPI(BaseModel):
    """Emotional dimensions for API responses."""

    valence: float = Field(ge=-1.0, le=1.0)
    activation: float = Field(ge=0.0, le=1.0)
    certainty: float = Field(ge=0.0, le=1.0)
    aperture: float = Field(ge=0.0, le=1.0)
    connection: float = Field(ge=0.0, le=1.0)


class StateResponse(BaseModel):
    """Response schema for emotional state."""

    dimensions: EmotionalDimensionsAPI
    intensity: float = Field(ge=0.0, le=1.0)
    duration: int = Field(ge=0)
    timestamp: datetime


class TriggerEvent(BaseModel):
    """Trigger event data."""

    name: str
    intensity: float = Field(ge=0.0, le=1.0)
    timestamp: datetime
    dimensions_affected: List[str]


class InteractionResponse(BaseModel):
    """Response schema for interaction processing."""

    response: str
    state_after: StateResponse
    triggers_detected: List[TriggerEvent]
    memory_consolidated: bool
    memory_id: Optional[UUID] = None
    processing_time_ms: int


class MemoryResponse(BaseModel):
    """Response schema for a single memory."""

    id: UUID
    type: str
    summary: str
    emotional_valence: float = Field(ge=-1.0, le=1.0)
    subjective_importance: float = Field(ge=0.0, le=1.0)
    surprise: float = Field(ge=0.0, le=1.0)
    created_at: datetime
    last_recalled: Optional[datetime] = None
    times_recalled: int
    retention_strength: float = Field(ge=0.0, le=1.0)
    interpretation_evolution: List[Dict[str, Any]]


class MemoriesListResponse(BaseModel):
    """Response schema for list of memories."""

    memories: List[MemoryResponse]
    total: int
    formative_count: int


class MemoryNode(BaseModel):
    """Node in memory network graph."""

    id: str  # UUID as string for JSON serialization
    summary: str
    importance: float
    valence: float
    times_recalled: int
    created_at: datetime


class MemoryEdge(BaseModel):
    """Edge in memory network graph."""

    source: str  # UUID as string
    target: str  # UUID as string
    similarity: float = Field(ge=0.0, le=1.0)


class MemoryNetworkResponse(BaseModel):
    """Response schema for memory network visualization."""

    nodes: List[MemoryNode]
    edges: List[MemoryEdge]


class MemoryStatsAPI(BaseModel):
    """Memory statistics."""

    total_memories: int
    formative_memories: int
    average_consolidation_score: float
    last_consolidation: Optional[datetime] = None


class SystemStatusResponse(BaseModel):
    """Response schema for system status."""

    phase: str
    uptime_seconds: int
    total_interactions: int
    emotional_state: StateResponse
    memory_stats: MemoryStatsAPI


class TimelineEvent(BaseModel):
    """Event in the system timeline."""

    timestamp: datetime
    event_type: str  # 'interaction', 'trigger', 'memory', 'reset', 'state_change'
    description: str
    data: Dict[str, Any]


class TimelineResponse(BaseModel):
    """Response schema for timeline."""

    events: List[TimelineEvent]
    start_time: datetime
    end_time: datetime
    total_events: int


class WebSocketMessage(BaseModel):
    """WebSocket message schema."""

    type: str  # 'message', 'subscribe', 'unsubscribe'
    data: Dict[str, Any]


class WebSocketEvent(BaseModel):
    """WebSocket event sent from server to client."""

    type: str  # 'state_update', 'trigger_detected', 'memory_consolidated', 'response', 'processing'
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
