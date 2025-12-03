import asyncio
from typing import Optional, Dict, Any

class GeneralProductClient:
    """
    A client to fetch general product information.
    In a real implementation, this would use Google Custom Search API or similar.
    For this prototype, it uses a mock database of common non-food/non-cosmetic items.
    """

    def __init__(self):
        self.mock_db = {
            # --- FOOD & BEVERAGE ---
            "028400090896": {
                "product_name": "Lay's Classic Potato Chips",
                "brand": "Lay's",
                "categories": ["Food", "Snacks", "Chips"],
                "description": "Classic salted potato chips.",
                "materials": ["Potatoes", "Vegetable Oil", "Salt"],
                "origin": "USA",
                "image_url": "https://example.com/lays.jpg"
            },
            "028400040112": {
                "product_name": "Doritos Nacho Cheese",
                "brand": "Doritos",
                "categories": ["Food", "Snacks", "Chips"],
                "description": "Nacho cheese flavored tortilla chips.",
                "materials": ["Corn", "Vegetable Oil", "Maltodextrin", "Salt", "Cheddar Cheese", "MSG", "Artificial Color (Red 40, Yellow 5)"],
                "origin": "USA",
                "image_url": "https://example.com/doritos.jpg"
            },
            "044000032029": {
                "product_name": "Oreo Original Cookies",
                "brand": "Nabisco",
                "categories": ["Food", "Snacks", "Cookies"],
                "description": "Chocolate sandwich cookies with cream filling.",
                "materials": ["Sugar", "Unbleached Enriched Flour", "Palm Oil", "Cocoa", "High Fructose Corn Syrup", "Soy Lecithin"],
                "origin": "USA",
                "image_url": "https://example.com/oreos.jpg"
            },
            "013000006408": {
                "product_name": "Heinz Tomato Ketchup",
                "brand": "Heinz",
                "categories": ["Food", "Condiments"],
                "description": "Classic tomato ketchup.",
                "materials": ["Tomato Concentrate", "Distilled Vinegar", "High Fructose Corn Syrup", "Corn Syrup", "Salt", "Spice", "Onion Powder"],
                "origin": "USA",
                "image_url": "https://example.com/heinz.jpg"
            },
            "038000001277": {
                "product_name": "Kellogg's Corn Flakes",
                "brand": "Kellogg's",
                "categories": ["Food", "Breakfast Cereal"],
                "description": "Toasted corn cereal.",
                "materials": ["Milled Corn", "Sugar", "Malt Flavor", "Salt", "Iron", "Vitamin C"],
                "origin": "USA",
                "image_url": "https://example.com/cornflakes.jpg"
            },
            "030000061534": {
                "product_name": "Quaker Oats Old Fashioned",
                "brand": "Quaker",
                "categories": ["Food", "Breakfast", "Grains"],
                "description": "100% Whole Grain Rolled Oats.",
                "materials": ["Whole Grain Rolled Oats"],
                "origin": "USA",
                "image_url": "https://example.com/quaker.jpg"
            },
             "076808516128": {
                "product_name": "Barilla Spaghetti",
                "brand": "Barilla",
                "categories": ["Food", "Pasta"],
                "description": "Dried semolina pasta.",
                "materials": ["Semolina (Wheat)", "Durum Wheat Flour", "Iron", "Vitamin B"],
                "origin": "Italy",
                "image_url": "https://example.com/barilla.jpg"
            },
            "611269991000": {
                "product_name": "Red Bull Energy Drink",
                "brand": "Red Bull",
                "categories": ["Food", "Beverages", "Energy Drink"],
                "description": "Caffeinated energy drink.",
                "materials": ["Carbonated Water", "Sucrose", "Glucose", "Citric Acid", "Taurine", "Sodium Bicarbonate", "Caffeine", "Niacinamide", "Vitamin B6", "Vitamin B12"],
                "origin": "Austria",
                "image_url": "https://example.com/redbull.jpg"
            },

            # --- COSMETICS & PERSONAL CARE ---
            "072140811800": {
                "product_name": "Nivea Creme",
                "brand": "Nivea",
                "categories": ["Beauty", "Skincare", "Moisturizer"],
                "description": "All-purpose moisturizing cream.",
                "materials": ["Aqua", "Paraffinum Liquidum", "Cera Microcristallina", "Glycerin", "Lanolin Alcohol", "Paraffin", "Panthenol", "Magnesium Sulfate"],
                "origin": "Germany",
                "image_url": "https://example.com/nivea.jpg"
            },
            "011111001556": {
                "product_name": "Dove White Beauty Bar",
                "brand": "Dove",
                "categories": ["Beauty", "Personal Care", "Soap"],
                "description": "Moisturizing beauty bar.",
                "materials": ["Sodium Lauroyl Isethionate", "Stearic Acid", "Lauric Acid", "Sodium Tallowate", "Water", "Sodium Isethionate", "Sodium Stearate", "Cocamidopropyl Betaine"],
                "origin": "USA",
                "image_url": "https://example.com/dove.jpg"
            },
             "035000521481": {
                "product_name": "Colgate Total Whitening Toothpaste",
                "brand": "Colgate",
                "categories": ["Beauty", "Oral Care", "Toothpaste"],
                "description": "Whitening toothpaste with fluoride.",
                "materials": ["Stannous Fluoride", "Hydrated Silica", "Water", "Glycerin", "Sorbitol", "Sodium Lauryl Sulfate", "Flavor", "Titanium Dioxide"],
                "origin": "USA",
                "image_url": "https://example.com/colgate.jpg"
            },
            "312547426522": {
                "product_name": "Listerine Cool Mint Mouthwash",
                "brand": "Listerine",
                "categories": ["Beauty", "Oral Care", "Mouthwash"],
                "description": "Antiseptic mouthwash.",
                "materials": ["Water", "Alcohol", "Sorbitol", "Poloxamer 407", "Benzoic Acid", "Sodium Saccharin", "Eucalyptol", "Methyl Salicylate", "Thymol", "Menthol"],
                "origin": "USA",
                "image_url": "https://example.com/listerine.jpg"
            },
            "041554409292": {
                "product_name": "Maybelline Great Lash Mascara",
                "brand": "Maybelline",
                "categories": ["Beauty", "Makeup", "Mascara"],
                "description": "Washable mascara.",
                "materials": ["Water", "Beeswax", "Ozokerite", "Shellac", "Glyceryl Stearate", "Triethanolamine", "Propylene Glycol", "Stearic Acid", "Sorbitan Sesquioleate"],
                "origin": "USA",
                "image_url": "https://example.com/maybelline.jpg"
            },
            "012044037539": {
                "product_name": "Old Spice High Endurance Deodorant",
                "brand": "Old Spice",
                "categories": ["Beauty", "Personal Care", "Deodorant"],
                "description": "Long lasting deodorant stick.",
                "materials": ["Dipropylene Glycol", "Water", "Propylene Glycol", "Sodium Stearate", "Fragrance", "PPG-3 Myristyl Ether", "Tetrasodium EDTA", "Violet 2", "Green 6"],
                "origin": "USA",
                "image_url": "https://example.com/oldspice.jpg"
            },
             "3606000537073": {
                "product_name": "CeraVe Hydrating Facial Cleanser",
                "brand": "CeraVe",
                "categories": ["Beauty", "Skincare", "Cleanser"],
                "description": "Gentle face cleanser with ceramides.",
                "materials": ["Aqua", "Glycerin", "Cetearyl Alcohol", "Phenoxyethanol", "Stearyl Alcohol", "Cetyl Alcohol", "PEG-40 Stearate", "Behentrimonium Methosulfate", "Glyceryl Stearate", "Polysorbate 20"],
                "origin": "France",
                "image_url": "https://example.com/cerave.jpg"
            },

            # --- Electronics (Kept for variety) ---
            "8806085081111": {
                "product_name": "Sony WH-1000XM5 Wireless Headphones",
                "brand": "Sony",
                "categories": ["Electronics", "Audio", "Headphones"],
                "description": "Noise cancelling headphones with industry leading sound.",
                "materials": ["Plastic", "Lithium Ion Battery", "Copper", "Gold"],
                "origin": "Malaysia",
                "image_url": "https://example.com/sony_headphones.jpg"
            },
            "194252000000": {
                "product_name": "Apple iPhone 15 Pro",
                "brand": "Apple",
                "categories": ["Electronics", "Smartphone"],
                "description": "Titanium design, A17 Pro chip.",
                "materials": ["Titanium", "Glass", "Lithium Ion Battery", "Rare Earth Elements"],
                "origin": "China",
                "image_url": "https://example.com/iphone15.jpg"
            },
            
            # --- Clothing (Kept for variety) ---
            "5410013123456": {
                "product_name": "Levi's 501 Original Fit Jeans",
                "brand": "Levi's",
                "categories": ["Clothing", "Denim", "Pants"],
                "description": "Classic straight leg jeans made from cotton.",
                "materials": ["Cotton", "Elastane", "Metal (Rivets)"],
                "origin": "Bangladesh",
                "image_url": "https://example.com/levis_jeans.jpg"
            }
        }

    async def get_product_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """
        Simulates searching the web for a product by barcode.
        """
        print(f"GeneralProductClient: Searching for barcode {barcode}...")
        await asyncio.sleep(1.0) # Simulate network latency

        product = self.mock_db.get(barcode)
        
        if product:
            print(f"GeneralProductClient: Found {product['product_name']}")
            return product
        
        # Universal Fallback for ANY unknown item
        # In a real app, this would be the result of a Google Lens/Search query
        return {
            "product_name": f"Generic Scanned Item ({barcode})",
            "brand": "Unknown Brand",
            "categories": ["General", "Unknown"],
            "description": "Product details could not be verified against the database. Analyzing as a general item.",
            "materials": ["Plastic", "Unknown Materials"], # Assumed worst-case for safety
            "origin": "Unknown",
            "image_url": "https://via.placeholder.com/150"
        }
