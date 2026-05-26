import httpx
import logging
from config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.TOGETHER_API_KEY
        self.url = "https://api.together.xyz/v1/images/generations"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_image(self, prompt: str, style_prefix: str = "") -> bytes:
        """
        Sends prompt to Together AI API and returns raw image bytes.
        """
        full_prompt = f"{style_prefix} {prompt}".strip() if style_prefix else prompt
        
        payload = {
            "model": settings.DEFAULT_MODEL,
            "prompt": full_prompt,
            "width": 1024,
            "height": 1024,
            "steps": 4, # Fast steps optimized for FLUX.1-schnell
            "n": 1,
            "response_format": "b64_json"
        }

        async with httpx.AsyncClient(timeout=45.0) as client:
            try:
                response = await client.post(self.url, json=payload, headers=self.headers)
                
                if response.status_code == 429:
                    raise Exception("Rate limit reached. Please try again later.")
                
                response.raise_for_status()
                data = response.json()
                
                # Extract Base64 and convert to bytes
                import base64
                image_b64 = data['data'][0]['b64_json']
                return base64.b64decode(image_b64)
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Together AI API Error: {e.response.text}")
                raise Exception("The AI generation service encountered an error.")
            except Exception as e:
                logger.error(f"Unexpected error in AIService: {str(e)}")
                raise Exception("Failed to generate your image due to an internal system error.")
