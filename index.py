#-*- coding: utf-8 -*-
from core import T9Bot
from json import load

if(__name__ == '__main__'):
    config = {}
    with open('config.json', 'r', encoding = 'utf-8') as string:
        config = load(string)
    T9Bot(config['blanks']).run()
