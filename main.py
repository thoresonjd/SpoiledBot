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
    '''Spoiled Bot spoiler modes'''

    OFF = 'off'
    SPOIL = 'spoil'
    UNSPOIL = 'unspoil'
    INVERT = 'invert'

class Level(Enum):
    '''Spoiled Bot pain levels'''

    NORMAL = 'normal'
    AGONY = 'agony'

class SpoiledBot(discord.Client):
    '''The Spoiled Bot class'''

    def __init__(self) -> None:
        super().__init__(intents=self.__load_intents())
        self.mode = Mode.UNSPOIL
        self.level = Level.NORMAL

    @staticmethod
    def __load_intents() -> discord.Intents:
        '''Establishes the intents for the Discord bot'''

        intents = discord.Intents().default()
        intents.message_content = True
        return intents

    async def on_ready(self) -> None:
        print('Logged in as {0.user}'.format(self))

    async def on_message(self, message: discord.Message) -> None:
        '''
        Processes a message whenever one is sent
        :param message: A Discord message object
        '''
        
        if self.mode == Mode.OFF or message.author == self.user:
            return
        elif message.channel == self.get_channel(message.channel.id) and message.webhook_id == None:
            webhook = await message.channel.create_webhook(name='delete')
            await message.delete()
            await webhook.send(
                content=self.__execute(message.content),
                username=message.author.display_name,
                avatar_url=message.author.avatar.url
            )
            await webhook.delete()

    def __execute(self, message: str) -> str:
        '''
        Executes the functionality of Spoiled Bot
        :param message: The message to process
        :return: The processed message
        '''
        
        match self.mode:
            case Mode.SPOIL:
                return self.__spoil(message)
            case Mode.UNSPOIL:
                return self.__unspoil(message)
            case Mode.INVERT:
                return self.__invert(message)
            
    @staticmethod
    def __spoil(message: str) -> str:
        '''
        Spoils a message marked as a spoiler
        :param message: The message to spoil
        :returne: The spoiled message
        '''
        
        spoiled = message
        pattern = re.compile(r'\|{2}.*?\|{2}')
        while found := pattern.search(spoiled):
            found = pattern.search(spoiled)
            start, end = found.span()
            section = found.group()[2:-2]
            spoiled = ''.join([spoiled[:start], section, spoiled[end:]])
        return spoiled

    def __unspoil(self, message: str) -> str:
        '''
        Marks a message as a spoiler
        :param message: The message to mark as a spoiler
        :return: The message marked as a spoiler
        '''

        return self.__hide(message.replace('||', ''))
    
    def __hide(self, message: str) -> str:
        '''
        Hides a message depending on the pain level
        :param message: The message to hide
        :return: The hiden message
        '''

        match self.level:
            case Level.NORMAL:
                return self.__hide_message(message)
            case Level.AGONY:
                return self.__hide_each_character(message)
    
    @staticmethod
    def __hide_message(message: str) -> str:
        '''
        Marks an entire message as a spoiler
        :param message: The message in which to hide
        :return: The hidden message
        '''

        return ''.join(['||', message, '||']) if message else ''
    
    @staticmethod
    def __hide_each_character(message: str) -> str:
        '''
        Marks each character in a message as a spoiler
        :param message: The message in which to hide each character
        :return: The message with individually hidden characters
        '''
        
        hidden = ''
        for c in message:
            hidden = ''.join([hidden, '||', c, '||'])
        return hidden
    
    def __invert(self, message: str) -> str:
        '''
        Unveils the hidden content and hides the visible content within a message
        :param message: The message to invert
        :return: The inverted message
        '''
        
        pattern = re.compile(r'\|{2}.*?\|{2}')
        spoiled = [hidden[2:-2] for hidden in pattern.findall(message)]
        marked = [self.__hide(visible) for visible in pattern.split(message)]
        result = [marked[0]]
        for i in range(0, len(spoiled)):
            result.append(spoiled[i])
            result.append(marked[i + 1])
        return ''.join(result)

def main() -> None:
    '''Runs Spoiled Bot'''

    load_dotenv()
    client = SpoiledBot()
    client.run(os.getenv('TOKEN'))

if __name__ == '__main__':
    main()