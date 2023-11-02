from typing import Dict, List, Optional

from asyncpg import create_pool
from pydantic import BaseModel

from core.config import Authorization, db


class database(BaseModel):
    host: str = db.host
    user: str = db.user
    port: int = db.port
    database: str = db.database
    password: str = db.password

    async def connect(self: "database") -> None:
        """
        Connects to the database
        """
        try:
            await create_pool(
                f"postgres://{self.user}:{self.password}@{self.host}/{self.database}"
            )
        except Exception as e:
            pass
