# -*- coding:utf-8 -*-

from ritsu_utils import *
from ritsu_api import *

import requests
import re
import logging as log

log.basicConfig(format="%(levelname)s: %(message)s", level=log.ERROR)

def get_search_page(query, engine):
    if not isinstance(query, str):
        raise TypeError('"query" must be "str", not "{}"'.format(
            query.__class__.__name__
        ))
    if len(query) is 0:
        raise ValueError('"query" length must be greater than 0"')

    if engine is 'google':
        url = requests.utils.requote_uri("https://www.google.com/search?q=" +
                                         query +
                                         "&ie=utf-8&oe=utf-8")
    elif engine is 'sputnik':
         url = requests.utils.requote_uri("http://www.sputnik.ru/search?q=" + query)
    else:
        raise ValueError('"engine" must be either "google" or "sputnik"')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0'
    }
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        log.error('An error has occured while page loading: {}'.format(e))
        return None
    return response

def get_links(query, engine):
    try:
        page = get_search_page(query, engine)
    except Exception as e:
        log.error('Query error: {}'.format(e))
        page =  None
    if page is None: return None

    result = []
    if engine is 'google':
        link_regex_str = r'<a href="(.*?)"'
        links = [link.split(' ')[0] for link in re.findall(link_regex_str, page.content)
                 if link.startswith('http')]
        log.debug(links)
        for link in links:
            googlestuff = re.compile(r'.*[.]*google[.]+')
            if not re.match(googlestuff, link) and link not in result:
                result.append(link)            
    elif engine is 'sputnik':
        link_regex_str = r'<div class=\"b-result-title\">.*<a href=\"(.*?)\".*<\/div>'
        result = re.findall(link_regex_str, page.content)
    else:
        raise ValueError('"engine" must be either "google" or "sputnik"')
    return result

def get_search_function(engine):
    def command_search(bot, room, nick, access_level, parameters, message):
        if nick != bot.gss['nick']:
            if not parameters:
                return 'Query expected.'    
        else:
            if parameters == bot.gss['query'] or not parameters:
                if bot.gss['current'] < len(bot.gss['links']) - 1:            
                    bot.gss['current'] = bot.gss['current'] + 1
                    return bot.gss['links'][bot.gss['current']]
                else:
                    return "End of search results. Please refine your search query."
        links = get_link(parameters, engine)
        if links is None:
            return 'Search error! Please contact your system administrator.'
        if links is []:
            return 'Nothing is found!'
        bot.gss['links'] = links
        bot.gss['query'] = parameters
        bot.gss['current'] = 0
        bot.gss['nick'] = nick

        bot.prevAction = 'search'

        return bot.gss['links'][bot.gss['current']]
    return command_search

def load(bot):
  bot.gss = {  # Google Search State
      'query': None,
      'links': None,
      'current': None,
      'nick': None
  }
  bot.add_command('google', get_search_function('google'), LEVEL_GUEST, 'google')
  bot.add_command('g', get_search_function('google'), LEVEL_GUEST, 'google')
  bot.add_command(u'п', get_search_function('sputnik'), LEVEL_GUEST, 'rkn')

def unload(bot):
  pass

def info(bot):
  return 'Search plugin v2.0.0-alpha'
