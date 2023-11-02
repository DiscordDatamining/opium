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
            if cog is None:
                continue

            filtered_commands = await self.filter_commands(commands, sort=True)
            if filtered_commands:
                embed = Embed(
                    title=f"{cog.qualified_name}",
                    color=Color.invis,
                )

            for command in filtered_commands:
                has_subcommands = "*" if isinstance(command, Group) else ""
                aliases = "|".join(command.aliases)
                aliases_str = f"[{aliases}]" if aliases else ""
                command_info = f"\n{has_subcommands}{command.name} {aliases_str} - {command.short_doc}"

                if embed.description:
                    embed.description += command_info
                else:
                    embed.description = command_info

                pages.append(embed)

        p = paginator(self.context, pages)
        await p.start()

    async def send_command_help(self, command: Command):
        """
        Send the embed for help on a command.
        """
        embed = Embed(color=Color.invis)

        embed.description = (
            f"`{self.context.prefix}{command.name} {command.signature}`\n"
        )

        if command.aliases:
            embed.description += f"***Aliases:*** {', '.join(command.aliases)}"

        embed.description += (
            f"\n\n{f'*{command.help}*' or '*No detailed description available.*'}"
        )

        return await self.context.send(embed=embed)
