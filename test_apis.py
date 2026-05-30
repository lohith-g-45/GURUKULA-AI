
import requests

print("--- Insights API Response ---")
try:
    res = requests.get("http://localhost:8000/api/v1/agent/insights")
    print(f"Status Code: {res.status_code}")
    print(res.json())
except Exception as e:
    print(f"Error: {e}")

print("\n--- Agent Status API Response ---")
try:
    res = requests.get("http://localhost:8000/api/v1/agent/status")
    print(f"Status Code: {res.status_code}")
    print(res.json())
except Exception as e:
    print(f"Error: {e}")

