from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus

class CircularGuideAgent(BaseAgent):
    """
    The Circular Guide: Provides local recycling advice based on product packaging and user location.
    """
    def __init__(self):
        super().__init__(agent_name="Circular Guide")
        # Mock Local Recycling Rules DB
        # In reality, this would use RAG or an API like Recyclops/Earth911
        self.recycling_rules = {
            "default": {
                "Plastic": "Recycle in Blue Bin (Clean & Dry)",
                "Glass": "Recycle in Green Bin",
                "Paper": "Recycle in Blue Bin",
                "Composite": "Trash (Not Recyclable)"
            },
            "San Francisco, CA": {
                "Plastic": "Recycle (Blue Bin)",
                "Glass": "Recycle (Blue Bin)",
                "Compostable": "Compost (Green Bin)"
            }
        }

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        # Extract packaging info (Mocking extraction from raw data if not present)
        packaging = product_data.get("packaging", "Plastic") # Default to Plastic if unknown
        
        # Determine location (Mocking location from context or default)
        location = context.get("location", "default")
        
        rules = self.recycling_rules.get(location, self.recycling_rules["default"])
        
        advice = rules.get(packaging)
        if not advice:
            # Fallback for unknown materials
            advice = "Check local guidelines. Status unknown."
            status = TrafficLightStatus.YELLOW
        elif "Trash" in advice:
            status = TrafficLightStatus.RED # Not recyclable
        else:
            status = TrafficLightStatus.GREEN # Recyclable

        return AgentVerdict(
            agent_name=self.agent_name,
            score=100.0 if status == TrafficLightStatus.GREEN else 0.0,
            status=status,
            reasoning=f"Packaging '{packaging}': {advice}",
            details={
                "packaging_detected": packaging,
                "location_used": location,
                "disposal_instructions": advice
            }
        )
