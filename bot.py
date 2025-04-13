import discord
import os
from dotenv import load_dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        channel = self.get_channel(int(os.getenv("CHANNEL_ID")))
        await channel.connect()
        await self.change_voice_state(channel=channel, self_mute=True)