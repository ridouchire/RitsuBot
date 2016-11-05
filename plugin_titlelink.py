# -*-coding:utf-8 -*-
import re
from ritsu_api import *
from ritsu_utils import *
from ritsu_config import PROXY

import urllib2
import logging as log
log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)

def info(bot):
    return 'Links parsing plugin 1.1.0'

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
        if nick == bot.self_nick[room] and hasattr(bot, 'prevAction') and \
        bot.prevAction is 'title':
            return
        regex_str = ur'(?:http[s]?://[\w\d\-.]*\.[\w\d]*[:\d]*[/]?[/\$\-\~\.\+\=\&\!\?\*\'\(\)\,\%\w\u0410-\u044f]*)'
        regex = re.compile(regex_str, re.UNICODE)
        try:            
            link = re.findall(regex, text.decode('utf8'))
        except UnicodeEncodeError as e:
            link =  re.findall(regex, text)
        if len(link) > 0:
            try:
	        source = get_link_title(link[0].encode('utf8'))
            except Exception as e:
                log.error('An error occurred while parsing the title: {}'.format(e))
                return                
            try:
                res = source.encode('utf8')
                bot.prevAction = 'title'
                bot.send_room_message(target, res)
            except Exception as e:
                log.error('An error occurred while sending a title parsing result.: {}'.format(e))              
	

def get_title(rec):
    title_regex = ur'<title>(.*?)</title>'
    title = re.findall(title_regex, rec)
    if len(title) > 0:
        return title[0]
    else:
        return None

def get_link_title(link):
  if PROXY['ENABLED']:
    opener = urllib2.build_opener(
      urllib2.ProxyHandler({
        'http': '{}:{}'.format(PROXY['HOST'], PROXY['PORT']),
        'http': '{}:{}'.format(PROXY['HOST'], PROXY['PORT'])
      })
    )
  else:
    opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0')]
  try:
    site = opener.open(link)
  except urllib2.HTTPError, e:
    if e.code == 404:
      return '%s: страница не существует.'%(e.code)
    elif e.code == 403:
      return '%s: страница ограничена к просмотру'%(e.code)
    else:
      return 'Код ошибки %s.'%(e.code)
  except urllib2.URLError, e:
      return 'This URL could not be resolved.'.decode('utf8')
  if re.search('http://(www\.)?opennet.ru/.*', link):
    rec = site.read().decode("koi8-r")
  else:
    try:
      rec = site.read().decode("utf-8")
    except UnicodeDecodeError:
      rec = site.read().decode("windows-1251")
  title = get_title(rec)
  if title is None:
      title = site.headers.gettype()
  site.close()
  return "%s" % (title)
