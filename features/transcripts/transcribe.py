import os

import speech_recognition as sr
from discord.ext.commands import Cog, command, group
from discord import Message
from pydub import AudioSegment
from core.opium import Opium
from os import remove


class Transcribe(Cog):
    """
    Transcribes messages sen't from a discord channel
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
                        await message.channel.send("working on it rq..")
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
                                await message.channel.send(f"```\n{text}```")
                            except sr.UnknownValueError:
                                await message.channel.send(
                                    "Could not understand the audio..."
                                )
                            except sr.RequestError as e:
                                await message.channel.send(
                                    f"Could not request results -> {e}"
                                )

                        remove(file_path)
                        remove(wav_path)
        except Exception as e:
            return await message.channel.send(e)


async def setup(bot: Opium):
    await bot.add_cog(Transcribe(bot))