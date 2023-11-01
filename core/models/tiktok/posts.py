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

    async def get_video(self: "TikTokModel", video_link: str) -> dict:
        ...
