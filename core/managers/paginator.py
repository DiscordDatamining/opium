from typing import List, Optional, Union

from discord import Embed, Member, Message, Reaction, User
from discord.ext import commands


class paginator:
    def __init__(
        self,
        ctx: commands.Context,
        pages: List[Union[Embed, str]],
        timeout: int = 60,
        use_embed: bool = True,
    ) -> None:
        self.ctx: commands.Context = ctx
        self.pages: List[Union[Embed, str]] = pages
        self.timeout: int = timeout
        self.current_page: int = 0
        self.use_embed: bool = use_embed
        self.reactions: List[str] = [
            "⬅️",
            "➡️",
            "⏪",
            "⏩",
            "⏸",
        ]
        self.message: Optional[Message] = None
        self.bot = ctx.bot

    async def start(self) -> None:
        if self.use_embed:
            self.message = await self.ctx.send(
                embed=self.pages[self.current_page],
            )
        else:
            self.message = await self.ctx.send(
                self.pages[self.current_page],
            )

        for reaction in self.reactions:
            await self.message.add_reaction(reaction)

        self.bot.loop.create_task(self.check_reactions())

    async def check_reactions(self) -> None:
        def check(reaction: Reaction, user: Union[User, Member]) -> bool:
            return (
                user == self.ctx.author
                and reaction.message.id == self.message.id
                and str(reaction.emoji) in self.reactions
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=self.timeout, check=check
                )

                if (
                    str(reaction.emoji) == "➡️"
                    and self.current_page < len(self.pages) - 1
                ):
                    self.current_page += 1

                elif str(reaction.emoji) == "⬅️" and self.current_page > 0:
                    self.current_page -= 1

                elif str(reaction.emoji) == "⏩":
                    self.current_page = len(self.pages) - 1

                elif str(reaction.emoji) == "⏪":
                    self.current_page = 0

                elif str(reaction.emoji) == "⏸":
                    await self.message.delete()
                    return

                await self.message.remove_reaction(reaction, user)

                if self.use_embed:
                    await self.message.edit(
                        embed=self.pages[self.current_page],
                    )
                else:
                    await self.message.edit(
                        content=self.pages[self.current_page],
                    )

            except TimeoutError:
                for reaction in self.reactions:
                    await self.message.remove_reaction(
                        reaction,
                        self.ctx.me,
                    )
                break
