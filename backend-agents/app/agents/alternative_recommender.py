from typing import Any, Dict, List
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus

class AlternativeRecommenderAgent(BaseAgent):
    """
    The Alternative Recommender: Suggests compliant alternatives if the scanned product is rejected.
    """
    def __init__(self):
        super().__init__(agent_name="Alternative Recommender")
        # Mock Database of Alternatives
        # In reality, this would query a product DB filtering by user constraints
        self.alternatives_db = {
            "Milk": [
                {"name": "Oatly Barista Edition", "reason": "Low Carbon, Vegan"},
                {"name": "Almond Breeze", "reason": "Vegan, Low Calorie"}
            ],
            "Soda": [
                {"name": "Zevia Zero Calorie", "reason": "No Sugar, No Artificial Colors"},
                {"name": "Spindrift Sparkling Water", "reason": "Natural Ingredients"}
            ],
            "Spread": [
                {"name": "Rigoni di Asiago Nocciolata", "reason": "Palm Oil Free, Organic"},
                {"name": "Justin's Hazelnut Butter", "reason": "Less Sugar"}
            ]
        }

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        # Check if we need to recommend anything
        # We look at the 'current_status' passed in context, or we assume we run after others
        # For simplicity, we'll always provide recommendations if we can match the category
        
        # Try to guess category from product name or keywords
        product_name = product_data.get("product_name", "").lower()
        category = None
        
        if "milk" in product_name or "oat" in product_name or "dairy" in product_name:
            category = "Milk"
        elif "cola" in product_name or "soda" in product_name or "drink" in product_name:
            category = "Soda"
        elif "spread" in product_name or "nutella" in product_name or "butter" in product_name:
            category = "Spread"
            
        if not category:
             return AgentVerdict(
                agent_name=self.agent_name,
                score=100.0,
                status=TrafficLightStatus.GREEN, # Neutral
                reasoning="No specific category detected for recommendations.",
                details={}
            )

        recommendations = self.alternatives_db.get(category, [])
        
        return AgentVerdict(
            agent_name=self.agent_name,
            score=100.0,
            status=TrafficLightStatus.GREEN, # Always Green as it's a helper
            reasoning=f"Found {len(recommendations)} alternatives for category '{category}'.",
            details={
                "category": category,
                "recommendations": recommendations
            }
        )
