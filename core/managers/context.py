from typing import Dict, Optional

from discord import Embed, Guild, Member, Message
from discord.ext.commands import Context as ContextConverter

from core.config import Color


class Context(ContextConverter):
    user: Member
    guild: Guild
    message: Message

    async def neutral(
        self: "Context",
        description: Optional[str] = None,
        *args,
        image: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs,
    ) -> Message:
        """
        Neutral embed
        """
        embed: Embed = Embed()
        embed.color = Color.invis if Color.invis else 0x2B2D31
        if description:
            embed.description = f"> {description}"
        if title:
            embed.title = title
        if image:
            embed.image(url=image if image else None)
        return await self.send(embed=embed, *args, **kwargs)

    async def deny(
        self: "Context",
        description: str,
        *args,
        **kwargs,
    ) -> Message:
        """
        Return's an deny embed
        """
        embed: Embed = Embed()
        embed.color = Color.deny if Color.deny else 0xF23F43
        if description:
            embed.description = f"> {description}"

        return await self.send(embed=embed, *args, **kwargs)

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
