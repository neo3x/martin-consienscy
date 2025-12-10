"""REST API routes for the backend."""

import time
from datetime import datetime
from typing import Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException, Query

from backend.models.api_models import (
    InteractionRequest,
    InteractionResponse,
    MemoriesListResponse,
    MemoryNetworkResponse,
    MemoryResponse,
    StateResponse,
    SystemStatusResponse,
    TimelineResponse,
    TriggerEvent,
)
from backend.services import get_session_manager

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1")


@router.post("/interactions", response_model=InteractionResponse)
async def create_interaction(request: InteractionRequest):
    """Process a user interaction.

    Args:
        request: The interaction request containing the user message

    Returns:
        InteractionResponse with the system response and state changes
    """
    start_time = time.time()

    try:
        session_manager = get_session_manager()

        logger.info("processing_interaction", message_length=len(request.message))

        # Process the interaction
        response, triggers, memory_consolidated, memory_id = session_manager.process_interaction(
            request.message
        )

        # Get state after interaction
        state_after = session_manager.get_current_state()

        # Convert triggers to TriggerEvent objects
        trigger_events = [
            TriggerEvent(
                name=trigger,
                intensity=1.0,  # TODO: Get actual intensity from core
                timestamp=state_after["timestamp"],
                dimensions_affected=[],  # TODO: Get from trigger definition
            )
            for trigger in triggers
        ]

        processing_time_ms = int((time.time() - start_time) * 1000)

        logger.info(
            "interaction_processed",
            processing_time_ms=processing_time_ms,
            triggers_count=len(triggers),
            memory_consolidated=memory_consolidated,
        )

        return InteractionResponse(
            response=response,
            state_after=StateResponse(**state_after),
            triggers_detected=trigger_events,
            memory_consolidated=memory_consolidated,
            memory_id=memory_id,
            processing_time_ms=processing_time_ms,
        )

    except Exception as e:
        logger.error("interaction_processing_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process interaction: {str(e)}")


@router.get("/state", response_model=StateResponse)
async def get_current_state():
    """Get the current emotional state.

    Returns:
        StateResponse with current emotional dimensions
    """
    try:
        session_manager = get_session_manager()
        state = session_manager.get_current_state()

        return StateResponse(**state)

    except Exception as e:
        logger.error("get_state_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get state: {str(e)}")


@router.post("/state/reset")
async def reset_state():
    """Reset the emotional state to defaults.

    Returns:
        Status message
    """
    try:
        session_manager = get_session_manager()
        session_manager.reset_state()

        return {"status": "reset_complete"}

    except Exception as e:
        logger.error("reset_state_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to reset state: {str(e)}")


@router.get("/memories", response_model=MemoriesListResponse)
async def get_memories(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """Get episodic memories with pagination.

    Args:
        limit: Maximum number of memories to return
        offset: Offset for pagination

    Returns:
        MemoriesListResponse with list of memories
    """
    try:
        session_manager = get_session_manager()
        memories, total, formative_count = session_manager.get_memories(limit, offset)

        memory_responses = [MemoryResponse(**m) for m in memories]

        return MemoriesListResponse(
            memories=memory_responses,
            total=total,
            formative_count=formative_count,
        )

    except Exception as e:
        logger.error("get_memories_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get memories: {str(e)}")


@router.get("/memories/network", response_model=MemoryNetworkResponse)
async def get_memory_network(
    similarity_threshold: float = Query(0.7, ge=0.0, le=1.0),
):
    """Get memory network for visualization.

    Args:
        similarity_threshold: Minimum cosine similarity for edges

    Returns:
        MemoryNetworkResponse with nodes and edges
    """
    try:
        session_manager = get_session_manager()
        nodes, edges = session_manager.get_memory_network(similarity_threshold)

        return MemoryNetworkResponse(
            nodes=nodes,
            edges=edges,
        )

    except Exception as e:
        logger.error("get_memory_network_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get memory network: {str(e)}")


@router.get("/memories/{memory_id}", response_model=MemoryResponse)
async def get_memory(memory_id: UUID):
    """Get a specific memory by ID.

    Args:
        memory_id: UUID of the memory

    Returns:
        MemoryResponse with the memory details
    """
    try:
        session_manager = get_session_manager()
        memory = session_manager.get_memory_by_id(memory_id)

        if memory is None:
            raise HTTPException(status_code=404, detail="Memory not found")

        return MemoryResponse(**memory)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_memory_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get memory: {str(e)}")


@router.get("/system/status", response_model=SystemStatusResponse)
async def get_system_status():
    """Get overall system status.

    Returns:
        SystemStatusResponse with system information
    """
    try:
        session_manager = get_session_manager()
        status = session_manager.get_system_status()

        return SystemStatusResponse(**status)

    except Exception as e:
        logger.error("get_system_status_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")


@router.get("/system/timeline", response_model=TimelineResponse)
async def get_timeline(
    minutes: int = Query(60, ge=1, le=1440),  # Max 24 hours
):
    """Get timeline of recent events.

    Args:
        minutes: How many minutes back to retrieve

    Returns:
        TimelineResponse with recent events
    """
    try:
        session_manager = get_session_manager()
        events = session_manager.get_timeline(minutes)

        if events:
            start_time = events[0].timestamp
            end_time = events[-1].timestamp
        else:
            now = datetime.now()
            start_time = now
            end_time = now

        return TimelineResponse(
            events=events,
            start_time=start_time,
            end_time=end_time,
            total_events=len(events),
        )

    except Exception as e:
        logger.error("get_timeline_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get timeline: {str(e)}")
