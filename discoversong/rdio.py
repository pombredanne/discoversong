import os
import sys
import urllib2
import web

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from contrib.rdio import Rdio

from discoversong.includes import *

def get_consumer_key():
  if os.environ.has_key('RDIO_CONSUMER_KEY'):
    return os.environ['RDIO_CONSUMER_KEY']
  return RDIO_CONSUMER_KEY

def get_consumer_secret():
  if os.environ.has_key('RDIO_CONSUMER_SECRET'):
    return os.environ['RDIO_CONSUMER_SECRET']
  return RDIO_CONSUMER_SECRET

def get_rdio():
  return Rdio((get_consumer_key(), get_consumer_secret()))

def get_rdio_with_access(token, secret):
  return Rdio((get_consumer_key(), get_consumer_secret()), (token, secret))

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
    
    return rdio, currentUser
  
  else:
    
    return None, None

