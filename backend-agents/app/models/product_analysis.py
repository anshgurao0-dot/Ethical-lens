from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field

class TrafficLightStatus(str, Enum):
    RED = "RED"       # Danger/Boycott
    YELLOW = "YELLOW" # Caution
    GREEN = "GREEN"   # Safe/Ethical

class AgentVerdict(BaseModel):
    """
    Represents the findings and score from a specific agent.
    """
    agent_name: str = Field(..., description="Name of the agent (e.g., 'Bio-Shield', 'Judge').")
    score: float = Field(..., description="Compatibility score (0-100).")
    status: TrafficLightStatus = Field(..., description="Traffic light status based on the score.")
    reasoning: str = Field(..., description="Explanation for the verdict.")
    details: Dict[str, Any] = Field(default_factory=dict, description="Raw data or specific findings (e.g., detected allergens).")

class ProductAnalysis(BaseModel):
    """
    The comprehensive analysis result for a scanned product.
    """
    product_id: str = Field(..., description="Barcode or unique product ID.")
    product_name: Optional[str] = Field(None, description="Name of the product.")
    overall_score: float = Field(..., description="Aggregated compatibility score (0-100).")
    overall_status: TrafficLightStatus = Field(..., description="Overall traffic light status.")
    agent_verdicts: List[AgentVerdict] = Field(default_factory=list, description="List of verdicts from individual agents.")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the analysis.")
