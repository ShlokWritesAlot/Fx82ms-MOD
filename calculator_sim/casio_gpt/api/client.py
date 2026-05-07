import httpx
import asyncio
from ..config import settings

class APIClient:
    """Handles communication with the FastAPI bridge."""
    
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.endpoint = settings.ASK_ENDPOINT
        self.timeout = settings.TIMEOUT_SECONDS

    async def ask_ai(self, prompt: str):
        """Sends a prompt to the bridge and returns the answer."""
        url = f"{self.base_url}{self.endpoint}"
        payload = {"prompt": prompt}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                return {"success": True, "answer": data.get("answer", "No response.")}
        except httpx.ConnectError:
            return {"success": False, "error": "Bridge Offline"}
        except httpx.TimeoutException:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
