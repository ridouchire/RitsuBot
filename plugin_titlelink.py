# -*-coding:utf-8 -*-
import re
from ritsu_api import *
from ritsu_utils import *
import urllib2

import logging as log
log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)

def info(bot):
    return 'Links parsing plugin 1.0.0-alpha'

def load(bot):
    pass

def unload(bot):
    pass

def event_room_message(bot, (message, room, nick)):
    if message.getType() == 'groupchat':
        target = room
    else:
        target = room+'/'+nick

    text = message.getBody()
    if text:
        if nick == bot.self_nick[room] and "'s link: " in text:
            return
        regex_str = ur'(?:http[s]?://[\w\d\-.]*\.[\w\d]*[:\d]*[/]?[/\$\-\~\.\+\!\?\*\'\(\)\,\%\w\u0410-\u044f]*)'
        regex = re.compile(regex_str, re.UNICODE)
        link = re.findall(regex, text.decode('utf8'))
        if len(link) > 0:
            try:
	        source = get_link_title(link[0])
            except Exception as e:
                log.error('An error occurred while parsing the title: {}'.format(e.message))
                return                
            try:
                res = "%s"%(source)
                bot.send_room_message(target, res)
            except Exception as e:
                log.error('An error occurred while sending a title parsing result.: {}'.format(e.message))              
	

def get_title(rec):
    title_regex = ur'<title>(.*?)</title>'
    title = re.findall(title_regex, rec)
    if len(title) > 0:
        return title[0]

def get_link_title(link):
  try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0')]
    site = opener.open(link)
  except urllib2.HTTPError, e:
    if e.code == 404:
      return '%s: страница не существует.'%(e.code)
    elif e.code == 403:
      return '%s: страница ограничена к просмотру'%(e.code)
    else:
      return 'Код ошибки %s.'%(e.code)
  if re.search('http://(www\.)?opennet.ru/.*', link):
    rec = site.read().decode("koi8-r")
  else:
    try:
      rec = site.read().decode("utf-8")
    except UnicodeDecodeError:
      rec = site.read().decode("windows-1251")
  site.close
  title = get_title(rec)
  return "%s" % (title)
