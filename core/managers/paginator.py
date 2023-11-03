from typing import List, Optional, Union

from discord import Embed, Member, Message, Reaction, User
from discord.ext.commands import Context


class paginator:
    def __init__(
        self,
        ctx: Context,
        pages: List[Union[Embed, str]],
        timeout: int = 60,
        use_embed: bool = True,
    ) -> None:
        self.ctx: Context = ctx
        self.pages: List[Union[Embed, str]] = pages
        self.timeout: int = timeout
        self.current_page: int = 0
        self.use_embed: bool = use_embed
        self.reactions: List[str] = ["⬅️", "🚮", "➡️", "🔢"]
        self.message: Optional[Message] = None
        self.bot = ctx.bot

    def _set_footer(
        self,
        page_content: Union[Embed, str],
    ) -> Union[Embed, str]:
        if isinstance(page_content, Embed):
            page_content.set_footer(
                text=f"Page {self.current_page + 1} of {len(self.pages)}"
            )
        else:
            page_content += f"\n\nPage {self.current_page + 1} of {len(self.pages)}"

        return page_content

    async def start(self) -> None:
        content_with_footer = self._set_footer(
            self.pages[self.current_page],
        )
        if self.use_embed:
            self.message = await self.ctx.send(embed=content_with_footer)
        else:
            self.message = await self.ctx.send(content_with_footer)

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

                elif str(reaction.emoji) == "🔢":
                    response_message = await self.ctx.neutral(
                        description="Which page would you like to go to?"
                    )

                    def check_msg(m):
                        return m.author == self.ctx.author and m.content.isdigit()

                    try:
                        msg = await self.bot.wait_for(
                            "message", check=check_msg, timeout=self.timeout
                        )
                        page_num = int(msg.content) - 1
                        if 0 <= page_num < len(self.pages):
                            self.current_page = page_num
                        await msg.delete()
                        await response_message.delete()
                    except Exception as e:
                        pass

                elif str(reaction.emoji) == "🚮":
                    await self.message.delete()
                    return

                await self.message.remove_reaction(reaction, user)

                content_with_footer = self._set_footer(self.pages[self.current_page])
                if self.use_embed:
                    await self.message.edit(embed=content_with_footer)
                else:
                    await self.message.edit(content=content_with_footer)

            except TimeoutError:
                for reaction in self.reactions:
                    await self.message.remove_reaction(
                        reaction,
                        self.ctx.me,
                    )
                break
