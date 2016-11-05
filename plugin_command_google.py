# -*- coding:utf-8 -*-

from ritsu_utils import *
from ritsu_api import *

import requests
import re
import logging as log

log.basicConfig(format="%(levelname)s: %(message)s", level=log.ERROR)

def get_search_page(query, engine='google', custom_query_url=None):
    if not isinstance(query, str):
        raise TypeError('"query" must be "str", not "{}"'.format(
            query.__class__.__name__
        ))
    if len(query) is 0:
        raise ValueError('"query" length must be greater than 0"')

    if custom_query_url:
        url = custom_query_url.format(query)
    if engine is 'google':
        url = "https://www.google.com/search?q={}".format(query)
    elif engine is 'sputnik':
         url = "http://www.sputnik.ru/search?q={}".format(query)
    else:
        raise ValueError('"engine" must be either "google" or "sputnik"')
    if custom_query_url:
        url = custom_query_url.format(query)
    url = requests.utils.requote_uri(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0'
    }
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        log.error('An error has occured while page loading: {}'.format(e))
        return None
    return response.content

def get_links(page, engine):
    result = []
    if engine is 'google':
        link_regex_str = r'<a href="(.*?)"'
        links = [link.split(' ')[0] for link in re.findall(link_regex_str, page)
                 if link.startswith('http')]
        log.debug(links)
        for link in links:
            googlestuff = re.compile(r'.*[.]*google[.]+')
            if not re.match(googlestuff, link) and link not in result:
                result.append(link)            
    elif engine is 'sputnik':
        link_regex_str = r'<div class=\"b-result-title\">.*<a href=\"(.*?)\".*<\/div>'
        result = re.findall(link_regex_str, page)
    else:
        raise ValueError('"engine" must be either "google" or "sputnik"')
    return result

def get_search_function(engine):
    def command_search(bot, room, nick, access_level, parameters, message):
        if nick != bot.ss[engine]['nick']:
            if not parameters:
                return 'Query expected.'    
        else:
            if parameters == bot.ss[engine]['query'] or not parameters:
                if bot.ss[engine]['current'] < len(bot.ss[engine]['links']) - 1:
                    bot.ss[engine]['current'] = bot.ss[engine]['current'] + 1
                    return bot.ss[engine]['links'][bot.ss[engine]['current']]
                else:
                    return "End of search results. Please refine your search query."
        try:
            page = get_search_page(parameters, engine)
        except Exception as e:
            log.error('Query error: {}'.format(e))
            return 'Search error! Please contact your system administrator.'
        links = get_links(page, engine)        
        if links == []:
            return 'Nothing is found!'
        bot.ss[engine]['links'] = links
        bot.ss[engine]['query'] = parameters
        bot.ss[engine]['current'] = 0
        bot.ss[engine]['nick'] = nick

        bot.prevAction = 'search'

        return bot.ss[engine]['links'][bot.ss[engine]['current']]
    return command_search

def load(bot):
    bot.ss = {  # Search State
        'google': {
            'query': None,
            'links': None,
            'current': None,
            'nick': None
        },
        'sputnik': {
            'query': None,
            'links': None,
            'current': None,
            'nick': None
        }
    }
    bot.add_command('google', get_search_function('google'), LEVEL_GUEST, 'google')
    bot.add_command('g', get_search_function('google'), LEVEL_GUEST, 'google')
    bot.add_command(u'п', get_search_function('sputnik'), LEVEL_GUEST, 'rkn')

def unload(bot):
    pass

def info(bot):
    return 'Search plugin v2.0.1'
