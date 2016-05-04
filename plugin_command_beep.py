# -*-coding:utf-8 -*-
from ritsu_api import *

def command_beep(bot, room, nick, access_level, parameters, message):
  return u'Xyй.'

def load(bot):
  bot.add_command('beep', command_beep, LEVEL_GUEST)
  bot.add_command('test', command_beep, LEVEL_GUEST)
  pass

def unload(bot):
  pass

def info(bot):
  return 'Beep plugin v1.0'
