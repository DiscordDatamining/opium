from typing import Any, Dict, Optional

import httpx
from aiohttp import ClientSession
from pydantic import BaseModel

from core.config import Api


class InstagramModel(BaseModel):
    url: str = Api.url
    headers: dict = Api.headers
    cache: Any

    async def get_user(self: "InstagramModel", username: str) -> None:
        """
        Get information on a instagram user
        """
        cached = self.cache.get(f"instagram_info:{username}")

        if cached:
            return cached

        else:
            async with ClientSession() as cs:
                data = await cs.get(
                    url=f"{self.url}/ig/user/{username}",
                    headers=self.headers,
                )
                self.cache[f"instagram_info:{username}"] = await data.json()
                return await data.json()

    async def get_user_media(
        self: "InstagramModel",
        username: str,
        limit: Optional[int] = 1,
    ) -> None:
        """
        Gets an optional amount of media posts from the user
        """
        async with ClientSession() as cs:
            r = await cs.get(
                url=f"{self.url}/ig/user/{username}/media",
                headers=self.headers,
                params={
                    "amount": limit,
                },
            )
            return await r.json()

    async def get_user_story(
        self: "InstagramModel",
        username: str,
        limit: Optional[int] = 5,
    ) -> Dict:
        """
        Gets a Instagram user story.
        """
        async with ClientSession() as client:
            response = await client.get(
                url=f"{self.url}/ig/user/{username}/stories",
                headers=self.headers,
                params={
                    "amount": limit,
                },
            )
            return await response.json()
