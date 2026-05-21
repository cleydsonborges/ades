"""
Champion/Challenger model router for healthcare and finance forecasting.

Phase 3 will add RL-based routing; Phase 1 exposes the interface and stub selection.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ModelRole(StrEnum):
    CHAMPION = "champion"
    CHALLENGER = "challenger"


@dataclass
class PredictionRequest:
    sector: str  # healthcare | finance
    feature_vector: dict[str, Any]
    model_ids: list[str]


@dataclass
class PredictionResult:
    model_id: str
    role: ModelRole
    score: float
    metadata: dict[str, Any]


class ChampionChallengerRouter:
    """Route requests to champion or challenger models based on stub accuracy scores."""

    def __init__(self, champion_id: str, challenger_ids: list[str] | None = None) -> None:
        self.champion_id = champion_id
        self.challenger_ids = challenger_ids or []

    def predict(self, request: PredictionRequest) -> PredictionResult:
        """Select model; Phase 1 returns champion by default."""
        model_id = self.champion_id
        if request.model_ids and request.model_ids[0] in self.challenger_ids:
            model_id = request.model_ids[0]
            role = ModelRole.CHALLENGER
        else:
            role = ModelRole.CHAMPION
        return PredictionResult(
            model_id=model_id,
            role=role,
            score=0.0,
            metadata={"sector": request.sector, "stub": True},
        )
