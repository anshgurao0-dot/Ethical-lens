import asyncio
import sys
import os

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.researcher import ResearcherAgent

async def test_expanded_db():
    researcher = ResearcherAgent()
    
    # Test Cases
    test_barcodes = {
        "028400090896": "Lay's Classic Potato Chips (Food)",
        "072140811800": "Nivea Creme (Cosmetic)",
        "8806085081111": "Sony Headphones (Electronics)",
        "9999999991234": "Unknown Item (Fallback)"
    }

    print("--- Starting Expanded Database Test ---\n")

    for barcode, description in test_barcodes.items():
        print(f"Testing: {description} [Barcode: {barcode}]")
        
        # Create a mock context
        context = {"user_profile": {"user_id": "test_user"}}
        
        # Run Analysis
        result = await researcher.analyze({"barcode": barcode}, context)
        
        # Print Results
        print(f"  Verdict: {result.status} (Score: {result.score})")
        print(f"  Reasoning: {result.reasoning}")
        
        details = result.details
        print(f"  Product Name: {details.get('product_name')}")
        print(f"  Category: {details.get('category')}")
        print(f"  Source: {details.get('source')}")
        print("-" * 40 + "\n")

if __name__ == "__main__":
    asyncio.run(test_expanded_db())
