import requests
import json
import time

def test_cosmetic_scan():
    url = "http://localhost:8000/analyze"
    
    # Mock Barcode for L'Oreal Shampoo
    barcode = "3600522606824" 
    
    # User Profile
    user_profile = {
        "user_id": "beauty_user",
        "health_profile": {
            "allergens": [],
            "conditions": [],
            "dietary_restrictions": []
        },
        "value_profile": {
            "weights": {
                "animal_welfare": 1.0 # Cruelty Free check (Future)
            }
        }
    }
    
    payload = {
        "barcode": barcode,
        "user_profile": user_profile
    }
    
    print(f"--- Simulating Cosmetic Scan ---")
    print(f"Product: L'Oreal Elvive Total Repair Shampoo")
    print(f"Sending request...\n")
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"--- Analysis Result ---\n")
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
        print("Could not connect to the server.")

if __name__ == "__main__":
    test_cosmetic_scan()
