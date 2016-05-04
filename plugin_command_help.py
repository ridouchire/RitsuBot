from ritsu_api import *
def load(bot):
  bot.add_command('help', command_help, LEVEL_GUEST)
  pass

def unload(bot):
  pass

def info(bot):
  return 'Help Commands Plugin v0.1'

def command_help(bot, room, nick, access_level, parameters, message):
  return '''
beep - beep(analog of the test command)
users -  users online in this conference(private)
ping - ping
google -  search Google
image - search images(Google)
devoice -  to deprive of the participant of a voice
voice - to return a voice
kick - to expel the participant
member - to make the participant the membery
delmember - to make the participant
seen - tracking the participant
sourse - version of the bot
setnick - set nick of the bot
setstatus - set status of the bot
iii - IIIypuk's song
g - search Google
sh - run command shell on server
akick - auto kick the participant
ban - ban participant
'''
