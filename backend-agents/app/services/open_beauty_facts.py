import aiohttp
from typing import Optional, Dict, Any

class OpenBeautyFactsClient:
    """
    Client for interacting with the Open Beauty Facts API.
    """
    BASE_URL = "https://world.openbeautyfacts.org/api/v0"

    async def get_product_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """
        Fetches product data from Open Beauty Facts by barcode.
        """
        url = f"{self.BASE_URL}/product/{barcode}.json"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # OBF returns { "status": 1, "product": { ... } } if found
                        # or { "status": 0, "status_verbose": "product not found" }
                        if data and data.get("status") == 1:
                            return data.get("product")
                    return None
        except Exception as e:
            print(f"Error fetching data from Open Beauty Facts: {e}")
            return None
