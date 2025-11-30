"""LLM Client - Phase 0.

This module handles communication with the Claude API, including:
- Prompt construction with state modulation
- Response generation
- Error handling and retries
- Token usage tracking
"""

from typing import List, Optional

import anthropic
import structlog

from ..config import settings
from ..models.memory_models import EpisodicMemory
from ..models.state_models import EmotionalState
from .prompts import PromptBuilder

logger = structlog.get_logger()


class LLMClient:
    """Client for interacting with Claude API."""

    def __init__(self):
        """Initialize the LLM client."""
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.prompt_builder = PromptBuilder()

        logger.info("llm_client_initialized", model=settings.llm_model)

    def generate_response(
        self,
        user_input: str,
        emotional_state: EmotionalState,
        relevant_memories: Optional[List[EpisodicMemory]] = None,
        context: Optional[str] = None,
    ) -> str:
        """Generate a response using Claude API.

        Args:
            user_input: The user's input
            emotional_state: Current emotional state (for modulation)
            relevant_memories: Relevant memories to include in context
            context: Additional context

        Returns:
            The generated response text
        """
        # Build system prompt with state modulation
        system_prompt = self.prompt_builder.build_system_prompt(
            emotional_state=emotional_state,
            relevant_memories=relevant_memories or [],
            additional_context=context,
        )

        logger.info("generating_response", input_length=len(user_input))

        try:
            message = self.client.messages.create(
                model=settings.llm_model,
                max_tokens=settings.llm_max_tokens,
                temperature=settings.llm_temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_input}],
            )

            response_text = message.content[0].text

            # Log usage
            logger.info(
                "response_generated",
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
                response_length=len(response_text),
            )

            return response_text

        except anthropic.APIError as e:
            logger.error("api_error", error=str(e), type=type(e).__name__)
            return f"I encountered an error: {str(e)}"

        except Exception as e:
            logger.error("unexpected_error", error=str(e), type=type(e).__name__)
            return "I encountered an unexpected error while processing your request."

    def generate_with_retry(
        self,
        user_input: str,
        emotional_state: EmotionalState,
        relevant_memories: Optional[List[EpisodicMemory]] = None,
        context: Optional[str] = None,
        max_retries: int = 3,
    ) -> str:
        """Generate response with retry logic.

        Args:
            user_input: The user's input
            emotional_state: Current emotional state
            relevant_memories: Relevant memories
            context: Additional context
            max_retries: Maximum number of retry attempts

        Returns:
            The generated response
        """
        for attempt in range(max_retries):
            try:
                return self.generate_response(
                    user_input=user_input,
                    emotional_state=emotional_state,
                    relevant_memories=relevant_memories,
                    context=context,
                )
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        "retry_attempt",
                        attempt=attempt + 1,
                        max_retries=max_retries,
                        error=str(e),
                    )
                else:
                    logger.error("all_retries_failed", error=str(e))
                    return "I apologize, but I'm having trouble responding right now."

        return "Error: Maximum retries exceeded."
