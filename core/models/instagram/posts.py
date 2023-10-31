from aiohttp import ClientSession
from httpx import get, post
from pydantic import BaseModel

from core.config import Api


class InstagramModel(BaseModel):
    url: str = Api.url
    headers: dict = Api.headers
    session = ClientSession()

    @property
    def get_user_story(self: "InstagramModel", username: str) -> None:
        """
        Get's a instagram user's story
        """
        r = get(
            headers=self.headers,
            url=f"{self.url}/ig/user/%s/stories" % username,
        )
        return r.json()
