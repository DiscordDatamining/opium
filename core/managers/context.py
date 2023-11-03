from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Mapping,
    Optional,
    Union,
)

from discord import Embed, Guild, Member, Message
from discord.ext.commands import Command
from discord.ext.commands import Context as ContextConverter
from discord.ext.commands import Group, MinimalHelpCommand
from discord.ext.commands.cog import Cog

from core.config import Color
from core.managers.paginator import paginator


class Context(ContextConverter):
    user: Member
    guild: Guild
    message: Message

    async def paginate(
        self: "Context",
        pages: List[Union[Embed, str]],
        timeout: int = 60,
        use_embed: bool = True,
        *args,
        **kwargs,
    ) -> Message:
        """
        Paginates the provided pages
        """
        paginated = paginator(
            self,
            pages=pages,
            timeout=timeout,
            use_embed=use_embed,
        )
        await paginated.start()
        return paginated.message

    async def neutral(
        self: "Context",
        description: Optional[str] = None,
        *args,
        image: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs,
    ) -> Message:
        """
        Neutral embed
        """
        embed: Embed = Embed()
        embed.color = Color.invis if Color.invis else 0x2B2D31

        if description:
            embed.description = f"{description}"
        if title:
            embed.title = title
            if url:
                embed.url = url if url else None
        if image:
            embed.set_image(url=image if image else None)

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


class Help(MinimalHelpCommand):
    context: Context

    def __init__(self: "Help", *args, **options) -> None:
        super().__init__(
            command_attrs={
                "aliases": [
                    "h",
                    "command",
                    "cmd",
                ]
            },
            **options,
        )

    async def send_command_help(
        self, command: Command[Any, Callable[..., Any], Any]
    ) -> None:
        return await self.context.neutral(
            description=(
                f"!{command.name} [command] (parameters)\n"
                f"**Aliases**: *{', '.join(command.aliases)}*\n"
                f"**Parameters**: *{', '.join(command.params)}*\n\n"
                f"*{command.help}*\n\n"
            ),
        )

    async def send_pages(self) -> None:
        return await self.context.paginate(
            pages=[
                Embed(
                    description=pages,
                    color=Color.invis,
                )
                for pages in self.paginator.pages
            ],
        )

    async def command_not_found(self, string: str) -> str:
        return await self.context.deny(
            f"Command `{string}` was not found in my cogs!",
        )

    async def send_error_message(self, error: str) -> None:
        return

    async def send_bot_help(self, mapping: Dict[str, List[str]]) -> None:
        """
        Sends help info
        """
        return await self.context.neutral(
            "Join my discord [here](https://discord.gg/op1um)",
        )
