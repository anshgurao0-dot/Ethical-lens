import aiohttp
from typing import Optional, Dict, Any

class OpenFoodFactsClient:
    """
    Client for interacting with the Open Food Facts API.
    """
    BASE_URL = "https://world.openfoodfacts.org/api/v0"

    def __init__(self):
        pass

    async def get_product_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """
        Fetches product data by barcode.
        """
        url = f"{self.BASE_URL}/product/{barcode}.json"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == 1:
                            return data.get("product")
                        else:
                            print(f"Product not found for barcode: {barcode}")
                            return None
                    else:
                        print(f"Error fetching data: {response.status}")
                        return None
        except Exception as e:
            print(f"Exception during API call: {e}")
            return None
