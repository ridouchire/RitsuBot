import os
from ritsu_api import *


BOT_HOME = os.path.dirname(__file__) + "/"
DATA_PATH = BOT_HOME + 'db/'
LOG_PATH = BOT_HOME + './'

GOOGLE_KEY = '' #'&key=ABCDEF'

PROXY = {
    'HOST': None,
    'PORT': None,
    'ENABLED': False
}

configuration1 = {
  'jid': '',
  'server': ('ume.mooo.com', 5222), # ('1.2.3.4', 5222)
  'password': '',
  'avatar_hash': '', # sha1 of image
  'log_level': 3, # 1 = error, 2 = warn, 3 = info, 4 = debug
  'echo_log': True,
  'hide_platform': False,
  'info_file': '_magnet2info.txt',
  'error_file': '_magnet2error.txt',
  'unload_plugin_on_error': True,
  'commands_level_overrides': {},
  'commands_pm_only': [],
  'commands_disabled': [],
  'command_prefix': '%',
  'bot_owners': [
    'test@ume.mooo.com',
    'ridouchire@jabber.ru',
    'ritsuka@kokkuri.moe'
  ],
  'nick': 'Balthazar_',
  'db_prefix': '',
  'mucs': {
    'ume@conference.ume.mooo.com': {
      'options': [
        'mock'
        'status',
        'google',
        'ping',
        'seen',
        'timebomb',
      ],
      'commands_level_overrides': {
        'setnick': LEVEL_OWNER,
        'setstatus': LEVEL_OWNER,
      },
      'commands_level_overrides': {},
      'commands_pm_only': ['image', 'users'],
      'commands_disabled': [],
    }
  },
  'plugins': [
    # 'xoma_add',
    'logger',
    'titlelink',
    # 'youtube',
    #'mock',
    'command_beep',
    'command_shell',
    #'user_limits',
    #'command_google',
    'command_ping',
    'command_users',
    'command_admin',
    'command_seen',
    'command_addmod',
    'command_blogs',
    'command_www',
    'command_timebomb',
    #'command_registation',
  ]
}
