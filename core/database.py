from typing import Dict, List, Optional

from asyncpg import create_pool
from pydantic import BaseModel
from terminut import log

from core.config import Authorization, db


class database:
    lost: log
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
            log.info(f"Attempting to connect to database at {self.host}:{self.port}")

            await create_pool(
                **{
                    "host": db.host,
                    "user": db.user,
                    "port": db.port,
                    "database": db.database,
                    "password": db.password,
                }
            )
            log.success("PostgreSQL database connected successfully.")

        except Exception as e:
            log.fatal(f"Couldn't connect to the database -> {e}")
