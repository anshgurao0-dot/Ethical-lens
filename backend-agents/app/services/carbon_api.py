import asyncio
from typing import Dict, Any, Optional

class CarbonAPIClient:
    """
    Client for fetching Carbon Footprint data.
    Designed to work with APIs like CarbonInterface or Climatiq.
    Currently runs in 'Simulation Mode' without an API key.
    """
    
    def __init__(self, api_key: str = "demo_key"):
        self.api_key = api_key
        self.base_url = "https://www.carboninterface.com/api/v1"
        
        # Realistic CO2 factors (kg CO2e per kg of product)
        self.factors = {
            "beef": 60.0,
            "lamb": 24.0,
            "cheese": 21.0,
            "chocolate": 19.0,
            "coffee": 17.0,
            "pork": 7.0,
            "chicken": 6.0,
            "eggs": 4.5,
            "rice": 4.0,
            "milk": 3.0,
            "oats": 0.9,
            "vegetables": 0.5,
            "plastic": 6.0, # Plastic packaging
            "glass": 0.9,   # Glass packaging
            "aluminum": 2.3 # Aluminum packaging
        }

    async def estimate_footprint(self, product_data: Dict[str, Any]) -> float:
        """
        Estimates the carbon footprint of a product based on its ingredients and packaging.
        Returns values in kg CO2e.
        """
        print(f"CarbonAPIClient: Estimating footprint for {product_data.get('product_name')}...")
        await asyncio.sleep(0.5) # Simulate API latency
        
        total_co2 = 0.0
        
        # 1. Estimate based on Ingredients (simplified weight assumption)
        ingredients = product_data.get("ingredients", [])
        # Assume standard serving size of 100g if weight not provided
        product_weight_kg = 0.1 
        
        for ingredient in ingredients:
            ing_lower = ingredient.lower()
            for key, factor in self.factors.items():
                if key in ing_lower:
                    # Rough estimation: assume main ingredients make up most of the weight
                    # In a real API, we'd send the specific weight of each ingredient
                    total_co2 += factor * (product_weight_kg / len(ingredients))
                    break
        
        # 2. Estimate based on Packaging
        packaging = product_data.get("packaging", "").lower()
        packaging_weight_kg = 0.02 # Assume 20g packaging
        
        if "plastic" in packaging:
            total_co2 += self.factors["plastic"] * packaging_weight_kg
        elif "glass" in packaging:
            total_co2 += self.factors["glass"] * packaging_weight_kg
        elif "can" in packaging or "aluminum" in packaging:
             total_co2 += self.factors["aluminum"] * packaging_weight_kg

        # Base fallback if no matches found (transportation overhead etc.)
        if total_co2 == 0:
            total_co2 = 0.5

        return round(total_co2, 2)
