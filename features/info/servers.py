from discord.ext.commands import Cog, command, group, Context
from core.opium import Opium
from typing import Optional
from discord import Member, User, Message, Embed
from core.config import Color


class Info(Cog):
    """
    Information
    """

    def __init__(self: "Info", bot: Opium) -> None:
        self.bot: Opium = Opium

    @command(
        name="avatar",
        aliases=[
            "av",
            "pfp",
        ],
    )
    async def avatar(
        self: "Info",
        ctx: Context,
        member: Optional[Member | User] = None,
    ) -> None:
        """
        View someone's profile picture
        """
        member = member or ctx.author
        return await ctx.neutral(
            title="***%s's avatar***" % member.name,
            image=member.display_avatar.url,
            url=member.display_avatar.url,
        )


async def setup(bot: Opium) -> Opium:
    await bot.add_cog(Info(bot))
