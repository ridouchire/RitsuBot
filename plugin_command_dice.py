# -*-coding:utf-8 -*-
import xmpp, time, re, random
from ritsu_api import *

drexp = re.compile(r'^(\d+)([DdUuZzWw])(\d+)(?:([HhLlEeFf\+\-\*\/])(\d+))?$')

def command_dice(bot, room, nick, access_level, parameters, message):
  if not parameters:
    return u'Ты выиграл!'
  dice_strs = map(lambda x: x.strip(), parameters.split(';'))
  if len(dice_strs) > 10:
    return u'Дохуя кубиков за раз!'
  return u'\n'.join(map(run_dice, dice_strs))

def run_dice(dice_str):
  result = ''
  m = drexp.match(dice_str)
  if m:
    count = int(m.group(1))
    die_type = m.group(2)
    die_sides = int(m.group(3))
    operator = m.group(4)
    operator_arg = m.group(5)
    if operator_arg:
      operator_arg = int(operator_arg)
    if count > 100 or die_sides > 1000 or (operator and operator_arg > 1000):
      return u'Дохуя'
    if (die_sides == 0) or ((die_type == 'w' or die_type == 'W') and (die_sides < 2)):
      return u'Охуел?'
    dice_runs = dice(count, die_type, die_sides)
    result += u'(' + u', '.join(map(str, dice_runs)) + u')'
    if not operator:
      result += u' = %d' % sum(dice_runs)
    elif operator == '+':
      result += u' + %d = %d' % (operator_arg, sum(dice_runs) + operator_arg)
    elif operator == '-':
      result += u' - %d = %d' % (operator_arg, sum(dice_runs) - operator_arg)
    elif operator == '*':
      result += u' * %d = %d' % (operator_arg, sum(dice_runs) * operator_arg)
    elif operator == '/':
      result += u' / %d = %d' % (operator_arg, sum(dice_runs) / operator_arg)
    elif operator == 'H' or operator == 'h':
      sorted_runs = sorted(dice_runs)
      vals = sorted_runs[-operator_arg:]
      result += u' макс (' + u', '.join(map(str, vals)) + (u') = %d' % sum(vals))
    elif operator == 'L' or operator == 'l':
      sorted_runs = sorted(dice_runs)
      vals = sorted_runs[0:operator_arg]
      result += u' мин (' + u', '.join(map(str, vals)) + (u') = %d' % sum(vals))
    elif operator == 'E' or operator == 'e':
      vals = map(lambda x: 1 if x >= operator_arg else 0, dice_runs)
      vals_str = map(lambda x: u'Успех' if x == 1 else u'Фейл', vals)
      result += u' успехи (' + u', '.join(vals_str) + (u') = %d' % sum(vals))
    elif operator == 'F' or operator == 'f':
      vals = map(lambda x: 1 if x >= operator_arg else -1, dice_runs)
      vals_str = map(lambda x: u'Успех' if x == 1 else u'Фейл', vals)
      result += u' успехи минус фейлы (' + u', '.join(vals_str) + (u') = %d' % sum(vals))
    return result
  else:
    return u"Обосрался ты, брат, с '%s'" % dice_str

def die(typ, sides):
  if typ == 'D' or typ == 'd':
    return [random.randint(1,sides)]
  elif typ == 'Z' or typ == 'z':
    return [random.randint(0,sides-1)]
  elif typ == 'U' or typ == 'u':
    return [random.randint(-sides,sides)]
  elif typ == 'W' or typ == 'w':
    r = []
    d = die('d', sides)
    while d == [sides]:
      r += d
      d = die('d', sides)
    r += d
  return r

def dice(num, typ, sides):
  # Гвидо, я твою мать ебал
  r = []
  for i in range(num):
    r += die(typ, sides)
  return r

def load(bot):
  random.seed()
  bot.add_command('dice', command_dice, LEVEL_GUEST, 'dice')
  bot.add_command(u'к', command_dice, LEVEL_GUEST, 'dice')
  bot.add_command(u'куб', command_dice, LEVEL_GUEST, 'dice')

def unload(bot):
  pass

def info(bot):
  return 'Dice plugin v1.0.1'

