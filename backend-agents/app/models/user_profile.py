from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class HealthProfile(BaseModel):
    """
    Stores health-related constraints and conditions for the user.
    Used by the Bio-Shield agent.
    """
    allergens: List[str] = Field(default_factory=list, description="List of ingredients the user is allergic to.")
    conditions: List[str] = Field(default_factory=list, description="Medical conditions (e.g., 'Diabetes', 'Hypertension').")
    age: Optional[int] = Field(None, description="User's age.")
    dietary_restrictions: List[str] = Field(default_factory=list, description="Dietary choices (e.g., 'Vegan', 'Gluten-Free').")

class ValueProfile(BaseModel):
    """
    Stores the user's ethical and sustainability priorities.
    Used by the Judge agent.
    Values are weighted from 0.0 (not important) to 1.0 (critical).
    """
    weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "palm_oil": 0.5,
            "animal_welfare": 0.5,
            "carbon_footprint": 0.5,
            "fair_labor": 0.5,
            "plastic_waste": 0.5
        },
        description="Map of ethical categories to their importance weights (0.0 to 1.0)."
    )

class UserProfile(BaseModel):
    """
    The main user profile combining health and value preferences.
    """
    user_id: str = Field(..., description="Unique identifier for the user.")
    health_profile: HealthProfile = Field(default_factory=HealthProfile)
    value_profile: ValueProfile = Field(default_factory=ValueProfile)
