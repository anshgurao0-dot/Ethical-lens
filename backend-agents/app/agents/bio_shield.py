from typing import Any, Dict, List
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus
from app.models.user_profile import UserProfile

class BioShieldAgent(BaseAgent):
    """
    The Bio-Shield: Checks ingredients against the user's HealthProfile.
    """
    def __init__(self):
        super().__init__(agent_name="Bio-Shield")

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        user_profile: UserProfile = context.get("user_profile")
        if not user_profile:
            return AgentVerdict(
                agent_name=self.agent_name,
                score=0.0,
                status=TrafficLightStatus.YELLOW,
                reasoning="No user profile provided for health check.",
                details={}
            )

        ingredients = product_data.get("ingredients", [])
        # Ensure ingredients is a list of strings
        if not isinstance(ingredients, list):
            ingredients = []
            
        allergens = user_profile.health_profile.allergens
        
        # 1. Allergen Check
        detected_allergens = []
        for ingredient in ingredients:
            if not isinstance(ingredient, str):
                continue
            for allergen in allergens:
                if allergen.lower() in ingredient.lower():
                    detected_allergens.append(ingredient)
                    break
        
        if detected_allergens:
             return AgentVerdict(
                agent_name=self.agent_name,
                score=0.0,
                status=TrafficLightStatus.RED,
                reasoning=f"Detected allergens: {', '.join(detected_allergens)}",
                details={"detected_allergens": detected_allergens}
            )

        # 2. Disease Guard (Diabetes, Hypertension)
        conditions = user_profile.health_profile.conditions
        nutriments = product_data.get("raw_data", {}).get("nutriments", {})
        
        warnings = []
        
        # Diabetes Check (High Sugar)
        if "Diabetes" in conditions:
            sugars_100g = nutriments.get("sugars_100g", 0)
            if sugars_100g > 10: # Threshold: 10g/100g
                warnings.append(f"High Sugar ({sugars_100g}g/100g) - Risk for Diabetes")

        # Hypertension Check (High Sodium)
        if "Hypertension" in conditions:
            salt_100g = nutriments.get("salt_100g", 0)
            if salt_100g > 1.5: # Threshold: 1.5g/100g (High salt)
                warnings.append(f"High Salt ({salt_100g}g/100g) - Risk for Hypertension")

        # 3. Age Check
        age = user_profile.health_profile.age
        if age is not None and age < 18:
            # Check for Alcohol or High Caffeine
            # Simple keyword check for now
            restricted_keywords = ["alcohol", "wine", "beer", "caffeine", "coffee", "energy drink"]
            for keyword in restricted_keywords:
                for ingredient in ingredients:
                     if isinstance(ingredient, str) and keyword in ingredient.lower():
                        warnings.append(f"Contains {keyword} - Not recommended for age {age}")
                        break

        # 4. Contraindication Guard (Mock)
        # Example: MAOIs vs Aged Cheese (Tyramine)
        # In a real app, we'd check user medications against food interactions
        if "MAOI" in user_profile.health_profile.dietary_restrictions: # Using dietary_restrictions field for meds mock
             if "cheese" in [i.lower() for i in ingredients if isinstance(i, str)]:
                 warnings.append("Potential Interaction: Cheese contains Tyramine (avoid with MAOIs)")

        # 5. Cosmetic Safety Guard
        # Check for common harmful chemicals in beauty products
        category = product_data.get("category", "unknown")
        if category == "beauty" or True: # Check everywhere for now, as these shouldn't be in food either
            toxins = ["paraben", "sulfate", "phthalate", "formaldehyde", "triclosan"]
            for toxin in toxins:
                for ingredient in ingredients:
                    if isinstance(ingredient, str) and toxin in ingredient.lower():
                        warnings.append(f"Contains {ingredient} (Potential Toxin: {toxin.title()})")

        if warnings:
            return AgentVerdict(
                agent_name=self.agent_name,
                score=50.0, # Warning level
                status=TrafficLightStatus.YELLOW,
                reasoning="; ".join(warnings),
                details={"warnings": warnings}
            )

        return AgentVerdict(
            agent_name=self.agent_name,
            score=100.0,
            status=TrafficLightStatus.GREEN,
            reasoning="Safe. No allergens or health risks detected.",
            details={}
        )
