"""Session manager for handling interaction loop instances."""

import threading
import time
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

import numpy as np
import structlog

from backend.models.api_models import TimelineEvent
from src.core.loop import InteractionLoop

logger = structlog.get_logger()

# Lock for thread-safe singleton initialization
_session_manager_lock = threading.Lock()


class SessionManager:
    """Manages interaction loop instances and system state.

    For Phase 0, we use a single global session.
    Future phases will support multiple concurrent sessions.
    """

    def __init__(self):
        """Initialize the session manager."""
        self._loop: Optional[InteractionLoop] = None
        self._timeline: List[TimelineEvent] = []
        self._start_time: float = time.time()
        self._interaction_count: int = 0
        logger.info("session_manager_initialized")

    def get_loop(self) -> InteractionLoop:
        """Get or create the interaction loop instance.

        Returns:
            InteractionLoop: The active interaction loop
        """
        if self._loop is None:
            logger.info("creating_new_interaction_loop")
            self._loop = InteractionLoop()
            self._add_timeline_event("system_start", "System initialized", {})
        return self._loop

    def process_interaction(self, user_message: str) -> tuple[str, List[str], bool, Optional[UUID]]:
        """Process a user interaction.

        Args:
            user_message: The user's message

        Returns:
            Tuple of (response, triggers_detected, memory_consolidated, memory_id)
        """
        loop = self.get_loop()

        # Add to timeline
        self._add_timeline_event(
            "interaction_start",
            f"User message: {user_message[:50]}...",
            {"message": user_message}
        )

        # Track triggers before processing
        state_before = loop.state_manager.get_current_state()

        # Process interaction
        response = loop.process_interaction(user_message)

        # Track triggers after processing
        # For now we'll extract this from state changes
        # TODO: Modify InteractionLoop to return trigger info
        triggers_detected = []  # Will be populated by modified core

        # Check if memory was consolidated
        # TODO: Modify InteractionLoop to return consolidation info
        memory_consolidated = False
        memory_id = None

        self._interaction_count += 1

        # Add to timeline
        self._add_timeline_event(
            "interaction_complete",
            f"Response generated",
            {
                "response_preview": response[:50] + "...",
                "triggers": triggers_detected,
                "memory_consolidated": memory_consolidated
            }
        )

        return response, triggers_detected, memory_consolidated, memory_id

    def get_current_state(self) -> dict:
        """Get current emotional state.

        Returns:
            Dict with current state information
        """
        loop = self.get_loop()
        state = loop.state_manager.get_current_state()

        return {
            "dimensions": {
                "valence": state.dimensions.valence,
                "activation": state.dimensions.activation,
                "certainty": state.dimensions.certainty,
                "aperture": state.dimensions.aperture,
                "connection": state.dimensions.connection,
            },
            "intensity": state.intensity,
            "duration": state.duration,
            "timestamp": datetime.now(),
        }

    def get_memories(self, limit: int = 50, offset: int = 0) -> tuple[List[dict], int, int]:
        """Get episodic memories.

        Args:
            limit: Maximum number of memories to return
            offset: Offset for pagination

        Returns:
            Tuple of (memories, total_count, formative_count)
        """
        loop = self.get_loop()
        all_memories = list(loop.memory_manager.memories.values())

        # Calculate formative memories (high retention strength)
        formative_count = sum(1 for m in all_memories if m.calculate_retention_strength() > 0.8)

        # Paginate
        memories_slice = all_memories[offset:offset + limit]

        # Convert to dict
        memories_dict = [
            {
                "id": m.id,
                "type": m.type.value,
                "summary": m.summary,
                "emotional_valence": m.emotional_valence,
                "subjective_importance": m.subjective_importance,
                "surprise": m.surprise,
                "created_at": m.created_at,
                "last_recalled": m.last_recalled,
                "times_recalled": m.times_recalled,
                "retention_strength": m.calculate_retention_strength(),
                "interpretation_evolution": m.interpretation_evolution,
            }
            for m in memories_slice
        ]

        return memories_dict, len(all_memories), formative_count

    def get_memory_by_id(self, memory_id: UUID) -> Optional[dict]:
        """Get a specific memory by ID.

        Args:
            memory_id: UUID of the memory

        Returns:
            Memory dict or None if not found
        """
        loop = self.get_loop()

        # Direct lookup by UUID key
        memory = loop.memory_manager.memories.get(memory_id)
        if memory is None:
            return None

        return {
            "id": memory.id,
            "type": memory.type.value,
            "summary": memory.summary,
            "emotional_valence": memory.emotional_valence,
            "subjective_importance": memory.subjective_importance,
            "surprise": memory.surprise,
            "created_at": memory.created_at,
            "last_recalled": memory.last_recalled,
            "times_recalled": memory.times_recalled,
            "retention_strength": memory.calculate_retention_strength(),
            "interpretation_evolution": memory.interpretation_evolution,
        }

    def get_memory_network(self, similarity_threshold: float = 0.7) -> tuple[List[dict], List[dict]]:
        """Get memory network for visualization.

        Args:
            similarity_threshold: Minimum cosine similarity for edges

        Returns:
            Tuple of (nodes, edges)
        """
        loop = self.get_loop()
        memories_list = list(loop.memory_manager.memories.values())

        # Create nodes
        nodes = [
            {
                "id": str(m.id),
                "summary": m.summary,
                "importance": m.subjective_importance,
                "valence": m.emotional_valence,
                "times_recalled": m.times_recalled,
                "created_at": m.created_at,
            }
            for m in memories_list
        ]

        # Create edges based on semantic similarity
        edges = []
        for i, mem1 in enumerate(memories_list):
            for mem2 in memories_list[i + 1:]:
                if mem1.embedding and mem2.embedding:
                    # Calculate cosine similarity
                    similarity = self._cosine_similarity(mem1.embedding, mem2.embedding)
                    if similarity >= similarity_threshold:
                        edges.append({
                            "source": str(mem1.id),
                            "target": str(mem2.id),
                            "similarity": similarity,
                        })

        return nodes, edges

    def get_system_status(self) -> dict:
        """Get overall system status.

        Returns:
            Dict with system status information
        """
        loop = self.get_loop()
        status = loop.get_system_status()

        # Add uptime
        uptime_seconds = int(time.time() - self._start_time)

        # Get memory stats
        all_memories = list(loop.memory_manager.memories.values())
        formative_count = sum(1 for m in all_memories if m.calculate_retention_strength() > 0.8)

        # Calculate average consolidation score if we have memories
        # Note: We don't currently store consolidation scores, so this is a placeholder
        avg_consolidation = 0.0
        last_consolidation = None
        if all_memories:
            last_consolidation = all_memories[-1].created_at

        return {
            "phase": "0",
            "uptime_seconds": uptime_seconds,
            "total_interactions": self._interaction_count,
            "emotional_state": self.get_current_state(),
            "memory_stats": {
                "total_memories": len(all_memories),
                "formative_memories": formative_count,
                "average_consolidation_score": avg_consolidation,
                "last_consolidation": last_consolidation,
            }
        }

    def get_timeline(self, minutes: int = 60) -> List[TimelineEvent]:
        """Get timeline of recent events.

        Args:
            minutes: How many minutes back to retrieve

        Returns:
            List of timeline events
        """
        cutoff = datetime.now().timestamp() - (minutes * 60)
        return [
            event for event in self._timeline
            if event.timestamp.timestamp() >= cutoff
        ]

    def reset_state(self):
        """Reset the emotional state."""
        loop = self.get_loop()
        loop.state_manager.reset()

        self._add_timeline_event(
            "system_reset",
            "Emotional state reset",
            {}
        )

        logger.info("emotional_state_reset")

    def _add_timeline_event(self, event_type: str, description: str, data: dict):
        """Add an event to the timeline.

        Args:
            event_type: Type of event
            description: Human-readable description
            data: Additional event data
        """
        event = TimelineEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            description=description,
            data=data,
        )
        self._timeline.append(event)

        # Keep only last 1000 events to prevent memory issues
        if len(self._timeline) > 1000:
            self._timeline = self._timeline[-1000:]

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity (0 to 1)
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        dot_product = np.dot(v1, v2)
        norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)

        if norm_product == 0:
            return 0.0

        return float(dot_product / norm_product)


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get the global session manager instance (thread-safe).

    Returns:
        SessionManager: The global session manager
    """
    global _session_manager
    if _session_manager is None:
        with _session_manager_lock:
            # Double-check locking pattern
            if _session_manager is None:
                _session_manager = SessionManager()
    return _session_manager
