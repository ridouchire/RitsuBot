# -*-coding:utf-8 -*-

import re
from ritsu_api import *
from ritsu_utils import *
from BeautifulSoup import BeautifulSoup
import urllib2

def info(bot):
  return 'Links parsing plugin 0.0.2'

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
    regexp = r'(?:http[s]?://[\w\d\-.]*\.[\w\d]*[:\d]*[/]?[/&=\$\-\~\.\+\!\?\*\'\(\)\,\%\w]*)'
    link = re.findall(regexp, text)
    
    if link:
      try:
	source = get_link_title(link[0])
      except Exception, e:
	return "Error get_link_title()."
      try:
	res = "%s"%(source)
	bot.send_room_message(target, res)
      except Exception, e:
	return "Other error."

def get_title(rec):
    soup = BeautifulSoup(rec)
    title = soup.html.head.title.string
    return title

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
