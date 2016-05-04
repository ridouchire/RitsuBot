import urllib2
from ritsu_api import *
from ritsu_utils import *

def event_room_message(bot, (message, room, nick)):
  if message.getType() != 'groupchat': return
  if not 'mock' in bot.get_config(room, 'options'): return
  if nick == bot.self_nick[room]: return

  text = message.getBody()
  if text:
    res = None
    if text == 'O.o':    res = 'o.O'
    elif text == u'О.о': res = u'o.O'
    elif text == u'о.О': res = u'O.o'
    elif text == 'o.O':  res = 'O.o'
    elif text == 'o.o':  res = 'O.O'
    elif text == 'O_o':  res = 'o_O'
    elif text == u'О_о': res = u'о_О'
    elif text == 'o_O':  res = 'O_o'
    elif text == u'О_о': res = u'о_О'
    elif text == u'лол': res = u'ХУЁЛ!'
    elif text == u'Рицка': res = u'Я за него!'
    elif text == u'рицка': res = u'По имени-отчеству, плз.'
    elif text == '...':  res = u'Опять он загружается...'
    elif text == '....': res = u'Что, почти загрузился?'
    elif text == '?':    res = u'\xbf'
    elif text == u'двач': res = u'Хуяч-ебош!'
    elif text == u'Что тут у вас?': res = u'Притон.'
    elif text == u'что тут у вас?': res = u'Заговор.'
    elif text == u'КОЛДУНСТВО': res = u'Пиздунство, блядь.'
    elif text == u'а': res = u'Б.'
    #elif text == 'k':    res = 'You forgot "o".'
    #elif text == 'lol':  res = '/me laughs out loud.'
    if res:
      bot.send_room_message(room, res)

def load(bot):
  pass

def unload(bot):
  pass

def info(bot):
  return 'Mock plugin v1.0'
