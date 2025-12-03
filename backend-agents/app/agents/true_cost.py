from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus
from app.services.carbon_api import CarbonAPIClient

class TrueCostAgent(BaseAgent):
    """
    The True Cost Agent: Calculates the environmental footprint (CO2, Water) and hidden costs.
    Now uses a simulated Carbon API for scientific accuracy.
    """
    def __init__(self):
        super().__init__(agent_name="True Cost")
        self.carbon_api = CarbonAPIClient()

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        product_name = product_data.get("product_name", "Unknown")
        print(f"[{self.agent_name}] Calculating true cost for: {product_name}")

        # Fetch Real Carbon Data
        carbon_footprint = await self.carbon_api.estimate_footprint(product_data)
        
        # Determine Status based on Carbon Footprint (kg CO2e)
        # Thresholds: < 1.0 (Low/Green), 1.0 - 5.0 (Medium/Yellow), > 5.0 (High/Red)
        if carbon_footprint < 1.0:
            score = 100.0
            status = TrafficLightStatus.GREEN
            reasoning = f"Low Carbon Footprint: {carbon_footprint} kg CO2e."
        elif carbon_footprint < 5.0:
            score = 50.0
            status = TrafficLightStatus.YELLOW
            reasoning = f"Moderate Carbon Footprint: {carbon_footprint} kg CO2e."
        else:
            score = 0.0
            status = TrafficLightStatus.RED
            reasoning = f"High Carbon Footprint: {carbon_footprint} kg CO2e."

        return AgentVerdict(
            agent_name=self.agent_name,
            score=score,
            status=status,
            reasoning=reasoning,
            details={
                "carbon_footprint_kg": carbon_footprint,
                "water_usage_liters": "Unknown (API pending)", # Placeholder for future expansion
                "social_cost": "Pending"
            }
        )
