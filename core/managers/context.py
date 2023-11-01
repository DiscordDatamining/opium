from typing import Dict, Optional

from discord import Embed, Guild, Member, Message
from discord.ext.commands import Context as ContextConverter

from core.config import Color
from core.opium import Opium


class Context(ContextConverter):
    bot: "Opium"
    user: Member
    guild: Guild
    message: Message

    async def approve(
        self: "Context",
        description: str,
        *args,
        color: Optional[Color] = None,
        **kwargs,
    ) -> Message:
        """
        Return's an approve embed
        """
        embed: Embed = Embed()
        embed.color = color if color else Color.regular
        if description:
            embed.description = f"> {description}"

        return await self.send(embed=embed, *args, **kwargs)
