import logging
import os
import sys
import urllib2
import web
import datetime
from discoversong.db import get_db, USER_TABLE

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from contrib.rdio import Rdio

from discoversong import NOT_SPECIFIED, make_unique_email, BSONPostgresSerializer, get_input, Preferences

import config

def get_rdio():
  return Rdio((config.RDIO_CONSUMER_KEY, config.RDIO_CONSUMER_SECRET))

def get_rdio_with_access(token, secret):
  open('log', 'w').write('\n'.join(map(str, [type(token), token, type(secret), secret])))
  return Rdio((config.RDIO_CONSUMER_KEY, config.RDIO_CONSUMER_SECRET), (token, secret))

def get_rdio_and_current_user(access_token=NOT_SPECIFIED, access_token_secret=NOT_SPECIFIED):
  if access_token == NOT_SPECIFIED:
    access_token = web.cookies().get('at')
  if access_token_secret == NOT_SPECIFIED:
    access_token_secret = web.cookies().get('ats')
  
  if access_token and access_token_secret:

    rdio = get_rdio_with_access(access_token, access_token_secret)
    # make sure that we can make an authenticated call
  
    try:
      currentUser = rdio.call('currentUser', {'extras': 'username'})['result']
    except urllib2.HTTPError:
      # this almost certainly means that authentication has been revoked for the app. log out.
      raise web.seeother('/logout')
    
    return rdio, currentUser, int(currentUser['key'][1:])
  
  else:
    
    return None, None, None

def get_db_prefs(user_id, db=None):
  if db is None:
    db = get_db()
  prefs = BSONPostgresSerializer.to_dict(list(db.select(USER_TABLE, what='prefs', where="rdio_user_id=%i" % user_id))[0]['prefs'])
  return prefs

def get_discoversong_user(user_id):
  db = get_db()

  disco_user = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))
  
  if len(disco_user) == 0:
    access_token = web.cookies().get('at')
    access_token_secret = web.cookies().get('ats')
    
    db.insert(USER_TABLE,
      rdio_user_id=user_id,
      address=make_unique_email(),
      token=access_token,
      secret=access_token_secret,
      first_use=datetime.date.today(),
      last_use=datetime.date.today(),
      emails=0,
      searches=0,
      songs=0,
      prefs=BSONPostgresSerializer.from_dict({}))
    
    disco_user = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))[0]
  else:
    disco_user = disco_user[0]
    
    def none_or_empty(strg):
      return strg is None or strg == ''
    
    def fields_need_update(field_names):
      for field in field_names:
        if not disco_user.has_key(field):
          return True
        if none_or_empty(disco_user[field]):
          return True
      return False
    
    if fields_need_update(['token', 'secret', 'address', 'prefs']):
      
      if fields_need_update(['token', 'secret']):
        access_token = web.cookies().get('at')
        access_token_secret = web.cookies().get('ats')
        db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, secret=access_token_secret, token=access_token)
      if fields_need_update(['address']):
        db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, address=make_unique_email())
      if fields_need_update(['prefs']):
        db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict({}))
      
      disco_user = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))[0]
  
  message = ''
  if 'saved' in get_input():
    message = '  Saved your selections.'
  
  if not disco_user.has_key('prefs') or not disco_user['prefs']:
    logging.info('resetting preferences')
    db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict({}))
    disco_user = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))[0]
  
  return disco_user, message

def get_discoversong_user_by_twitter(twitter_name):
  db = get_db()
  disco_users = list(db.select(USER_TABLE))
  for disco_user in disco_users:
    prefs = BSONPostgresSerializer.to_dict(disco_user['prefs'])
    if prefs.get(Preferences.TwitterName) == twitter_name:
      return disco_user
  return None
