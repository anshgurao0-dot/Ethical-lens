import requests
import json
import time

def test_bad_product_scan():
    url = "http://localhost:8000/analyze"
    
    # Mock Barcode for "Rainforest Destroyer Snack"
    barcode = "9999999999999" 
    
    # User Profile (Diabetic, Hypertensive, Eco-Conscious)
    user_profile = {
        "user_id": "test_user",
        "health_profile": {
            "allergens": [],
            "conditions": ["Diabetes", "Hypertension"], # Should trigger Bio-Shield
            "dietary_restrictions": []
        },
        "value_profile": {
            "weights": {
                "palm_oil": 1.0, # Critical
                "animal_welfare": 0.8
            }
        }
    }
    
    payload = {
        "barcode": barcode,
        "user_profile": user_profile
    }
    
    print(f"--- Simulating 'Bad Product' Scan ---")
    print(f"Product: Rainforest Destroyer Snack")
    print(f"User Conditions: Diabetes, Hypertension")
    print(f"User Values: Anti-Palm Oil")
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
                    # Print details nicely, especially for Activist actions
                    if "actions" in verdict['details']:
                         print("Actions:")
                         for action in verdict['details']['actions']:
                             print(f" - {action['type']}: {action['content']}")
                    else:
                         print(f"Details: {json.dumps(verdict['details'], indent=2)}")
                
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")

if __name__ == "__main__":
    test_bad_product_scan()
