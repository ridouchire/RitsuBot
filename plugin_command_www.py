# -*-coding:utf-8 -*-
import urllib, urllib2, re, random, time
from ritsu_utils import *
from ritsu_api import *

def load(bot):
  global langreg
  bot.add_command('whtask', command_whtask, LEVEL_GUEST)
  bot.add_command(u'делать', command_whtask, LEVEL_GUEST)
  bot.add_command('true', command_true, LEVEL_GUEST)
  bot.add_command(u'инфа', command_true, LEVEL_GUEST)
  bot.add_command('d', command_d, LEVEL_GUEST)
  bot.add_command(u'в', command_d, LEVEL_GUEST)
  
def unload(bot):
  pass

def info(bot):
  return 'WWW plugin v1.0.4'

def command_d(bot, room, nick, access_level, parameters, message):
    if not parameters:
        return
    try:
        link = urllib2.urlopen(urllib2.Request("http://isup.me/" + parameters.encode("idna")), timeout = 20)
	downfor = link.read()
	return u"Сайт " + parameters + (u" в дауне." if "It's not just you!" in downfor else u" работает." if "It's just you" in downfor else u" не сайт вообще.")
    except urllib2.URLError:
	return u"Ошибка запроса."

def command_true(bot, room, nick, access_level, parameters, message):
  if parameters:
    procent = str(random.randint(1, 100))
    return u'%s процентов(а) истины.' % (procent)

def command_whtask(bot, room, nick, access_level, parameters, message):
  if parameters:
    listtask = parameters.split(',')
    number = random.randint(1, len(listtask))
    result = listtask[number-1]
    res = u'Тебе нужно: %s' % (result)
    return res
