# -*-coding:utf-8 -*-
import os, sys
sys.path.append(os.path.abspath(os.path.curdir))
from plugin_titlelink import *
from common import *
messages = [
    '',
    'test',
    'https://ru.wikipedia.org/wiki/%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D1%81%D0%BA%D0%B8%D0%B9_%D0%B7%D0%BE%D0%BC%D0%B1%D0%B8',
    "https://www.youtube.com/watch?v=8TX9zpTqZrc",
    'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=58996056',
    """
    https://github.com/ridouchire/RitsuBot
    """,
    """
    https://ru.wikipedia.org/wiki/Философский_зомби
    """,
    """
    http://петушиная-ссылка.рф
    и текст ниже петушиный
    """,
    'http://putin.nash.president.ru',
    ' https://raw.githubusercontent.com/ridouchire/RitsuBot/master/plugin_titlelink.py '
]

bot = Bot(room, nick)

for text in messages:
    message = Message(text)
    event_room_message(bot, (message, room, nick))
