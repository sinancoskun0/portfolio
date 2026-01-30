"""
Risk Calculator Module
Handles risk scoring logic.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class RiskRating(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class RiskEntry:
    """This is a single risk assessment entry."""
    asset: str
    threat: str
    likelihood_inherent: int  # 1-5
    impact_inherent: int      # 1-5
    controls: str
    likelihood_residual: int  # 1-5
    impact_residual: int      # 1-5
    
    @property
    def inherent_risk_score(self) -> int:
        return self.likelihood_inherent * self.impact_inherent
    
    @property
    def residual_risk_score(self) -> int:
        return self.likelihood_residual * self.impact_residual
    
    @property
    def inherent_risk_rating(self) -> RiskRating:
        return get_risk_rating(self.inherent_risk_score)
    
    @property
    def residual_risk_rating(self) -> RiskRating:
        return get_risk_rating(self.residual_risk_score)
    
    @property
    def risk_reduction(self) -> int:
        """Percentage reduction from inherent to residual risk."""
        if self.inherent_risk_score == 0:
            return 0
        return round((1 - self.residual_risk_score / self.inherent_risk_score) * 100)


def get_risk_rating(score: int) -> RiskRating:
    """Convert score to rating category"""
    if score <= 4:
        return RiskRating.LOW
    elif score <= 9:
        return RiskRating.MEDIUM
    elif score <= 16:
        return RiskRating.HIGH
    else:
        return RiskRating.CRITICAL


def get_rating_color(rating: RiskRating) -> str:
    """Return ´color"""
    colors = {
        RiskRating.LOW: "#28a745",      # Green
        RiskRating.MEDIUM: "#ffc107",   # Yellow
        RiskRating.HIGH: "#fd7e14",     # Orange
        RiskRating.CRITICAL: "#dc3545"  # Red
    }
    return colors.get(rating, "#6c757d")


def get_action_required(rating: RiskRating) -> str:
    """Return policy"""
    actions = {
        RiskRating.LOW: "Accept / Monitor annually",
        RiskRating.MEDIUM: "Handle within 90 days",
        RiskRating.HIGH: "Handle within 30 days",
        RiskRating.CRITICAL: "Immediate action required"
    }
    return actions.get(rating, "Review required")


# Likelihood scale descriptions
LIKELIHOOD_SCALE = {
    1: ("Rare", "May occur, though rarely (<5%)"),
    2: ("Unlikely", "Could occur but not expected (5-25%)"),
    3: ("Possible", "Might occur at some time (25-50%)"),
    4: ("Likely", "Will probably occur (50-75%)"),
    5: ("Almost Certain", "Expected to occur in most circumstances (>75%)")
}

# Impact scale descriptions
IMPACT_SCALE = {
    1: ("Negligible", "Minimal impact, easily absorbed"),
    2: ("Minor", "Small impact, minor disruption"),
    3: ("Moderate", "Noticeable impact, some disruption"),
    4: ("Major", "Significant impact, major disruption"),
    5: ("Severe", "Critical impact, potential business failure")
}


def generate_risk_matrix() -> List[List[dict]]:
    """Generate 5x5 risk matrix with scores and colors"""
    matrix = []
    for likelihood in range(5, 0, -1):  # 5 to 1 (top to bottom)
        row = []
        for impact in range(1, 6):  # 1 to 5 (left to right)
            score = likelihood * impact
            rating = get_risk_rating(score)
            row.append({
                "score": score,
                "rating": rating.value,
                "color": get_rating_color(rating),
                "likelihood": likelihood,
                "impact": impact
            })
        matrix.append(row)
    return matrix
