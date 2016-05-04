import urllib2
from ritsu_api import *
from ritsu_utils import *

def getyoutubeinfo(yid):
  try:
    site = urllib2.urlopen('http://gdata.youtube.com/feeds/api/videos/'+yid)
  except urllib2.HTTPError, e:
    if e.code == 404:
      return 'The video is not available or is being processed.'
    elif e.code == 400:
      return 'Malformed video ID.'
    else:
      return 'Error %s.'%(e.code)

  rec = site.read().decode("utf-8")
  #writelog('_debug-youtube.txt', rec)
  site.close()
  p = rec.find("<title type='text'>")
  p2 = rec.find("</title>", p+19)
  title = unhtml(rec[p+19:p2])

  p = rec.find("<author><name>", p2)
  author = '???'
  if p != -1:
    p2 = rec.find('<', p+14)
    author = rec[p+14:p2]

  p = rec.find("<yt:duration seconds='", p2)
  min = 0
  sec = 0
  if p != -1:
    p2 = rec.find("'", p+22)
    sec = int(rec[p+22:p2])
    min = sec/60
    sec = sec-min*60

  p = rec.find("viewCount='", p2)
  views = 0
  if p != -1:
    p2 = rec.find("'", p+11)
    views = int(rec[p+11:p2])

  return "%s [by %s, %02d:%02d, %d views]"%(title, author, min, sec, views)

def event_room_message(bot, (message, room, nick)):
  if message.getType() == 'groupchat':
    target = room
  else:
    target = room+'/'+nick

  text = message.getBody()
  if text:
    # allow identifying youtube links from self messages but prevent infinite loop
    if nick == bot.self_nick[room] and "'s YouTube link: " in text:
      return

    yid = None
    p = text.find('www.youtube.com/watch')
    if p != -1:
      p = text.find('v=', p)
      if p != -1:
        yid = text[p+2:p+2+11]
    if not yid:
      p = text.find('http://youtu.be/')
      if p != -1:
        yid = text[p+16:p+16+11]

    if yid and len(yid) == 11:
      try:
        res = "%s's YouTube link: %s"%(nick, getyoutubeinfo(yid))
        bot.send_room_message(target, res)
      except Exception, e:
        bot.log_warn('Error getting youtube video "%s" info: %s' % (yid, str(e)))

def load(bot):
  pass

def unload(bot):
  pass

def info(bot):
  return 'Youtube plugin v1.0.3'
