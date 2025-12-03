from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus

class LocalvoreScoutAgent(BaseAgent):
    """
    The Localvore Scout: Calculates "Food Miles" by detecting the Country of Origin.
    """
    def __init__(self):
        super().__init__(agent_name="Localvore Scout")
        # Mock User Location (Ideally this comes from the mobile app context)
        self.user_country = "United States" # Default

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        # Extract Origin Data
        # Open Food Facts often has 'origins' or 'manufacturing_places'
        raw_data = product_data.get("raw_data", {})
        origins = raw_data.get("origins", "") or raw_data.get("manufacturing_places", "")
        
        if not origins:
             return AgentVerdict(
                agent_name=self.agent_name,
                score=50.0,
                status=TrafficLightStatus.YELLOW,
                reasoning="Country of origin not found.",
                details={}
            )

        # Simple logic: Check if user country is in origin string
        # In reality, we'd use geocoding to calculate distance
        is_local = self.user_country.lower() in origins.lower()
        
        score = 100.0 if is_local else 40.0
        status = TrafficLightStatus.GREEN if is_local else TrafficLightStatus.YELLOW
        
        reasoning = f"Product origin: {origins}. "
        reasoning += "Locally sourced!" if is_local else "Imported (High Food Miles)."

        return AgentVerdict(
            agent_name=self.agent_name,
            score=score,
            status=status,
            reasoning=reasoning,
            details={
                "origin": origins,
                "is_local": is_local,
                "user_location_assumed": self.user_country
            }
        )
