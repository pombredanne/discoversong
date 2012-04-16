import traceback
import sys
import web
import urllib
from bson import loads, dumps

__author__ = 'Eugene Efremov'

SETGETGO_WORDER = 'http://randomword.setgetgo.com/get.php'

def make_unique_email():
  
  random_word = urllib.urlopen(SETGETGO_WORDER).read()
  
  random_word = random_word[3:-2]
  
  return '%s@discoversong.com' % random_word.lower()

def generate_playlist_name(existing_names):
  base_name = "discoversong's finds"
  name = base_name
  i = 0
  while name in existing_names:
    i += 1
    name = '%s %i' % (base_name, i)
  return name

def printerrors(function):
  def wrapped(*a, **kw):
    try:
      return function(*a, **kw)
    except web.Redirect:
      raise
    except:
      traceback.print_exception(*sys.exc_info())
  return wrapped

def get_input():
  try:
    return web.input()
  except:
    return web.input(_unicode=False)

class BSONTranscoder(object):
  
  @staticmethod
  def encode(data):
    print 'encode', type(data)
    if not isinstance(data, dict):
      raise ValueError('BSON can only encode dictionary objects.')
    print dumps(data)
    return dumps(data)

  @staticmethod
  def decode(string):
    print 'decode', type(string)
    if not isinstance(string, basestring):
      raise ValueError('BSON can only decode strings.')
    return loads(string)

