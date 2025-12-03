from typing import List, Dict
from pydantic import BaseModel, Field

class RegulationMap(BaseModel):
    """
    Maps regions or contexts to specific regulations and banned ingredients.
    Used by the Researcher and Bio-Shield agents to cross-reference legal compliance.
    """
    region_code: str = Field(..., description="ISO country or region code (e.g., 'EU', 'US-CA').")
    banned_ingredients: List[str] = Field(default_factory=list, description="List of ingredients banned in this region.")
    recycling_rules: Dict[str, str] = Field(default_factory=dict, description="Map of material types to recycling instructions.")
    additives_limits: Dict[str, float] = Field(default_factory=dict, description="Max allowed concentration for specific additives.")
