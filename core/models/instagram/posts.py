from aiohttp import ClientSession
from pydantic import BaseModel

from core.config import Api


class InstagramModel(BaseModel):
    url: str = Api.url
    headers: dict = Api.headers
    session = ClientSession()
