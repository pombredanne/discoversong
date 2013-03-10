import logging
import traceback
import sys
import psycopg2
import web
import urllib
from bson import loads, dumps
import config

__author__ = 'Eugene Efremov'

SETGETGO_WORDER = 'http://randomword.setgetgo.com/get.php'

def get_environment_message():
  
  from discoversong.db import MASTER_PROD_DB_URL, MASTER_STAGE_DB_URL
  db_message = 'PROD!!!' if config.DB_URL_NAME == MASTER_PROD_DB_URL else 'staging' if config.DB_URL_NAME == MASTER_STAGE_DB_URL else 'other'

  return ('%s + %s' % (config.ENVIRONMENT, db_message)) if config.ENVIRONMENT != 'production' else ''

def make_unique_email():
  
  random_word = urllib.urlopen(SETGETGO_WORDER).read()
  
  random_word = random_word[3:-2]
  
  subdomain = '' if config.ENVIRONMENT == 'production' else 'test.'
  
  return '%s@%sdiscoversong.com' % (random_word.lower(), subdomain)

def generate_playlist_name(existing_names):
  base_name = "discoversong's finds"
  name = base_name
  i = 0
  while name in existing_names:
    i += 1
    name = '%s %i' % (base_name, i)
  return name

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

class Enum:
  pass

class Preferences(Enum):
  NoOrSearch = 'nor'
  OneResult = 'one'
  PlaylistToSaveTo = 'ply'
  AddToCollection = 'col'

NOT_SPECIFIED = object()

