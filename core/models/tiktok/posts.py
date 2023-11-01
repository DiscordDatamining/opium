from typing import Dict

import httpx
from aiohttp import ClientSession
from pydantic import BaseModel

from core.config import Api


class TikTokModel(BaseModel):
    """
    Tiktok model
    """

    headers: dict = Api.headers
    url: str = Api.url

    async def random_video(self: "TikTokModel") -> None:
        """
        Get's a random tiktok video
        """
        async with ClientSession() as cs:
            async with cs.get(
                url=f"{self.url}/tiktok/videos",
                headers=self.headers,
            ) as r:
                return await r.json()

    async def get_video(self: "TikTokModel", video_link: str = None) -> dict:
        """
        Get's a tiktok video
        """
        async with ClientSession() as cs:
            async with cs.get(
                url=f"{self.url}/tiktok/{video_link if video_link else ''}",
                headers=self.headers,
            ) as r:
                return await r.json()
