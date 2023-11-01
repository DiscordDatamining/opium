import os
from os import remove

import discord
import speech_recognition as sr
from discord import Embed, Forbidden, HTTPException, Message
from discord.ext.commands import Cog
from pydub import AudioSegment

from core.config import Color
from core.opium import Opium
import uuid


class Transcribe(Cog):
    """
    Transcribes messages sent from a discord channel
    """

    def __init__(self: "Transcribe", bot: Opium):
        self.bot: Opium = bot

    @Cog.listener("on_message")
    async def transcribe(self: "Transcribe", message: Message) -> None:
        if message.author == self.bot.user:
            return

        try:
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.endswith(".ogg"):
                        async with message.channel.typing():
                            file_path = f"./{attachment.filename}"
                            await attachment.save(file_path)

                            audio = AudioSegment.from_ogg(file_path)
                            wav_path = file_path.replace(".ogg", ".wav")
                            audio.export(wav_path, format="wav")

                            recognizer = sr.Recognizer()
                            with sr.AudioFile(wav_path) as source:
                                audio_data = recognizer.record(source)
                                text = recognizer.recognize_google(audio_data)

                                permissions = message.author.guild_permissions

                                if "opium create a text Channel called" in text:
                                    if permissions.manage_channels:
                                        name = text.replace(
                                            "opium create a text Channel called",
                                            "",
                                        ).strip()
                                        await self.create_channel(message, name)
                                    else:
                                        await message.reply(
                                            "> *You don't have permission to create channels.*"
                                        )
                                elif "opium delete the channel called" in text:
                                    if permissions.manage_channels:
                                        channel_name = text.replace(
                                            "opium delete the channel called",
                                            "",
                                        ).strip()
                                        await self.delete_channel(message, channel_name)
                                    else:
                                        await message.reply(
                                            "> *You don't have permission to delete channels.*"
                                        )

                                elif "opium create a role called" in text:
                                    if permissions.manage_roles:
                                        role_name = text.replace(
                                            "opium create a role called",
                                            "",
                                        ).strip()
                                        await self.create_role(message, role_name)
                                    else:
                                        await message.reply(
                                            "> *You don't have permission to create roles.*"
                                        )

                                elif "opium delete the role called" in text:
                                    if permissions.manage_roles:
                                        role_name = text.replace(
                                            "opium delete the role called",
                                            "",
                                        ).strip()
                                        await self.delete_role(message, role_name)
                                    else:
                                        await message.reply(
                                            "> *You don't have permission to delete roles.*"
                                        )

                                remove(file_path)
                                remove(wav_path)

        except Exception as e:
            return self.bot.log.error(e)

    async def create_channel(self, message, name):
        try:
            await message.guild.create_text_channel(name=name)
            await message.reply(
                f"> *I have created a text channel called* ***{name}***"
            )
        except Forbidden:
            await message.reply("> *I don't have permission to create channels.*")
        except HTTPException:
            await message.reply("> *Failed to create the channel.*")

    async def delete_channel(self, message, channel_name):
        channel = discord.utils.get(message.guild.channels, name=channel_name)
        if channel:
            try:
                await channel.delete()
                await message.reply(f"> *Channel {channel_name} deleted successfully.*")
            except Forbidden:
                await message.reply("> *I don't have permission to delete channels.*")
            except HTTPException:
                await message.reply("> *Failed to delete the channel.*")
        else:
            await message.reply(f"> *Channel {channel_name} not found.*")

    async def create_role(self, message, role_name):
        try:
            await message.guild.create_role(name=role_name)
            await message.reply(f"> *Role {role_name} created successfully.*")
        except Forbidden:
            await message.reply("> *I don't have permission to create roles.*")
        except HTTPException:
            await message.reply("> *Failed to create the role.*")

    async def delete_role(self, message, role_name):
        role = discord.utils.get(message.guild.roles, name=role_name)
        if role:
            try:
                await role.delete()
                await message.reply(f"> *Role {role_name} deleted successfully.*")
            except Forbidden:
                await message.reply("> *I don't have permission to delete roles.*")
            except HTTPException:
                await message.reply("> *Failed to delete the role.*")
        else:
            await message.reply(f"> *Role {role_name} not found.*")


async def setup(bot: Opium):
    await bot.add_cog(Transcribe(bot))
