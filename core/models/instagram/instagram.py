from typing import Dict

import httpx
from aiohttp import ClientSession
from pydantic import BaseModel

from core.config import Api


class InstagramModel(BaseModel):
    url: str = Api.url
    headers: dict = Api.headers

    async def get_user_media(self: "InstagramModel", username: str) -> Dict:
        """
        Gets all media posts from the user
        """
        async with ClientSession() as cs:
            r = await cs.get(
                url=f"{self.url}/ig/user/{username}/media",
                headers=self.headers,
            )
            return await r.json()

    async def get_user_story(self: "InstagramModel", username: str) -> Dict:
        """
        Gets a Instagram user story.
        """
        async with ClientSession() as client:
            response = await client.get(
                url=f"{self.url}/ig/user/{username}/stories",
                headers=self.headers,
            )
            return await response.json()
