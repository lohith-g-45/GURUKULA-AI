
import requests
import json

# Test the optimized planner endpoint
url = "http://localhost:8000/api/v1/agent/planner"

payload = {
    "readiness_score": 60,
    "available_hours_per_day": 6,
    "weak_subjects": ["History", "Geography"],
    "exam": "KAS",
    "refresh": True
}

print("=" * 80)
print("Testing Optimized Planner Endpoint")
print("=" * 80)
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\n" + "=" * 80)

try:
    response = requests.post(url, json=payload, timeout=60)
    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nSuccess! Planner Response:")
        print(json.dumps(result, indent=2))
        print("\n" + "=" * 80)
        print("[SUCCESS] Planner endpoint returned 200!")
        print("=" * 80)
    else:
        print("\nError! Response:")
        print(response.text)
        print("\n" + "=" * 80)
        print("[FAILURE] Planner endpoint failed!")
        print("=" * 80)
except Exception as e:
    print(f"Exception: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 80)
    print("[FAILURE] Exception occurred!")
    print("=" * 80)

