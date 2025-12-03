from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus

class ActivistAgent(BaseAgent):
    """
    The Activist: Drafts emails or tweets to brands regarding specific ethical violations.
    """
    def __init__(self):
        super().__init__(agent_name="The Activist")

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        # The Activist only acts if there are issues found by other agents (Judge, Corporate Detective)
        # In a real system, we would inspect the other verdicts. 
        # Here, we'll re-run a quick check or rely on passed context if we had a shared state.
        # For simplicity, let's check for "Palm Oil" or "Plastic" in the product data directly.
        
        ingredients = product_data.get("ingredients", [])
        packaging = product_data.get("packaging", "")
        brand = product_data.get("brand_owner") or product_data.get("brands", "Unknown Brand")
        
        actions = []
        
        # Check for Palm Oil violation
        has_palm_oil = False
        for ingredient in ingredients:
            if isinstance(ingredient, str) and "palm oil" in ingredient.lower():
                has_palm_oil = True
                break
        
        if has_palm_oil:
            tweet = f"Hey @{brand.replace(' ', '')}, why are you still using Palm Oil in {product_data.get('product_name')}? #Deforestation #EthicalLens"
            email = f"Subject: Concern regarding Palm Oil in {product_data.get('product_name')}\n\nDear {brand} Team,\n\nI am a concerned consumer..."
            actions.append({"type": "Tweet", "content": tweet})
            actions.append({"type": "Email Draft", "content": email})

        # Check for Plastic violation
        if "plastic" in packaging.lower():
             tweet = f"Hey @{brand.replace(' ', '')}, please switch to sustainable packaging for {product_data.get('product_name')}! #EndPlasticWaste"
             actions.append({"type": "Tweet", "content": tweet})

        if actions:
            return AgentVerdict(
                agent_name=self.agent_name,
                score=100.0, # Helper agent, always green
                status=TrafficLightStatus.GREEN,
                reasoning=f"Drafted {len(actions)} advocacy actions.",
                details={
                    "actions": actions
                }
            )

        return AgentVerdict(
            agent_name=self.agent_name,
            score=100.0,
            status=TrafficLightStatus.GREEN,
            reasoning="No advocacy actions needed.",
            details={}
        )
