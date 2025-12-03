from typing import Any, Dict
from app.agents.base_agent import BaseAgent
from app.models.product_analysis import AgentVerdict, TrafficLightStatus
from app.services.open_food_facts import OpenFoodFactsClient
from app.services.open_beauty_facts import OpenBeautyFactsClient
from app.services.general_product import GeneralProductClient

class ResearcherAgent(BaseAgent):
    """
    The Researcher: Fetches product data from external APIs (Open Food Facts, Open Beauty Facts, etc.).
    """
    def __init__(self):
        super().__init__(agent_name="Researcher")
        self.off_client = OpenFoodFactsClient()
        self.obf_client = OpenBeautyFactsClient()
        self.general_client = GeneralProductClient()
        
        # Fallback data for demo purposes (if API fails or product missing)
        self.demo_db = {
            "7340083438685": { # Oatly Barista
                "product_name": "Oatly Barista Edition",
                "brands": "Oatly",
                "ingredients_text": "Water, Oats, Rapeseed Oil, Dipotassium Phosphate, Calcium Carbonate, Salt, Vitamins (D2, Riboflavin, B12)",
                "packaging": "Carton",
                "origins": "Sweden",
                "nutriments": {"sugars_100g": 4.0, "salt_100g": 0.1},
                "category": "food"
            },
            "5449000000996": { # Coca Cola
                "product_name": "Coca-Cola Original",
                "brands": "Coca-Cola",
                "ingredients_text": "Carbonated Water, Sugar, Caramel Color, Phosphoric Acid, Natural Flavors, Caffeine",
                "packaging": "Plastic Bottle",
                "origins": "USA",
                "nutriments": {"sugars_100g": 10.6, "salt_100g": 0.0},
                "category": "food"
            },
             "3017620422003": { # Nutella
                "product_name": "Nutella Hazelnut Spread",
                "brands": "Ferrero",
                "ingredients_text": "Sugar, Palm Oil, Hazelnuts, Skim Milk, Cocoa, Lecithin, Vanillin",
                "packaging": "Glass Jar",
                "origins": "Italy",
                "nutriments": {"sugars_100g": 56.3, "salt_100g": 0.1},
                "category": "food"
            },
            "9999999999999": { # The "Bad" Product
                "product_name": "Rainforest Destroyer Snack",
                "brands": "Evil Corp",
                "ingredients_text": "Sugar, Palm Oil, Beef Tallow, Artificial Flavors, Red 40",
                "packaging": "Non-recyclable Plastic Wrapper",
                "origins": "Deforested Zone",
                "nutriments": {"sugars_100g": 50.0, "salt_100g": 2.5}, # High Sugar, High Salt
                "category": "food"
            },
            "3600522606824": { # L'Oreal Shampoo (Mock)
                "product_name": "Elvive Total Repair Shampoo",
                "brands": "L'Oreal",
                "ingredients_text": "Aqua, Sodium Laureth Sulfate, Dimethicone, Coco-Betaine, Sodium Chloride, Sodium Benzoate, Sodium Hydroxide",
                "packaging": "Plastic Bottle",
                "origins": "France",
                "category": "beauty"
            }
        }

    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        barcode = product_data.get("barcode")
        if not barcode:
            return AgentVerdict(
                agent_name=self.agent_name,
                score=0.0,
                status=TrafficLightStatus.YELLOW,
                reasoning="No barcode provided for analysis.",
                details={}
            )

        print(f"[{self.agent_name}] Fetching data for barcode: {barcode}")
        
        # 1. Try Open Food Facts
        product_info = await self.off_client.get_product_by_barcode(barcode)
        source = "Open Food Facts"
        category = "food"

        # 2. Try Open Beauty Facts if not found
        if not product_info:
             print(f"[{self.agent_name}] Not found in OFF, trying Open Beauty Facts...")
             product_info = await self.obf_client.get_product_by_barcode(barcode)
             if product_info:
                 source = "Open Beauty Facts"
                 category = "beauty"

        # 3. Try General Product Search (Universal Fallback)
        if not product_info:
            print(f"[{self.agent_name}] Not found in OBF, trying General Product Search...")
            general_data = await self.general_client.get_product_by_barcode(barcode)
            if general_data:
                product_info = general_data
                source = "General Web Search"
                category = "general"
                # Map general data to expected format
                product_info["ingredients_text"] = ", ".join(general_data.get("materials", []))
                product_info["brands"] = general_data.get("brand")
                product_info["origins"] = general_data.get("origin")

        # 4. Fallback to demo DB if not found
        if not product_info and barcode in self.demo_db:
            print(f"[{self.agent_name}] Using DEMO DATA for barcode: {barcode}")
            product_info = self.demo_db[barcode]
            source = "Demo Database"
            category = product_info.get("category", "unknown")

        if not product_info:
             return AgentVerdict(
                agent_name=self.agent_name,
                score=50.0, # Neutral score for unknown product
                status=TrafficLightStatus.YELLOW,
                reasoning="Product not found in Open Food/Beauty Facts (and no demo data).",
                details={}
            )

        # Extract relevant details
        product_name = product_info.get("product_name", "Unknown")
        brands = product_info.get("brands", "Unknown")
        ingredients_text = product_info.get("ingredients_text", "")
        
        # OFF/OBF returns ingredients as a list of dicts usually, but we might need to parse or use the text
        ingredients_list = [i.get('text') for i in product_info.get('ingredients', [])] if 'ingredients' in product_info else []
        if not ingredients_list and ingredients_text:
            ingredients_list = [i.strip() for i in ingredients_text.split(',')]
        
        # Pass packaging if available (for Circular Guide)
        packaging = product_info.get("packaging", "Unknown")

        return AgentVerdict(
            agent_name=self.agent_name,
            score=100.0, # Researcher is neutral, just provides facts
            status=TrafficLightStatus.GREEN,
            reasoning=f"Data fetched successfully from {source}.",
            details={
                "source": source,
                "category": category,
                "product_name": product_name,
                "brand_owner": brands,
                "ingredients": ingredients_list,
                "packaging": packaging,
                "raw_data": product_info 
            }
        )
