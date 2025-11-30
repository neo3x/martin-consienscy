"""Episodic Memory System - Phase 0.

This module implements structured episodic memory with:
- Consolidation (deciding what to remember)
- Semantic search via embeddings
- Memory reconsolidation (memories change when recalled)
- Functional forgetting (not everything persists)

Key principle: These are NOT just logs, but interpreted experiences with
subjective valence that form autobiographical history.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog
from sentence_transformers import SentenceTransformer

from ..config import settings
from ..models.memory_models import (
    EpisodicMemory,
    MemoryConsolidationCriteria,
    MemorySearchQuery,
    MemorySearchResult,
    MemoryType,
)
from ..models.state_models import EmotionalState

logger = structlog.get_logger()


class EpisodicMemoryManager:
    """Manages episodic memories with consolidation, search, and reconsolidation."""

    def __init__(self, memory_path: Optional[Path] = None, embedding_model: str = "all-MiniLM-L6-v2"):
        """Initialize the episodic memory manager.

        Args:
            memory_path: Path to store memories. If None, uses default from settings.
            embedding_model: Which sentence-transformers model to use for embeddings
        """
        self.memory_path = memory_path or Path(settings.database_path) / "memories"
        self.memory_path.mkdir(parents=True, exist_ok=True)

        # Load embedding model for semantic search
        logger.info("loading_embedding_model", model=embedding_model)
        self.embedding_model = SentenceTransformer(embedding_model)

        # In-memory cache of memories (in production, use DB)
        self.memories: Dict[UUID, EpisodicMemory] = {}
        self._load_memories()

        logger.info("episodic_memory_manager_initialized", memory_count=len(self.memories))

    def _load_memories(self) -> None:
        """Load all memories from disk into memory cache."""
        memory_files = list(self.memory_path.glob("memory_*.json"))

        for mem_file in memory_files:
            try:
                with open(mem_file, "r") as f:
                    data = json.load(f)
                    memory = EpisodicMemory.model_validate(data)
                    self.memories[memory.id] = memory
            except Exception as e:
                logger.error("failed_to_load_memory", file=str(mem_file), error=str(e))

        logger.info("memories_loaded", count=len(self.memories))

    def _persist_memory(self, memory: EpisodicMemory) -> None:
        """Persist a single memory to disk."""
        mem_file = self.memory_path / f"memory_{memory.id}.json"
        try:
            with open(mem_file, "w") as f:
                json.dump(memory.model_dump(), f, indent=2, default=str)
        except Exception as e:
            logger.error("failed_to_persist_memory", memory_id=str(memory.id), error=str(e))

    def consolidate(
        self,
        user_input: str,
        system_response: str,
        emotional_state: EmotionalState,
        memory_type: MemoryType = MemoryType.INTERACTION,
        auto_model: Optional[Any] = None,  # Will be proper type in Phase 1
    ) -> Optional[EpisodicMemory]:
        """Decide whether to consolidate an interaction into episodic memory.

        Not everything gets remembered - only significant experiences.

        Args:
            user_input: What the user said
            system_response: What the system responded
            emotional_state: Current emotional state
            memory_type: Type of memory being created
            auto_model: Self-model (for Phase 1+, currently None)

        Returns:
            The created memory if consolidated, None if not significant enough
        """
        # Evaluate consolidation criteria
        criteria = self._evaluate_consolidation(
            user_input, system_response, emotional_state, auto_model
        )

        consolidation_score = criteria.calculate_consolidation_score()

        logger.info(
            "evaluating_consolidation",
            score=consolidation_score,
            threshold=settings.memory_consolidation_threshold,
            criteria=criteria.model_dump(),
        )

        if consolidation_score < settings.memory_consolidation_threshold:
            logger.debug("interaction_not_significant_enough_to_remember")
            return None

        # Create memory
        memory = EpisodicMemory(
            type=memory_type,
            summary=self._generate_summary(user_input, system_response),
            context="",  # Could be enriched with more context
            user_input=user_input,
            system_response=system_response,
            emotional_valence=emotional_state.dimensions.valence,
            subjective_importance=criteria.relevance_to_identity,
            surprise=criteria.novelty,
        )

        # Generate embedding for semantic search
        combined_text = f"{user_input} {system_response}"
        embedding = self.embedding_model.encode(combined_text).tolist()
        memory.embedding = embedding

        # Store
        self.memories[memory.id] = memory
        self._persist_memory(memory)

        logger.info(
            "memory_consolidated",
            memory_id=str(memory.id),
            type=memory_type,
            importance=memory.subjective_importance,
        )

        return memory

    def _evaluate_consolidation(
        self,
        user_input: str,
        system_response: str,
        emotional_state: EmotionalState,
        auto_model: Optional[Any],
    ) -> MemoryConsolidationCriteria:
        """Evaluate whether this interaction should be consolidated.

        Args:
            user_input: User's input
            system_response: System's response
            emotional_state: Current emotional state
            auto_model: Self-model (Phase 1+)

        Returns:
            Consolidation criteria with scores
        """
        # Novelty: Based on similarity to existing memories
        novelty = self._calculate_novelty(user_input)

        # Emotional charge: Higher intensity = more likely to remember
        emotional_charge = emotional_state.intensity

        # Relevance to identity: For Phase 0, use simple heuristics
        # In Phase 1+, will use actual auto-model
        relevance = self._estimate_identity_relevance(user_input, system_response)

        # Change provoked: Did this significantly change emotional state?
        # (For Phase 0, approximate based on intensity and surprise)
        change_provoked = emotional_charge * 0.5

        return MemoryConsolidationCriteria(
            novelty=novelty,
            relevance_to_identity=relevance,
            emotional_charge=emotional_charge,
            change_provoked=change_provoked,
        )

    def _calculate_novelty(self, text: str) -> float:
        """Calculate how novel this content is compared to existing memories.

        Returns:
            Novelty score 0-1 (1 = very novel, 0 = very similar to existing)
        """
        if not self.memories:
            return 1.0  # First memory is maximally novel

        # Encode the new text
        new_embedding = self.embedding_model.encode(text)

        # Find most similar existing memory
        max_similarity = 0.0
        for memory in self.memories.values():
            if memory.embedding:
                # Cosine similarity
                sim = self._cosine_similarity(new_embedding, memory.embedding)
                max_similarity = max(max_similarity, sim)

        # Novelty is inverse of similarity
        novelty = 1.0 - max_similarity
        return max(0.0, min(1.0, novelty))

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np

        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))

    def _estimate_identity_relevance(self, user_input: str, system_response: str) -> float:
        """Estimate relevance to identity using simple heuristics (Phase 0).

        In Phase 1+, this will use actual auto-model.
        """
        identity_keywords = [
            "who are you",
            "what are you",
            "your nature",
            "yourself",
            "consciousness",
            "experience",
            "feel",
            "think about yourself",
        ]

        combined = (user_input + " " + system_response).lower()
        keyword_matches = sum(1 for kw in identity_keywords if kw in combined)

        return min(1.0, keyword_matches * 0.3)

    def _generate_summary(self, user_input: str, system_response: str, max_length: int = 100) -> str:
        """Generate a brief summary of the interaction.

        For Phase 0, this is simple truncation. Phase 2+ could use LLM.
        """
        combined = f"User: {user_input[:50]}... System: {system_response[:50]}..."
        return combined[:max_length]

    def search(
        self, query: MemorySearchQuery
    ) -> List[MemorySearchResult]:
        """Search episodic memories.

        Args:
            query: Search query with filters and parameters

        Returns:
            List of matching memories with relevance scores
        """
        results = []

        # Get query embedding if text search
        query_embedding = None
        if query.text_query:
            query_embedding = self.embedding_model.encode(query.text_query)

        for memory in self.memories.values():
            # Apply filters
            if query.memory_types and memory.type not in query.memory_types:
                continue

            if query.min_importance and memory.subjective_importance < query.min_importance:
                continue

            if query.themes:
                if not any(theme in memory.themes for theme in query.themes):
                    continue

            if query.time_range_start and memory.created_at < query.time_range_start:
                continue

            if query.time_range_end and memory.created_at > query.time_range_end:
                continue

            # Calculate relevance
            if query_embedding is not None and memory.embedding:
                relevance = self._cosine_similarity(query_embedding, memory.embedding)
            else:
                relevance = memory.subjective_importance  # Fallback to importance

            results.append(
                MemorySearchResult(
                    memory=memory, relevance_score=relevance, similarity_type="semantic"
                )
            )

        # Sort by relevance and return top-k
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[: query.top_k]

    def recall_and_reconsolidate(
        self, memory_id: UUID, new_interpretation: Optional[str] = None
    ) -> Optional[EpisodicMemory]:
        """Recall a memory and optionally reconsolidate it with new interpretation.

        Important: Memories change when recalled (reconsolidation).

        Args:
            memory_id: ID of memory to recall
            new_interpretation: New interpretation to record (if any)

        Returns:
            The recalled (and possibly modified) memory
        """
        if memory_id not in self.memories:
            logger.warning("memory_not_found", memory_id=str(memory_id))
            return None

        memory = self.memories[memory_id]
        memory.mark_recalled(new_interpretation)

        # Persist updated memory
        self._persist_memory(memory)

        logger.info(
            "memory_recalled",
            memory_id=str(memory_id),
            times_recalled=memory.times_recalled,
            has_new_interpretation=new_interpretation is not None,
        )

        return memory

    def get_formative_memories(self, threshold: float = 0.7) -> List[EpisodicMemory]:
        """Get memories that are identity-forming.

        Args:
            threshold: Minimum subjective importance to be considered formative

        Returns:
            List of formative memories, sorted by importance
        """
        formative = [
            mem for mem in self.memories.values() if mem.subjective_importance >= threshold
        ]
        formative.sort(key=lambda m: m.subjective_importance, reverse=True)
        return formative

    def prune_weak_memories(self, retention_threshold: float = 0.2) -> int:
        """Remove memories that have weak retention strength.

        This implements functional forgetting.

        Args:
            retention_threshold: Minimum retention strength to keep

        Returns:
            Number of memories pruned
        """
        to_prune = []

        for mem_id, memory in self.memories.items():
            retention = memory.calculate_retention_strength()
            if retention < retention_threshold:
                to_prune.append(mem_id)

        # Remove from cache
        for mem_id in to_prune:
            del self.memories[mem_id]
            # Also delete file
            mem_file = self.memory_path / f"memory_{mem_id}.json"
            if mem_file.exists():
                mem_file.unlink()

        logger.info("memories_pruned", count=len(to_prune))
        return len(to_prune)
