# -*- coding:utf-8 -*-
import urllib, urllib2, json, re
from ritsu_utils import *
from ritsu_api import *
from ritsu_config import GOOGLE_KEY

def duckduckgosearch(query, num=0, safe="off"):
    url = 'http://api.duckduckgo.com/?q=%s&format=json&pretty=1&t=no_html&t=no_redirect&t=skip_disambig'%(urllib.quote_plus(query.encode('utf-8')))
    rec = urllib2.urlopen(url)
    js = json.loads(rec.read())
    results = js['RelatedTopics']
    if len(results)>num:
        r = results[num]
        content = r['Result']
        content = content.replace('<b>', '')
        content = content.replace('</b>', '')
        content = unhtml(content)
        title = unhtml(r['Text'])
        return '%s\n%s'%(title, js['AbstractURL'])
    else:
        return 'Nothing found.'

def googlesearch(query, num=0, safe="off"):
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0%s&safe=%s&q=%s'%(
    GOOGLE_KEY,
    safe,
    urllib.quote_plus(query.encode('utf-8'))
  )
  rec = urllib2.urlopen(url)
  js = json.loads(rec.read())
  results = js['responseData']['results']
  if len(results)>num:
    r = results[num]
    #reg = re.compile('<b>([^<]+)</b>', re.IGNORECASE)
    #content = reg.sub('\\1', r['content'])
    content = r['content']
    content = content.replace('<b>', '')
    content = content.replace('</b>', '')
    content = unhtml(content)
    title = unhtml(r['titleNoFormatting'])
    return '%s\n%s\n%s'%(title, content, r['unescapedUrl'])
  else:
    return 'Nothing found.'

def googleimagesearch(query, safe="off"):
  url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0%s&safe=%s&q=%s'%(
    GOOGLE_KEY,
    safe,
    urllib.quote_plus(query.encode('utf-8'))
  )
  rec = urllib2.urlopen(url)
  js = json.loads(rec.read())
  results = js['responseData']['results']
  if len(results)>0:
    return results[0]['unescapedUrl']
  else:
    return 'Nothing found.'

def command_google(bot, room, nick, access_level, parameters, message):
  if not parameters: return 'Query expected.'
  if 'safesearch' in bot.get_config(room, 'options'):
    safe = "active"
  else:
    safe = "off"
  try: res = duckduckgosearch(parameters, 0, safe)
  except: res = 'An error occured.'
  return res

def command_image(bot, room, nick, access_level, parameters, message):
  if not parameters: return 'Query expected.'
  if 'safesearch' in bot.get_config(room, 'options'):
    safe = "active"
  else:
    safe = "off"
  try: res = googleimagesearch(parameters, safe)
  except: res = 'An error occured.'
  return res

LANGCODES = [
  'af','sq','ar','hy','az','eu','be','bn','bg','ca','hr','cs','da',
  'nl','en','et','tl','fi','fr','gl','ka','de','el','gu','ht','iw',
  'hi','hu','is','id','ga','it','ja','kn','ko','la','lv','lt','mk',
  'ms','mt','no','fa','pl','pt','ro','ru','sr','sk','sl','es','sw',
  'sv','ta','te','th','tr','uk','ur','vi','cy','yi','zh-CN','zh-TW'
]

def load(bot):
  global langreg
  bot.add_command('google', command_google, LEVEL_GUEST, 'google')
  bot.add_command('g', command_google, LEVEL_GUEST, 'google')
  bot.add_command(u'п', command_google, LEVEL_GUEST, 'google')
  bot.add_command('image', command_image, LEVEL_GUEST, 'google')
 # bot.add_command('calc', command_calc, LEVEL_GUEST, 'google')
 # bot.add_command('translate', command_translate, LEVEL_GUEST, 'google')
 # bot.add_command('tr', command_translate, LEVEL_GUEST, 'google')
  l = '|'.join(LANGCODES)
  langreg = re.compile('(?:(%s) )?(?:(%s) )?(.+)'%(l, l), re.IGNORECASE | re.DOTALL)

def unload(bot):
  pass

def info(bot):
  return 'Google plugin v1.0.3'
