from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus

class CorporateDetectiveAgent(BaseAgent):
    """
    The Corporate Detective: Traces brand ownership to find parent companies and their ethical track record.
    """
    def __init__(self):
        super().__init__(agent_name="Corporate Detective")
        # Mock Knowledge Graph / Database
        self.brand_ownership_db = {
            "Ben & Jerry's": {"parent": "Unilever", "issues": ["Plastic Pollution", "Palm Oil"]},
            "Oatly": {"parent": "Oatly Group", "investors": ["Blackstone"], "issues": ["Deforestation links (via investor)"]},
            "Innocent Drinks": {"parent": "Coca-Cola", "issues": ["Plastic Pollution", "Water Usage"]},
            "Seventh Generation": {"parent": "Unilever", "issues": ["Plastic Pollution"]}
        }

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        brand = product_data.get("brand_owner") or product_data.get("brands")
        
        if not brand or brand == "Unknown":
             return AgentVerdict(
                agent_name=self.agent_name,
                score=50.0, # Neutral score for unknown brand
                status=TrafficLightStatus.YELLOW,
                reasoning="No brand information found.",
                details={}
            )

        # Simple fuzzy match for mock DB
        parent_info = None
        matched_brand = None
        
        for db_brand, info in self.brand_ownership_db.items():
            if db_brand.lower() in brand.lower():
                parent_info = info
                matched_brand = db_brand
                break
        
        if not parent_info:
             return AgentVerdict(
                agent_name=self.agent_name,
                score=100.0,
                status=TrafficLightStatus.GREEN,
                reasoning=f"No negative records found for brand '{brand}'.",
                details={"brand_checked": brand}
            )

        parent_name = parent_info.get("parent")
        issues = parent_info.get("issues", [])
        
        score = 100.0
        if issues:
            score -= (len(issues) * 20) # -20 per issue
            
        score = max(0.0, score)
        
        status = TrafficLightStatus.GREEN
        if score < 50:
            status = TrafficLightStatus.RED
        elif score < 80:
            status = TrafficLightStatus.YELLOW

        return AgentVerdict(
            agent_name=self.agent_name,
            score=score,
            status=status,
            reasoning=f"Brand '{matched_brand}' is owned by '{parent_name}', associated with: {', '.join(issues)}.",
            details={
                "parent_company": parent_name,
                "issues": issues,
                "ownership_trace": f"{matched_brand} -> {parent_name}"
            }
        )
