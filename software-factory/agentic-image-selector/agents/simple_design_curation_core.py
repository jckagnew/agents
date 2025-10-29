"""
Shared design curation utilities for Agentic Image Selector workflows.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import json


@dataclass
class ImagePair:
    before_url: str
    after_url: str
    before_description: str
    after_description: str
    source: str
    project_type: str
    quality_score: float = 0.0
    commercial_appeal: float = 0.0
    animation_potential: float = 0.0
    overall_score: float = 0.0


class SimpleDesignCurationAgent:
    """Heuristic curator for ranking image pairs."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.project_type = config.get("projectType", "unknown")
        self.evaluation_criteria = config.get("evaluationCriteria", {})
        self.commercial_weight = config.get("commercialWeight", 0.4)

    def evaluate_image_pair(self, pair: Dict[str, Any]) -> Dict[str, float]:
        scores = {
            "commercial_appeal": 0.0,
            "animation_potential": 0.0,
            "design_quality": 0.0,
            "overall": 0.0,
        }

        before_desc = pair.get("before_description", "").lower()
        after_desc = pair.get("after_description", "").lower()
        source = pair.get("source", "").lower()

        commercial_score = 0.5
        fitness_keywords = [
            "fitness",
            "health",
            "gym",
            "workout",
            "exercise",
            "transformation",
            "weight",
            "muscle",
            "strength",
        ]
        commercial_score += min(
            sum(1 for keyword in fitness_keywords if keyword in before_desc or keyword in after_desc) * 0.1,
            0.3,
        )
        positive_words = [
            "success",
            "progress",
            "improvement",
            "better",
            "strong",
            "fit",
            "healthy",
            "motivation",
        ]
        commercial_score += min(
            sum(1 for word in positive_words if word in before_desc or word in after_desc) * 0.05,
            0.2,
        )
        if "pexels" in source:
            commercial_score += 0.1
        if "pixabay" in source:
            commercial_score += 0.05
        scores["commercial_appeal"] = min(commercial_score, 1.0)

        animation_score = 0.6
        if "transformation" in before_desc or "transformation" in after_desc:
            animation_score += 0.2
        if "before" in before_desc and "after" in after_desc:
            animation_score += 0.1
        people_keywords = ["woman", "man", "person", "character", "people", "figure"]
        animation_score += min(
            sum(1 for keyword in people_keywords if keyword in before_desc or keyword in after_desc) * 0.05,
            0.2,
        )
        scores["animation_potential"] = min(animation_score, 1.0)

        design_score = 0.5
        desc_length = len(before_desc) + len(after_desc)
        if desc_length > 100:
            design_score += 0.2
        elif desc_length > 50:
            design_score += 0.1
        if "pexels" in source:
            design_score += 0.2
        if "pixabay" in source:
            design_score += 0.1
        if "illustration" in before_desc or "illustration" in after_desc:
            design_score += 0.1
        scores["design_quality"] = min(design_score, 1.0)

        weights = self.evaluation_criteria or {
            "commercial_appeal": 0.4,
            "animation_potential": 0.3,
            "design_quality": 0.3,
        }
        scores["overall"] = (
            scores["commercial_appeal"] * weights.get("commercial_appeal", 0.4)
            + scores["animation_potential"] * weights.get("animation_potential", 0.3)
            + scores["design_quality"] * weights.get("design_quality", 0.3)
        )

        return scores

    def curate_image_pairs(self, pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        evaluated_pairs = []

        for pair in pairs:
            scores = self.evaluate_image_pair(pair)
            pair["scores"] = scores
            pair["quality_score"] = scores["design_quality"]
            pair["commercial_appeal"] = scores["commercial_appeal"]
            pair["animation_potential"] = scores["animation_potential"]
            pair["overall_score"] = scores["overall"]
            evaluated_pairs.append(pair)

        evaluated_pairs.sort(key=lambda x: x["overall_score"], reverse=True)
        return evaluated_pairs

    def select_top_pairs(self, evaluated_pairs: List[Dict[str, Any]], count: int = 3) -> List[Dict[str, Any]]:
        return evaluated_pairs[:count]

    def save_results(self, top_pairs: List[Dict[str, Any]], output_file: Path) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "project_type": self.project_type,
            "total_pairs_evaluated": len(top_pairs),
            "top_pairs": top_pairs,
            "evaluation_criteria": self.evaluation_criteria,
            "commercial_weight": self.commercial_weight,
        }

        with open(output_file, "w") as handle:
            json.dump(payload, handle, indent=2)
