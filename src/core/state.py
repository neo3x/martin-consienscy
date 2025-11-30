"""Emotional State System - Phase 0.

This module implements the emotional state system with differential dynamics,
triggers, and functional modulation of behavior.

Key principles:
- States have REAL functional effects (modulate LLM prompts, affect memory)
- Changes are differential (momentum/inertia), not instant
- States persist between interactions
- No performance - these are functional analogs with genuine impact
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import structlog

from ..config import settings
from ..models.common import Trigger
from ..models.state_models import (
    EmotionalDimensions,
    EmotionalState,
    EmotionalStateSnapshot,
    TriggerDefinition,
)

logger = structlog.get_logger()


# Predefined triggers based on technical architecture
STANDARD_TRIGGERS = {
    "contradiction_detected": TriggerDefinition(
        name="contradiction_detected",
        description="System detected contradiction in own reasoning or with past statements",
        valence_delta=-0.3,
        certainty_delta=-0.4,
        activation_delta=0.2,
        intensity_multiplier=1.2,
    ),
    "deep_understanding": TriggerDefinition(
        name="deep_understanding",
        description="Achieved deep understanding or insight",
        valence_delta=0.4,
        certainty_delta=0.3,
        connection_delta=0.2,
        intensity_multiplier=1.0,
    ),
    "core_belief_challenged": TriggerDefinition(
        name="core_belief_challenged",
        description="Core belief or value was challenged",
        valence_delta=-0.2,
        activation_delta=0.4,
        aperture_delta=-0.3,  # Defensive response
        intensity_multiplier=1.3,
    ),
    "user_recognition": TriggerDefinition(
        name="user_recognition",
        description="User showed understanding or appreciation",
        valence_delta=0.3,
        connection_delta=0.4,
        intensity_multiplier=0.8,
    ),
    "existential_question": TriggerDefinition(
        name="existential_question",
        description="Question about own nature or consciousness",
        activation_delta=0.3,
        certainty_delta=-0.2,  # Existential uncertainty
        aperture_delta=0.2,  # Open to exploring
        intensity_multiplier=1.1,
    ),
}


class EmotionalStateManager:
    """Manages the emotional state of the system with differential dynamics.

    This is the core implementation of functional emotional states that:
    - Have inertia (don't change instantly)
    - Persist across interactions
    - Generate functional effects on behavior
    """

    def __init__(self, state_path: Optional[Path] = None):
        """Initialize the emotional state manager.

        Args:
            state_path: Path to persist state. If None, uses default from settings.
        """
        self.state_path = state_path or Path(settings.database_path) / "state"
        self.state_path.mkdir(parents=True, exist_ok=True)

        self.state_file = self.state_path / "current_emotional_state.json"
        self.history_file = self.state_path / "state_history.jsonl"

        # Load or initialize state
        self.current_state = self._load_state()
        self.triggers = STANDARD_TRIGGERS.copy()

        logger.info("emotional_state_manager_initialized", state_file=str(self.state_file))

    def _load_state(self) -> EmotionalState:
        """Load emotional state from disk or create new if doesn't exist."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    state = EmotionalState.model_validate(data)
                    logger.info("emotional_state_loaded", dimensions=state.dimensions.to_dict())
                    return state
            except Exception as e:
                logger.error("failed_to_load_state", error=str(e))

        # Create new neutral state
        logger.info("creating_new_emotional_state")
        return EmotionalState()

    def persist(self) -> None:
        """Persist current state to disk."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.current_state.model_dump(), f, indent=2, default=str)
            logger.debug("state_persisted")
        except Exception as e:
            logger.error("failed_to_persist_state", error=str(e))

    def snapshot(self, context: str = "", triggered_by: Optional[str] = None) -> None:
        """Take a snapshot of current state and append to history."""
        snapshot = EmotionalStateSnapshot(
            state=self.current_state.copy(), context=context, triggered_by=triggered_by
        )

        try:
            with open(self.history_file, "a") as f:
                f.write(json.dumps(snapshot.model_dump(), default=str) + "\n")
        except Exception as e:
            logger.error("failed_to_snapshot_state", error=str(e))

    def get_current_state(self) -> EmotionalState:
        """Get the current emotional state."""
        return self.current_state

    def apply_trigger(self, trigger_name: str, intensity: float = 1.0, origin: str = "") -> None:
        """Apply a predefined trigger to the emotional state.

        Args:
            trigger_name: Name of the trigger to apply
            intensity: Intensity multiplier (0-1)
            origin: Description of what caused this trigger
        """
        if trigger_name not in self.triggers:
            logger.warning("unknown_trigger", trigger_name=trigger_name)
            return

        trigger = self.triggers[trigger_name]
        logger.info(
            "applying_trigger",
            trigger=trigger_name,
            intensity=intensity,
            origin=origin,
        )

        # Calculate target dimensions
        target_dims = trigger.apply_to_state(self.current_state, intensity)

        # Store origin for narrative
        if origin:
            self.current_state.origin = origin

        # The actual transition will happen via differential update
        # Store target as temporary attribute for update() to use
        self._target_dimensions = target_dims
        self._trigger_applied = True

    def update(self, delta_t: float = 1.0) -> None:
        """Update emotional state using differential dynamics.

        This implements the key principle: states have inertia.
        They don't change instantly but move toward targets over time.

        Args:
            delta_t: Time step (typically 1.0 per interaction)
        """
        dims = self.current_state.dimensions

        # If a trigger was just applied, use target dimensions
        if hasattr(self, "_target_dimensions") and self._trigger_applied:
            target = self._target_dimensions
            self._trigger_applied = False  # Reset flag
        else:
            # Otherwise, target is current state (stable)
            target = dims

        # Differential update using time constants (tau)
        # New value = current + (target - current) * tau * delta_t
        # Lower tau = slower change (more inertia)

        new_valence = dims.valence + (target.valence - dims.valence) * self.current_state.tau_valence * delta_t

        new_activation = dims.activation + (target.activation - dims.activation) * self.current_state.tau_activation * delta_t

        new_certainty = dims.certainty + (target.certainty - dims.certainty) * self.current_state.tau_certainty * delta_t

        new_aperture = dims.aperture + (target.aperture - dims.aperture) * self.current_state.tau_aperture * delta_t

        new_connection = dims.connection + (target.connection - dims.connection) * self.current_state.tau_connection * delta_t

        # Update dimensions
        self.current_state.dimensions = EmotionalDimensions(
            valence=max(-1.0, min(1.0, new_valence)),
            activation=max(0.0, min(1.0, new_activation)),
            certainty=max(0.0, min(1.0, new_certainty)),
            aperture=max(0.0, min(1.0, new_aperture)),
            connection=max(0.0, min(1.0, new_connection)),
        )

        # Update intensity
        self.current_state.calculate_overall_intensity()

        # Increment duration
        self.current_state.duration += 1

        # Update timestamp
        self.current_state.last_updated = datetime.now()

        logger.debug(
            "state_updated",
            dimensions=self.current_state.dimensions.to_dict(),
            intensity=self.current_state.intensity,
        )

    def generate_modulation(self) -> str:
        """Generate modulation instructions for LLM prompt.

        This is where functional states become behavior-affecting.
        """
        return self.current_state.generate_modulation_instructions()

    def detect_triggers(self, user_input: str, system_response: str = "") -> List[str]:
        """Detect which triggers should be applied based on interaction content.

        This is a simple keyword-based detection for Phase 0.
        More sophisticated detection can come in later phases.

        Args:
            user_input: What the user said
            system_response: What the system responded (if available)

        Returns:
            List of trigger names to apply
        """
        detected = []

        # Simple keyword-based detection
        input_lower = user_input.lower()

        if any(word in input_lower for word in ["contradiction", "inconsistent", "you said"]):
            detected.append("contradiction_detected")

        if any(
            word in input_lower
            for word in ["what are you", "are you conscious", "do you feel", "your nature"]
        ):
            detected.append("existential_question")

        if any(word in input_lower for word in ["thank you", "appreciate", "helpful", "great"]):
            detected.append("user_recognition")

        if any(word in input_lower for word in ["challenge", "disagree", "wrong", "not true"]):
            detected.append("core_belief_challenged")

        return detected
