from discord.ext.commands import Cog, Context, command, group
from core.opium import Opium
from core.models.instagram import InstagramModel


class Instagram(Cog):
    """
    Instagram
    """

    def __init__(
        self: "Instagram",
        bot: Opium,
    ):
        self.bot: Opium = bot
        self.InstagramModel = InstagramModel(
            cache=self.bot.cache,
        )

    @group(
        name="instagram",
        aliases=[
            "ig",
            "insta",
        ],
        invoke_without_command=True,
    )
    async def instagram(
        self: "Instagram",
        ctx: Context,
        username: str,
    ):
        """
        Gets information on a instagram user
        """
        user = await self.InstagramModel.get_user(username=username)
        if not user:
            return await ctx.deny(
                "That user wasn't found on instagram.",
            )
        async with ctx.typing():
            return await ctx.neutral(
                description=user["biography"],
                thumbnail=user["profile_pic_url_hd"],
                authoricon=ctx.author.display_avatar.url,
                fields=[
                    ("Followers", f'{user["follower_count"]:,}', True),
                    ("Following", f'{user["following_count"]:,}', True),
                    ("Media", f'{user["media_count"]:,}', True),
                ],
                author=f"{user['full_name'] or ''} ({username})",
            )


async def setup(bot: Opium) -> Opium:
    await bot.add_cog(Instagram(bot))
