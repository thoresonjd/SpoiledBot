'''
SpoiledBot
File: main.py
Author: Justin Thoreson
Version: 1.0
'''

from dotenv import load_dotenv
from enum import Enum
import discord
import os

class Mode(Enum):
    OFF = 'off'
    SPOIL = 'spoil'
    UNSPOIL = 'unspoil'
    INVERT = 'invert'

class Level(Enum):
    NORMAL = 'normal'
    AGONY = 'agony'

class SpoiledBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=self.__load_intents())
        self.mode = Mode.INVERT
        self.level = Level.AGONY

    @staticmethod
    def __load_intents() -> discord.Intents:
        intents = discord.Intents().default()
        intents.message_content = True
        return intents

    async def on_ready(self) -> None:
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message: discord.Message) -> None:
        print(message.content)
        if message.author == self.user:
            return
        if message.content == '$test':
            await message.channel.send('Hello! I am a bot!')

def main() -> None:
    load_dotenv()
    client = SpoiledBot()
    client.run(os.getenv('TOKEN'))

if __name__ == '__main__':
    main()