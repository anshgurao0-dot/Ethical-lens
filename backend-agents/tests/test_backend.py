import requests
import json
import time
from datetime import datetime

def test_analyze_endpoint():
    url = "http://localhost:8000/analyze"
    
    # Mock User Profile
    user_profile = {
        "user_id": "test_user_1",
        "health_profile": {
            "allergens": ["Peanuts"],
            "conditions": ["Diabetes"],
            "age": 30,
            "dietary_restrictions": ["Low Sugar"]
        },
        "value_profile": {
            "weights": {
                "palm_oil": 1.0,
                "animal_welfare": 0.8
            }
        }
    }
    
    payload = {
        "barcode": "123456789",
        "user_profile": user_profile
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("\nSuccess! Response received:")
            data = response.json()
            print(json.dumps(data, indent=2))
            
            # Basic assertions
            assert data["product_id"] == "123456789"
            assert len(data["agent_verdicts"]) == 5
            print("\nVerdicts:")
            for verdict in data["agent_verdicts"]:
                print(f"- {verdict['agent_name']}: {verdict['status']} (Score: {verdict['score']})")
                print(f"  Reason: {verdict['reasoning']}")
                
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Is it running?")

if __name__ == "__main__":
    # Wait a bit for the server to start if running in automation
    time.sleep(2) 
    test_analyze_endpoint()
