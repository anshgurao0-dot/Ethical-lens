from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus
from app.models.user_profile import UserProfile

class JudgeAgent(BaseAgent):
    """
    The Judge: Compares findings against the user's ValueProfile.
    """
    def __init__(self):
        super().__init__(agent_name="Judge")

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        user_profile: UserProfile = context.get("user_profile")
        if not user_profile:
             return AgentVerdict(
                agent_name=self.agent_name,
                score=50.0,
                status=TrafficLightStatus.YELLOW,
                reasoning="No user profile provided for value judgment.",
                details={}
            )

        weights = user_profile.value_profile.weights
        ingredients = product_data.get("ingredients", [])
        # Ensure ingredients is a list of strings
        if not isinstance(ingredients, list):
            ingredients = []
            
        score = 100.0
        reasons = []
        
        # Define some simple keyword maps for values (in a real app, this would be a Knowledge Graph or DB)
        value_keywords = {
            "palm_oil": ["palm oil", "palmitate", "palm kernel"],
            "animal_welfare": ["gelatin", "lard", "tallow"], # Simple check for non-vegan items as proxy
            "plastic_waste": [], # Hard to check from ingredients alone
            "fair_labor": [] # Hard to check from ingredients alone
        }

        for value_category, weight in weights.items():
            if weight <= 0:
                continue
                
            keywords = value_keywords.get(value_category, [])
            for keyword in keywords:
                for ingredient in ingredients:
                    if isinstance(ingredient, str) and keyword.lower() in ingredient.lower():
                        # Penalty proportional to weight. 
                        # If weight is 1.0 (Critical), penalty is high (e.g., -50).
                        # If weight is 0.5, penalty is -25.
                        penalty = 50.0 * weight
                        score -= penalty
                        reasons.append(f"Found {keyword} ({value_category} conflict)")
                        break # Count once per category
        
        # Normalize score
        score = max(0.0, min(100.0, score))
            
        status = TrafficLightStatus.GREEN
        if score < 50:
            status = TrafficLightStatus.RED
        elif score < 80:
            status = TrafficLightStatus.YELLOW

        return AgentVerdict(
            agent_name=self.agent_name,
            score=score,
            status=status,
            reasoning="; ".join(reasons) if reasons else "Aligned with values.",
            details={"weights_applied": weights, "final_score": score}
        )
