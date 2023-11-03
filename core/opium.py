import asyncio
import os
from typing import Any, Dict, Generator, List, Optional

import asyncpg
import redis
from aiohttp import ClientSession, web
from discord import (
    Activity,
    ActivityType,
    AllowedMentions,
    Guild,
    Intents,
    Message,
    Status,
)
from discord.ext.commands import Bot
from discord.ext.commands import Context as DiscordContext
from redis.asyncio import Redis
from terminut import log
from terminut import printf as print

from core.config import Api, Authorization, db
from core.database import database
from core.managers.context import Context, Help


class Opium(Bot):
    def __init__(self: "Opium", *args, **kwargs):
        super().__init__(
            command_prefix=Authorization.prefix,
            help_command=Help(),
            allowed_mentions=AllowedMentions(
                replied_user=False,
                everyone=False,
                users=True,
                roles=False,
            ),
            status=Status.idle,
            intents=Intents.all(),
            owner_ids=Authorization.owner_ids,
            case_insensitive=True,
            *args,
            **kwargs,
        )
        self.run(
            token=Authorization.token,
            log_handler=None,
        )

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=Context)

    async def handle(self, request):
        return web.Response(
            text="Opium",
        )

    def setup_routes(self, app):
        app.router.add_get("/", self.handle)

    async def start_webserver(self):
        app = web.Application()
        self.setup_routes(app)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 8080)
        await site.start()

    async def stop_webserver(self, app):
        await app.cleanup()

    async def setup_hook(self: "Opium") -> None:
        """
        Setup Hook
        """
        self.log = log
        # self.db = await database.connect(self=database())
        self.session = ClientSession()

        self.log.success("Setup hook was executed!")

    async def on_ready(self: "Opium") -> None:
        """
        Client Ready
        """
        await self.load_extension("jishaku")
        await self.start_webserver()
        for root, dirs, files in os.walk("features"):
            for filename in files:
                if filename.endswith(".py"):
                    cog_name = os.path.join(root, filename)[:-3].replace(os.sep, ".")
                    try:
                        await self.load_extension(cog_name)
                        print(
                            "Feature %s has been loaded" % cog_name,
                        )
                    except:
                        pass
