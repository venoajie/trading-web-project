
# trading_app/app/clients/librarian.py
import aiohttp
from fastapi import status, HTTPException
from loguru import logger

from app.core.config import settings

class LibrarianClient:
    def __init__(self):
        self.api_url = settings.LIBRARIAN_API_URL
        self.api_key = settings.LIBRARIAN_API_KEY
        # Create a single, reusable session for the lifespan of the application
        # for performance and resource management.
        self._session: aiohttp.ClientSession | None = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self._session

    async def query(self, user_id: str, prompt: str, conversation_history: list | None = None) -> dict:
        """
        Sends a query to the Librarian RAG service.
        """
        session = await self.get_session()
        payload = {
            "prompt": prompt,
            "user_id": user_id,
            "conversation_history": conversation_history or []
        }
        
        try:
            async with session.post(self.api_url, json=payload, timeout=30) as response:
                if response.status == status.HTTP_200_OK:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(
                        f"Librarian service returned error {response.status}: {error_text}"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="The AI service is currently unavailable.",
                    )
        except aiohttp.ClientError as e:
            logger.error(f"Could not connect to Librarian service: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error connecting to the AI service.",
            )

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

# Create a singleton instance to be used across the application
librarian_client = LibrarianClient()

# Add lifespan events to main.py to manage the client's session