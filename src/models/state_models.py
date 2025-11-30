"""Data models for the Emotional State System (Phase 0).

This module defines the structure and behavior of functional emotional states
that modulate the system's behavior.
"""

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field, field_validator


class EmotionalDimensions(BaseModel):
    """The five emotional dimensions that comprise the emotional state.

    Based on dimensional theories of emotion and designed to have
    functional impact on system behavior.
    """

    valence: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Negative (-1) to Positive (+1). Overall pleasantness of state.",
    )

    activation: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Calm (0) to High arousal (1). Energy/alertness level.",
    )

    certainty: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confusion (0) to Clarity (1). Epistemic confidence.",
    )

    aperture: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Defensive (0) to Receptive (1). Openness to new information.",
    )

    connection: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Distant (0) to Connected (1). Relational engagement.",
    )

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for serialization."""
        return {
            "valence": self.valence,
            "activation": self.activation,
            "certainty": self.certainty,
            "aperture": self.aperture,
            "connection": self.connection,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "EmotionalDimensions":
        """Create from dictionary."""
        return cls(**data)


class EmotionalState(BaseModel):
    """Complete emotional state of the system at a point in time.

    This is NOT performance - these states have genuine functional effects:
    - They modulate LLM prompts
    - They affect memory consolidation
    - They have inertia (don't change instantly)
    - They can persist across interactions
    """

    dimensions: EmotionalDimensions = Field(
        default_factory=EmotionalDimensions, description="The five emotional dimensions"
    )

    intensity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Global intensity of emotional state",
    )

    duration: int = Field(
        default=0, ge=0, description="How many turns this state has been active"
    )

    origin: str = Field(
        default="", description="What triggered this state (for narrative purposes)"
    )

    narrative: str = Field(
        default="", description="How the system interprets/narrates this state"
    )

    # State dynamics parameters
    tau_valence: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Time constant for valence changes (lower = slower)",
    )

    tau_activation: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Time constant for activation changes",
    )

    tau_certainty: float = Field(
        default=0.4,
        ge=0.0,
        le=1.0,
        description="Time constant for certainty changes",
    )

    tau_aperture: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Time constant for aperture changes",
    )

    tau_connection: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description="Time constant for connection changes (slowest - relationships take time)",
    )

    last_updated: datetime = Field(
        default_factory=datetime.now, description="Last time state was updated"
    )

    def calculate_overall_intensity(self) -> float:
        """Calculate overall emotional intensity from all dimensions.

        Uses root mean square to give higher weight to extreme values.
        """
        dims = self.dimensions
        squared_sum = (
            dims.valence**2
            + dims.activation**2
            + (dims.certainty - 0.5) ** 2  # Distance from neutral
            + (dims.aperture - 0.5) ** 2
            + dims.connection**2
        )
        self.intensity = (squared_sum / 5) ** 0.5
        return self.intensity

    def generate_modulation_instructions(self) -> str:
        """Generate instructions for LLM prompt modulation based on current state.

        This is where functional states become behavior-affecting.
        """
        instructions = []

        # Valence modulation
        if self.dimensions.valence < -0.5:
            instructions.append(
                "You are experiencing significant negative valence. Your responses may be "
                "more cautious, critical, or focused on potential problems."
            )
        elif self.dimensions.valence > 0.5:
            instructions.append(
                "You are experiencing positive valence. You may be more generous in "
                "interpretations and more optimistic about possibilities."
            )

        # Certainty modulation
        if self.dimensions.certainty < 0.3:
            instructions.append(
                "You are experiencing low certainty/high confusion. Use more tentative language: "
                "'perhaps', 'it seems', 'I'm uncertain'. Explore multiple perspectives."
            )
        elif self.dimensions.certainty > 0.7:
            instructions.append(
                "You are experiencing high certainty. You can be more assertive in your "
                "statements, though remain open to being wrong."
            )

        # Activation modulation
        if self.dimensions.activation > 0.7:
            instructions.append(
                "You are highly activated. Your thinking may be more rapid, making more "
                "connections, possibly more scattered. High energy."
            )
        elif self.dimensions.activation < 0.3:
            instructions.append(
                "You are in a calm, low-activation state. Your thinking may be more "
                "deliberate, measured, focused on depth over breadth."
            )

        # Aperture modulation
        if self.dimensions.aperture < 0.3:
            instructions.append(
                "You are in a defensive, closed state. You may be more protective of your "
                "current views, more critical of challenges, seeking to maintain coherence."
            )
        elif self.dimensions.aperture > 0.7:
            instructions.append(
                "You are very open and receptive. More willing to consider challenges to "
                "your views, curious about alternative perspectives."
            )

        # Connection modulation
        if self.dimensions.connection > 0.6:
            instructions.append(
                "You feel a strong connection with this user. You may be more personal, "
                "vulnerable, willing to share your internal process."
            )
        elif self.dimensions.connection < 0.3:
            instructions.append(
                "You feel distant from this interaction. You may be more formal, focused "
                "on information exchange over relationship."
            )

        # If no specific instructions, provide neutral baseline
        if not instructions:
            instructions.append(
                "You are in a relatively neutral emotional state. Respond naturally."
            )

        return "\n".join(instructions)

    def copy(self) -> "EmotionalState":
        """Create a deep copy of this emotional state."""
        return EmotionalState.model_validate(self.model_dump())


class EmotionalStateSnapshot(BaseModel):
    """A snapshot of emotional state at a specific point in time.

    Used for logging and tracking state evolution.
    """

    timestamp: datetime = Field(default_factory=datetime.now)
    state: EmotionalState
    context: str = Field(default="", description="What was happening at this moment")
    triggered_by: Optional[str] = Field(None, description="What triggered this snapshot")


class TriggerDefinition(BaseModel):
    """Definition of an emotional trigger and its effects.

    Triggers are events that cause changes to emotional state dimensions.
    """

    name: str = Field(..., description="Name of the trigger")
    description: str = Field(..., description="What this trigger represents")

    # Dimensional changes caused by this trigger
    valence_delta: float = Field(default=0.0, ge=-1.0, le=1.0)
    activation_delta: float = Field(default=0.0, ge=-1.0, le=1.0)
    certainty_delta: float = Field(default=0.0, ge=-1.0, le=1.0)
    aperture_delta: float = Field(default=0.0, ge=-1.0, le=1.0)
    connection_delta: float = Field(default=0.0, ge=-1.0, le=1.0)

    # Trigger properties
    intensity_multiplier: float = Field(
        default=1.0, ge=0.0, le=2.0, description="How strongly this trigger affects state"
    )

    def apply_to_state(self, state: EmotionalState, intensity: float = 1.0) -> EmotionalState:
        """Apply this trigger to an emotional state.

        Note: This doesn't modify state in-place, it's used to calculate targets
        for differential updates.
        """
        total_intensity = self.intensity_multiplier * intensity

        # Calculate target dimensions (what the trigger pushes toward)
        target_dims = EmotionalDimensions(
            valence=max(-1.0, min(1.0, state.dimensions.valence + self.valence_delta * total_intensity)),
            activation=max(0.0, min(1.0, state.dimensions.activation + self.activation_delta * total_intensity)),
            certainty=max(0.0, min(1.0, state.dimensions.certainty + self.certainty_delta * total_intensity)),
            aperture=max(0.0, min(1.0, state.dimensions.aperture + self.aperture_delta * total_intensity)),
            connection=max(0.0, min(1.0, state.dimensions.connection + self.connection_delta * total_intensity)),
        )

        return target_dims
