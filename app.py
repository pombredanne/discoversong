#!/usr/bin/env python

# (c) 2011 Rdio Inc
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import json
import logging
import os
import sys
import web
import config

from eusful.errors import printerrors
from eusful.for_web import get_input

from discoversong import make_unique_email, BSONPostgresSerializer, Preferences, get_environment_message, stats, set_logging_level
from discoversong.db import get_db, USER_TABLE
from discoversong.forms import get_admin_content, editform
from discoversong.parse import parse
from discoversong.rdio import get_rdio, get_rdio_and_current_user, get_rdio_with_access, get_discoversong_user, get_db_prefs
from discoversong.source_apps.capabilities import ConfigStoredValue
from discoversong.well_formed_search import well_formed_search, return_results

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

set_logging_level()

urls = (
  '/', 'root',
  '/login', 'login',
  '/callback', 'callback',
  '/logout', 'logout',
  '/save', 'save',
  '/idsong', 'idsong',
  '/config', 'configger',
  '/admin', 'admin',
  '/admin/users', 'users',
  '/404', 'fourohfour',
  '/500', 'fivehundred',
)

app = web.application(urls, globals())

render = web.template.render('templates/')

def not_allowed(user_id):
  if len(config.WHITELIST_USERS) > 0:
    if user_id not in config.WHITELIST_USERS:
      return True
  return False

class root:
  
  @printerrors
  def GET(self):
    rdio, currentUser, user_id = get_rdio_and_current_user()
    
    if rdio and currentUser:
      if not_allowed(user_id):
        raise web.seeother('/logout')
      
      disco_user, message = get_discoversong_user(user_id)
      stats.visited(user_id)
      # circular import
      from discoversong.sources import SourceAppsManager
      return render.loggedin(name=currentUser['firstName'],
                             message=message,
                             sourceapps=SourceAppsManager.ALL,
                             env_message=get_environment_message())
    else:
      return render.loggedout(env_message=get_environment_message())

class admin:
  
  @printerrors
  def GET(self):
    
    rdio, currentUser, user_id = get_rdio_and_current_user()
    
    if rdio and currentUser:
      if user_id in config.ADMIN_USERS:
        input = get_input()
        
        if 'button' in input.keys():
          action = input['button']
          db = get_db()
          
          if action == 'doitnow_go_on_killme':
            if user_id in config.ADMIN_USERS:
              db.delete(USER_TABLE, where="rdio_user_id=%i" % user_id)
            raise web.seeother('/')

          elif action == 'clear_preferences':
            if user_id in config.ADMIN_USERS:
              db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict({}))
          
            raise web.seeother('/admin')
        
        else:
          admin=get_admin_content()
          return render.admin(env_message=get_environment_message(), admin=admin)
      
    raise web.seeother('/')

class users:
  
  @printerrors
  def GET(self):
    rdio, currentUser, user_id = get_rdio_and_current_user()
    
    if rdio and currentUser:
      if user_id in config.ADMIN_USERS:
        db = get_db()
        users = db.select(USER_TABLE, what='*')
        return render.admin_users(env_message=get_environment_message(), users=users)
    
    raise web.seeother('/')

class login:
  
  @printerrors
  def GET(self):
    # clear all of our auth cookies
    web.setcookie('at', '', expires=-1)
    web.setcookie('ats', '', expires=-1)
    web.setcookie('rt', '', expires=-1)
    web.setcookie('rts', '', expires=-1)
    # begin the authentication process
    rdio = get_rdio()
    url = rdio.begin_authentication(callback_url = web.ctx.homedomain+'/callback')
    # save our request token in cookies
    web.setcookie('rt', rdio.token[0], expires=60*60*24) # expires in one day
    web.setcookie('rts', rdio.token[1], expires=60*60*24) # expires in one day
    # go to Rdio to authenticate the app
    raise web.seeother(url)

class callback:
  
  @printerrors
  def GET(self):
    # get the state from cookies and the query string
    request_token = web.cookies().get('rt')
    request_token_secret = web.cookies().get('rts')
    verifier = get_input()['oauth_verifier']
    # make sure we have everything we need
    if request_token and request_token_secret and verifier:
      # exchange the verifier and request token for an access token
      rdio = get_rdio_with_access(request_token, request_token_secret)
      rdio.complete_authentication(verifier)
      # save the access token in cookies (and discard the request token)
      web.setcookie('at', rdio.token[0], expires=60*60*24*14) # expires in two weeks
      web.setcookie('ats', rdio.token[1], expires=60*60*24*14) # expires in two weeks
      web.setcookie('rt', '', expires=-1)
      web.setcookie('rts', '', expires=-1)
      # go to the home page
      raise web.seeother('/')
    else:
      # we're missing something important
      raise web.seeother('/logout')
    
class logout:
  
  @printerrors
  def GET(self):
    # clear all of our auth cookies
    web.setcookie('at', '', expires=-1)
    web.setcookie('ats', '', expires=-1)
    web.setcookie('rt', '', expires=-1)
    web.setcookie('rts', '', expires=-1)
    # and go to the homepage
    raise web.seeother('/')

class save:
  
  def get_prefs_from_input(self, input):
    prefs = {}
    
    prefs[Preferences.NoOrSearch] = Preferences.NoOrSearch in input.keys()
    prefs[Preferences.OneResult] = Preferences.OneResult in input.keys()
    prefs[Preferences.PlaylistToSaveTo] = input[Preferences.PlaylistToSaveTo] if Preferences.PlaylistToSaveTo in input.keys() else 'new'
    prefs[Preferences.AddToCollection] = Preferences.AddToCollection in input.keys()
    logging.info('new prefs %r' % prefs)
    return prefs
  
  @printerrors
  def GET(self):
    
    form_input = get_input()
    action = form_input['button']
    logging.info(form_input.items())
    rdio, currentUser, user_id = get_rdio_and_current_user()
    db = get_db()
    where_to_next = '/'
    
    if action == 'new_email':
      new_email = make_unique_email()
      db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, address=new_email)
      where_to_next += 'config?saved=True'
    
    elif action == 'save':
      where_to_next += 'config?saved=True'
      prefs = get_db_prefs(user_id, db=db)
      new_prefs = self.get_prefs_from_input(form_input)
      prefs.update(new_prefs)
      db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict(prefs))

      # circular import
      from discoversong.sources import SourceAppsManager
      for source_app in SourceAppsManager.ALL:
        for capability in source_app.capabilities:
          for configurable_thing in capability.config_options():
            if isinstance(configurable_thing, ConfigStoredValue):
              new_value = configurable_thing.read_from_input(form_input)
              logging.info('%s: %s' % (configurable_thing.name, new_value))
              if not configurable_thing.store_as_db_field:
                prefs = get_db_prefs(user_id, db=db)
                prefs[configurable_thing.name] = new_value
                db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict(prefs))
              else:
                db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, **{configurable_thing.name: new_value})

    raise web.seeother(where_to_next)

class idsong:

  @printerrors
  def POST(self):
    db = get_db()
    
    input = get_input()
    
    envelope = json.loads(input['envelope'])
    to_addresses = envelope['to']
    
    for to_address in to_addresses:
      
      lookup = db.select(USER_TABLE, where="address='%s'" % to_address)
      
      if len(lookup) == 1:
        result = lookup[0]
        
        access_token = str(result['token'])
        access_token_secret = str(result['secret'])
        
        rdio, current_user, user_id = get_rdio_and_current_user(access_token=access_token, access_token_secret=access_token_secret)
        
        stats.got_email(user_id)
        
        subject = input['subject']
        body = input['text']
        
        try:
          title, artist = parse(subject, body)
        except Exception as e:
          logging.exception(e.message)
          return None
        
        search_results = well_formed_search(rdio, user_id, artist, title)
        return_results(rdio, user_id, search_results)
    
    return None

class configger:
  @printerrors
  def GET(self):
    rdio, currentUser, user_id = get_rdio_and_current_user()
    disco_user, message = get_discoversong_user(user_id)
    prefs = BSONPostgresSerializer.to_dict(disco_user['prefs'])
    # circular import
    from discoversong.sources import SourceAppsManager
    
    return render.config(user=disco_user,
                         prefs=prefs,
                         capabilities=SourceAppsManager.all_capabilities(),
                         editform=editform(playlists=rdio.call('getPlaylists')['result']['owned'], prefs=get_db_prefs(user_id)),
                         env_message=get_environment_message(),
                         message=message)

def html_centered_image(title, image_uri):
  return '<html><head><title>%(title)s</title></head><body style="margin: 0px;"><table border="0" height="100%%" width="100%%"><tr><td><img src="%(image_uri)s" style="display: block; margin-left: auto; margin-right: auto;"/></tr></td></table></body>' % {'title': title, 'image_uri': image_uri}

class fourohfour:
  @printerrors
  def GET(self):
    return html_centered_image('discoversong:404', '/static/404.jpg')

class fivehundred:
  @printerrors
  def GET(self):
    return html_centered_image('discoversong:500', '/static/500.jpg')

def notfound():
  return web.seeother('/404')

def internalerror():
  return web.seeother('/500')

app.notfound = notfound
app.internalerror = internalerror

if __name__ == "__main__":
    app.run()
