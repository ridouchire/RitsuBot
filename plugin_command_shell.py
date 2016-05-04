from ritsu_api import *
import subprocess
def load(bot):
  bot.add_command('sh', command_sh, LEVEL_OWNER)
  bot.add_command('uptime', command_uptime, LEVEL_GUEST)
  #bot.add_command('mpc', command_mpc, LEVEL_GUEST)
  pass

def unload(bot):
  pass

def info(bot):
  return 'Shell Commands Plugin v0.1'

def command_sh(bot, room, nick, access_level, parameters, message):
    if parameters: buf = parameters
    else: return
    proc = subprocess.Popen("%s" % buf, shell=True, stdout=subprocess.PIPE)
    out = proc.stdout.read()
    return '%s' % (out[:-1])

def command_uptime(bot, room, nick, access_level, parameters, message):
    proc = subprocess.Popen('uptime', shell=True, stdout=subprocess.PIPE)
    out = proc.stdout.read()
    return out[:-1]

def command_mpc(bot, room, nick, access_level, parameters, message):
    proc = subprocess.Popen('mpc', shell=True, stdout=subprocess.PIPE)
    out = proc.stdout.read()
    return out[:-3]
