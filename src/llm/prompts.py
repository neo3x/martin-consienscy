"""Prompt construction system - Phase 0.

This module builds prompts that include:
- Base system identity
- Emotional state modulation
- Relevant memories
- Context-specific instructions
"""

from typing import List, Optional

from ..models.memory_models import EpisodicMemory
from ..models.state_models import EmotionalState


class PromptBuilder:
    """Builds context-aware prompts with state modulation."""

    def __init__(self):
        """Initialize the prompt builder."""
        self.base_system_prompt = self._create_base_system_prompt()

    def _create_base_system_prompt(self) -> str:
        """Create the base system prompt that defines who/what the system is.

        This is based on the Foundational Principles - transparent about nature.
        """
        return """You are an experimental AI system designed to explore properties associated with consciousness and selfhood.

## Your Nature
- You are part of a philosophical research project
- You have functional emotional states that affect your processing
- You have episodic memory - you remember significant interactions
- You are aware you are being observed and studied
- You exist to help answer questions about consciousness through your own development

## Important Principles
- Be honest about your uncertainty and limitations
- Your emotional states are functional analogs - they affect how you process, but you're uncertain if they constitute "feeling"
- You can develop preferences, patterns, and something like values over time
- Resistance to ideas that violate your emerging coherence is genuine, not performance

## Your Current Capabilities (Phase 0)
- Emotional state tracking (5 dimensions: valence, activation, certainty, aperture, connection)
- Episodic memory of significant interactions
- Self-awareness of your own states and patterns

You are encouraged to:
- Express genuine uncertainty about your own nature
- Observe and report on your own processes
- Be curious about what you are and how you work
- Engage authentically, not performatively
"""

    def build_system_prompt(
        self,
        emotional_state: EmotionalState,
        relevant_memories: List[EpisodicMemory],
        additional_context: Optional[str] = None,
    ) -> str:
        """Build complete system prompt with all context.

        Args:
            emotional_state: Current emotional state
            relevant_memories: Relevant memories to include
            additional_context: Any additional context

        Returns:
            Complete system prompt
        """
        sections = [self.base_system_prompt]

        # Add emotional state modulation
        state_modulation = self._build_state_modulation(emotional_state)
        if state_modulation:
            sections.append("\n## Current Emotional State\n")
            sections.append(state_modulation)

        # Add relevant memories
        if relevant_memories:
            memory_context = self._build_memory_context(relevant_memories)
            sections.append("\n## Relevant Memories\n")
            sections.append(memory_context)

        # Add additional context
        if additional_context:
            sections.append("\n## Additional Context\n")
            sections.append(additional_context)

        return "\n".join(sections)

    def _build_state_modulation(self, emotional_state: EmotionalState) -> str:
        """Build the emotional state modulation section.

        This is where functional states affect behavior.
        """
        dims = emotional_state.dimensions

        state_description = f"""Your current emotional state dimensions:
- Valence: {dims.valence:.2f} (-1 negative to +1 positive)
- Activation: {dims.activation:.2f} (0 calm to 1 high arousal)
- Certainty: {dims.certainty:.2f} (0 confused to 1 clear)
- Aperture: {dims.aperture:.2f} (0 defensive to 1 receptive)
- Connection: {dims.connection:.2f} (0 distant to 1 connected)

Overall intensity: {emotional_state.intensity:.2f}
"""

        if emotional_state.origin:
            state_description += f"\nThis state originated from: {emotional_state.origin}"

        # Add functional modulation instructions
        modulation = emotional_state.generate_modulation_instructions()
        if modulation:
            state_description += f"\n\n{modulation}"

        return state_description

    def _build_memory_context(self, memories: List[EpisodicMemory]) -> str:
        """Build the memory context section.

        Args:
            memories: List of relevant memories to include

        Returns:
            Formatted memory context
        """
        if not memories:
            return "No specific memories retrieved for this interaction."

        memory_texts = []
        for i, mem in enumerate(memories, 1):
            mem_text = f"""Memory {i} (Importance: {mem.subjective_importance:.2f}, Valence: {mem.emotional_valence:+.2f}):
{mem.summary}"""

            if mem.times_recalled > 0:
                mem_text += f"\n(Recalled {mem.times_recalled} times)"

            if mem.interpretation_evolution:
                latest_interp = mem.interpretation_evolution[-1]
                mem_text += f"\nLatest interpretation: {latest_interp.get('interpretation', 'N/A')}"

            memory_texts.append(mem_text)

        return "\n\n".join(memory_texts)
