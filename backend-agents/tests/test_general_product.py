import asyncio
import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.researcher import ResearcherAgent

async def test_general_product():
    researcher = ResearcherAgent()
    
    # Test Case 1: Sony Headphones (Electronics)
    print("\n--- Testing Sony Headphones (Electronics) ---")
    context_sony = {"barcode": "8806085081111"}
    result_sony = await researcher.analyze(context_sony, {})
    print(f"Result: {result_sony}")
    assert result_sony["product_name"] == "Sony WH-1000XM5 Wireless Headphones"
    assert result_sony["source"] == "GeneralWebSearch"
    assert "Electronics" in result_sony["categories"]

    # Test Case 2: Levi's Jeans (Clothing)
    print("\n--- Testing Levi's Jeans (Clothing) ---")
    context_levis = {"barcode": "5410013123456"}
    result_levis = await researcher.analyze(context_levis, {})
    print(f"Result: {result_levis}")
    assert result_levis["product_name"] == "Levi's 501 Original Fit Jeans"
    assert "Cotton" in result_levis["ingredients"] # Materials mapped to ingredients

    # Test Case 3: Unknown Generic Item
    print("\n--- Testing Generic Unknown Item ---")
    context_generic = {"barcode": "999123456"}
    result_generic = await researcher.analyze(context_generic, {})
    print(f"Result: {result_generic}")
    assert result_generic["product_name"] == "Generic Unknown Gadget"
    assert result_generic["source"] == "GeneralWebSearch"

if __name__ == "__main__":
    asyncio.run(test_general_product())
