#-*- coding: utf-8 -*-
from os import environ
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pyaspeller import YandexSpeller
from re import sub, compile
from gc import collect

class T9Bot(object):
    def __init__(self, blanks : dict):
        self.blanks = blanks
        self.engine = Bot(environ['TOKEN'], parse_mode = types.ParseMode.HTML)
        self.dispatcher = Dispatcher(self.engine)
        self.speller = YandexSpeller()

    def __spelled(self, message : str):
        result = self.blanks['correctly']
        try: corrected = self.speller.spelled(message)
        except: result = self.blanks['error']
        if(message != corrected): result = self.blanks['incorrectly'].format(corrected)
        return result

    def __init_handlers(self):
        @self.dispatcher.message_handler(commands = ['start', 'help'])
        async def process_command(message : types.Message):
            response = self.blanks[message.text.replace('/', '')]
            await self.engine.send_message(message.from_user.id, response)
        @self.dispatcher.message_handler()
        async def process_message(message : types.Message):
            response = self.__spelled(sub(compile('<.*?>') , '', message.text))
            await message.reply(response)

    def run(self):
        self.__init_handlers()
        try: executor.start_polling(self.dispatcher)
        except Exception as error: print(f'Error: {error}')
        finally: (collect(), self.run())
