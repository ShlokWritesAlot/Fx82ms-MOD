import requests
import time

class AIClient:
    """Synchronous client to interact with the local FastAPI bridge (designed for threading)."""
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.last_latency = 0

    def ask(self, prompt: str):
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/ask", 
                json={"prompt": prompt}, 
                timeout=60.0
            )
            self.last_latency = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                return {"success": True, "answer": response.json().get("answer", "")}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            self.last_latency = int((time.time() - start_time) * 1000)
            return {"success": False, "error": str(e)}
