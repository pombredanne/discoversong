import traceback
import sys
import psycopg2
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

class BSONPostgresSerializer(object):
  
  @staticmethod
  def from_dict(data):
    if not isinstance(data, dict):
      raise ValueError('Need a dictionary object.')
    return psycopg2.Binary(dumps(data))

  @staticmethod
  def to_dict(string):
    try:
      if not isinstance(string, basestring):
        return loads(str(string))
      return loads(string)
    except:
      raise ValueError('Expected a string or buffer.')
