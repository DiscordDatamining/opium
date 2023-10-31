from httpx import AsyncClient
from pydantic import BaseModel

from core.config import Api


class InstagramModel(BaseModel):
    url: str = Api.url
    headers: dict = Api.headers

    async def get_user_story(self: "InstagramModel", username: str) -> dict:
        """
        Get's an Instagram user's story
        """
        async with AsyncClient() as client:
            response = await client.get(
                url=f"{self.url}/ig/user/{username}/stories",
                headers=self.headers,
            )
            return response.json()
