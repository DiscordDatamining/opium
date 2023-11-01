import os
from os import remove

import speech_recognition as sr
from discord import Embed, Message
from discord.ext.commands import Cog
from pydub import AudioSegment

from core.config import Color
from core.opium import Opium


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
                                try:
                                    text = recognizer.recognize_google(audio_data)
                                    await message.reply(
                                        embed=Embed(
                                            description=f"> 💤 *{text}*",
                                            color=Color.regular,
                                        ),
                                    )
                                except sr.UnknownValueError:
                                    pass
                                except sr.RequestError as e:
                                    pass

                            remove(file_path)
                            remove(wav_path)
        except Exception as e:
            await message.reply(f"An error occurred: {e}")


async def setup(bot: Opium):
    await bot.add_cog(Transcribe(bot))
