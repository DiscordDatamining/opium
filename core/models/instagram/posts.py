import httpx
from pydantic import BaseModel

from core.config import Api


class InstagramModel(BaseModel):
    url: str = Api.url
    headers: dict = Api.headers
    session: httpx.AsyncClient = httpx.AsyncClient()

    async def get_user_story(self: "InstagramModel", username: str) -> None:
        """
        Get's an Instagram user's story
        """
        async with self.session as client:
            r = await client.get(
                headers=self.headers, url=f"{self.url}/ig/user/{username}/stories"
            )
        return r.json()
