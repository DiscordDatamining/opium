from typing import Dict

import httpx
from aiohttp import ClientSession
from pydantic import BaseModel

from core.config import Api


class InstagramModel(BaseModel):
    url: str = Api.url
    headers: dict = Api.headers

    async def get_user_story(self, username: str) -> Dict:
        """
        Get an Instagram user's story.
        """
        async with ClientSession() as client:
            response = await client.get(
                url=f"{self.url}/ig/user/{username}/stories",
                headers=self.headers,
            )
            return await response.json()
