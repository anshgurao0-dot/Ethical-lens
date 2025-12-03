import requests
import json
import time

def test_real_product_scan():
    url = "http://localhost:8000/analyze"
    
    # Real Barcode for Oatly Barista Edition
    # This is what the camera would detect
    barcode = "7340083438685" 
    
    # User Profile (same as demo)
    user_profile = {
        "user_id": "demo_user",
        "health_profile": {
            "allergens": ["Peanuts", "Gluten"], # Oatly is usually GF but let's see if it flags anything
            "conditions": [],
            "dietary_restrictions": ["Vegan"]
        },
        "value_profile": {
            "weights": {
                "palm_oil": 1.0,
                "animal_welfare": 0.8,
                "plastic_waste": 0.5
            }
        }
    }
    
    payload = {
        "barcode": barcode,
        "user_profile": user_profile
    }
    
    print(f"--- Simulating Camera Scan ---")
    print(f"Detected Barcode: {barcode}")
    print(f"Sending request to Backend Agents...\n")
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"--- Analysis Result for: {data.get('product_name', 'Unknown')} ---\n")
            print(f"Overall Score: {data['overall_score']}")
            print(f"Overall Status: {data['overall_status']}\n")
            
            print("--- Agent Verdicts ---")
            for verdict in data["agent_verdicts"]:
                print(f"\n[{verdict['agent_name']}]")
                print(f"Status: {verdict['status']}")
                print(f"Reasoning: {verdict['reasoning']}")
                if verdict['details']:
                    print(f"Details: {json.dumps(verdict['details'], indent=2)}")
                
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Please ensure 'python -m app.main' is running.")

if __name__ == "__main__":
    test_real_product_scan()
