"""Interaction Loop - Phase 0.

This module implements the core interaction loop that ties together:
- Emotional state management
- Episodic memory
- LLM generation
- Post-processing and consolidation

This is the heart of the system's functioning.
"""

import time
from typing import Optional

import structlog

from ..llm.client import LLMClient
from ..models.memory_models import MemorySearchQuery, MemoryType
from .memory import EpisodicMemoryManager
from .state import EmotionalStateManager

logger = structlog.get_logger()


class InteractionLoop:
    """Core interaction loop for the artificial consciousness system."""

    def __init__(
        self,
        state_manager: Optional[EmotionalStateManager] = None,
        memory_manager: Optional[EpisodicMemoryManager] = None,
        llm_client: Optional[LLMClient] = None,
    ):
        """Initialize the interaction loop.

        Args:
            state_manager: Emotional state manager (creates new if None)
            memory_manager: Memory manager (creates new if None)
            llm_client: LLM client (creates new if None)
        """
        self.state_manager = state_manager or EmotionalStateManager()
        self.memory_manager = memory_manager or EpisodicMemoryManager()
        self.llm_client = llm_client or LLMClient()

        logger.info("interaction_loop_initialized")

    def process_interaction(self, user_input: str) -> str:
        """Process a single interaction through the complete loop.

        This implements the core flow from Technical Architecture:
        1. Load current state
        2. Detect and apply emotional triggers
        3. Search relevant memories
        4. Build context
        5. Generate response
        6. Post-processing (update state, consolidate memory)

        Args:
            user_input: The user's input

        Returns:
            The system's response
        """
        start_time = time.time()

        logger.info("processing_interaction", input_length=len(user_input))

        # 1. LOAD CURRENT STATE
        emotional_state = self.state_manager.get_current_state()
        logger.debug(
            "current_emotional_state",
            dimensions=emotional_state.dimensions.to_dict(),
            intensity=emotional_state.intensity,
        )

        # 2. DETECT AND APPLY EMOTIONAL TRIGGERS
        detected_triggers = self.state_manager.detect_triggers(user_input)
        if detected_triggers:
            logger.info("triggers_detected", triggers=detected_triggers)
            for trigger_name in detected_triggers:
                self.state_manager.apply_trigger(
                    trigger_name, intensity=1.0, origin=f"User input: {user_input[:50]}..."
                )

        # 3. SEARCH RELEVANT MEMORIES
        relevant_memories = []
        if user_input.strip():  # Only search if there's actual input
            search_query = MemorySearchQuery(text_query=user_input, top_k=5)
            search_results = self.memory_manager.search(search_query)
            relevant_memories = [result.memory for result in search_results]

            if relevant_memories:
                logger.info(
                    "memories_retrieved",
                    count=len(relevant_memories),
                    importance_range=(
                        min(m.subjective_importance for m in relevant_memories),
                        max(m.subjective_importance for m in relevant_memories),
                    ),
                )

                # Mark memories as recalled (reconsolidation)
                for memory in relevant_memories:
                    self.memory_manager.recall_and_reconsolidate(memory.id)

        # 4. GENERATE RESPONSE
        try:
            response = self.llm_client.generate_response(
                user_input=user_input,
                emotional_state=emotional_state,
                relevant_memories=relevant_memories,
            )
        except Exception as e:
            logger.error("response_generation_failed", error=str(e))
            response = "I apologize, but I encountered an error while processing your input."

        # 5. POST-PROCESSING

        # 5a. Update emotional state (differential dynamics)
        self.state_manager.update(delta_t=1.0)

        # Take snapshot of state after interaction
        self.state_manager.snapshot(
            context=f"After: {user_input[:30]}...",
            triggered_by=", ".join(detected_triggers) if detected_triggers else None,
        )

        # 5b. Consolidate memory if significant
        memory = self.memory_manager.consolidate(
            user_input=user_input,
            system_response=response,
            emotional_state=emotional_state,
            memory_type=MemoryType.INTERACTION,
        )

        if memory:
            logger.info(
                "new_memory_created",
                memory_id=str(memory.id),
                importance=memory.subjective_importance,
            )

        # 5c. Persist current state
        self.state_manager.persist()

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # ms

        logger.info(
            "interaction_processed",
            processing_time_ms=processing_time,
            response_length=len(response),
            memory_created=memory is not None,
        )

        return response

    def get_system_status(self) -> dict:
        """Get current status of the system.

        Returns:
            Dictionary with system status information
        """
        emotional_state = self.state_manager.get_current_state()

        return {
            "emotional_state": {
                "dimensions": emotional_state.dimensions.to_dict(),
                "intensity": emotional_state.intensity,
                "duration": emotional_state.duration,
            },
            "memory_stats": {
                "total_memories": len(self.memory_manager.memories),
                "formative_memories": len(self.memory_manager.get_formative_memories()),
            },
            "phase": "Phase 0 - Foundation",
        }

    def reset(self) -> None:
        """Reset the system (for testing purposes)."""
        logger.warning("system_reset_requested")

        # This is a dangerous operation - only for development
        self.state_manager = EmotionalStateManager()
        self.memory_manager = EpisodicMemoryManager()

        logger.info("system_reset_complete")
