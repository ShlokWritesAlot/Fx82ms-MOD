import requests
import json

try:
    print("Testing API Bridge at http://localhost:8001/ask...")
    r = requests.post("http://localhost:8001/ask", json={"prompt": "hi"}, timeout=30)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
