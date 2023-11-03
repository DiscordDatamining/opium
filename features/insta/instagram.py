from discord.ext.commands import Cog, Context, command, group
from core.opium import Opium
from core.models.instagram import InstagramModel
from typing import Optional


class Instagram(Cog):
    """
    Instagram
    """

    def __init__(self: "Instagram", bot: Opium):
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

    @instagram.command()
    async def story(
        self: "Instagram",
        ctx: Context,
        username: str,
        limit: Optional[int] = 3,
    ) -> None:
        """
        Gets multiple stories on an Instagram user
        """
        async with ctx.typing():
            user = await self.InstagramModel.get_user_story(
                username=username,
                limit=limit,
            )
            if not user:
                return await ctx.deny("No stories found on this user!")

            if len(user) == 1:
                return await ctx.send(
                    f"[Download Video]({u['video_url'] if u['video_url'] is not None else u['thumbnail_url']}"
                    for u in user[0]
                )
            else:
                return await ctx.paginate(
                    use_embed=False,
                    pages=[
                        f"[Download Video]({u['video_url'] if u['video_url'] is not None else u['thumbnail_url']})"
                        for u in user
                    ],
                )


async def setup(bot: Opium) -> Opium:
    await bot.add_cog(Instagram(bot))
