from typing import List, Optional, Union

from discord import Embed, Guild, Member, Message
from discord.ext.commands import Command
from discord.ext.commands import Context as ContextConverter
from discord.ext.commands import Group, MinimalHelpCommand

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
            embed.description = f"> {description}"
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

    def __init__(self, *args, **options):
        super().__init__(
            command_attrs={
                "aliases": ["h", "cmd", "command"],
            },
            *args,
            **options,
        )

    async def send_bot_help(self, mapping):
        pages: List[Union[Embed, str]] = []

        for cog, commands in mapping.items():
            filtered_commands = await self.filter_commands(commands, sort=True)
            if filtered_commands:
                embed = Embed(title=f"{cog.qualified_name} Commands", color=0x00FF00)
                for command in filtered_commands:
                    embed.add_field(
                        name=command.name, value=command.short_doc, inline=False
                    )
                pages.append(embed)

        if len(pages) == 1:
            await self.context.send(embed=pages[0])
        else:
            p = paginator(self.context, pages)
            await p.start()

    async def send_command_help(self, command: Command):
        embed = Embed(title=command.name, color=Color.invis)
        embed.description = command.help or "*No help command provided*"

        if isinstance(command, Group):
            subcommands = command.commands
            if subcommands:
                embed.add_field(
                    name="Subcommands",
                    value="\n".join([c.name for c in subcommands]),
                )

        await self.context.send(embed=embed)
