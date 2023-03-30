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
import re

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

    def execute(self, message: str) -> str:
        match self.mode:
            case Mode.OFF:
                return message
            case Mode.SPOIL:
                return self.spoil(message)
            case Mode.UNSPOIL:
                return self.unspoil(message)
            case Mode.INVERT:
                return self.invert(message)
            
    @staticmethod
    def spoil(message: str) -> str:
        spoiled = message
        pattern = re.compile(r'\|{2}.*?\|{2}')
        while found := pattern.search(spoiled):
            found = pattern.search(spoiled)
            start, end = found.span()
            section = found.group()[2:-2]
            spoiled = ''.join([spoiled[:start], section, spoiled[end:]])
        return spoiled

    def unspoil(self, msg):
        return self.hide(msg.replace('||', ''))
    
    def hide(self, msg):
        match self.level:
            case Level.NORMAL:
                return self.hide_message(msg)
            case Level.AGONY:
                return self.hide_each_character(msg)
    
    @staticmethod
    def hide_message(message: str) -> str:
        return ''.join(['||', message, '||']) if message else ''
    
    @staticmethod
    def hide_each_character(message: str) -> str:
        hidden = ''
        for c in message:
            hidden = ''.join([hidden, '||', c, '||'])
        return hidden

    def invert(message):
        pass

def main() -> None:
    load_dotenv()
    client = SpoiledBot()
    client.run(os.getenv('TOKEN'))

if __name__ == '__main__':
    main()