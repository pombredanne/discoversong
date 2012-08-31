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

import datetime
import json
import os
import sys
import web
import logging
import config

from discoversong import make_unique_email, generate_playlist_name, printerrors, get_input, BSONPostgresSerializer, Preferences, get_environment_message, stats
from discoversong.db import get_db, USER_TABLE
from discoversong.forms import editform, get_admin_content
from discoversong.parse import parse
from discoversong.rdio import get_rdio, get_rdio_and_current_user, get_rdio_with_access

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

urls = (
  '/', 'root',
  '/login', 'login',
  '/callback', 'callback',
  '/logout', 'logout',
  '/save', 'save',
  '/idsong', 'idsong',
  '/admin', 'admin',
  '/admin/users', 'users',
)

app = web.application(urls, globals())

render = web.template.render('templates/')

def not_allowed(user_id):
  if len(config.WHITELIST_USERS) > 0:
    if user_id not in config.WHITELIST_USERS:
      print 'not allowed because', user_id, 'not in', config.WHITELIST_USERS
      return True
  return False

class root:
  
  @printerrors
  def GET(self):
    logging.info('!!!!! root')
    rdio, currentUser, user_id = get_rdio_and_current_user()
    
    if rdio and currentUser:
      
      if not_allowed(user_id):
        raise web.seeother('/logout')
      
      myPlaylists = rdio.call('getPlaylists')['result']['owned']
      
      db = get_db()
      
      result = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))
      
      if len(result) == 0:
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
        
        result = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))[0]
      else:
        result = result[0]
        
        def none_or_empty(strg):
          return strg is None or strg == ''
        
        def fields_need_update(field_names):
          for field in field_names:
            if not result.has_key(field):
              return True
            if none_or_empty(result[field]):
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
          
          result = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))[0]
      
      stats.visited(user_id)
      
      message = ''
      if 'saved' in get_input():
        message = '  Saved your selections.'
      
      if not result.has_key('prefs') or not result['prefs']:
        logging.info('resetting preferences')
        db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict({}))
        result = list(db.select(USER_TABLE, where="rdio_user_id=%i" % user_id))[0]
      
      return render.loggedin(name=currentUser['firstName'],
                             message=message,
                             to_address=result['address'],
                             editform=editform(myPlaylists, BSONPostgresSerializer.to_dict(result['prefs'])),
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
    logging.info('!!!!! login')
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
    prefs[Preferences.PlaylistToSaveTo] = input[Preferences.PlaylistToSaveTo]
    prefs[Preferences.AddToCollection] = input[Preferences.AddToCollection]
    
    return prefs
  
  @printerrors
  def GET(self):
    
    input = get_input()
    action = input['button']
    
    rdio, currentUser, user_id = get_rdio_and_current_user()
    db = get_db()
    
    if action == 'save':
      prefs = BSONPostgresSerializer.to_dict(list(db.select(USER_TABLE, what='prefs', where="rdio_user_id=%i" % user_id))[0]['prefs'])
      new_prefs = self.get_prefs_from_input(input)
      prefs.update(new_prefs)
      db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict(prefs))
      
      raise web.seeother('/?saved=True')
    
    elif action == 'new_name':
      
      new_email = make_unique_email()
      
      db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, address=new_email)
    
    raise web.seeother('/')

class idsong:

  @printerrors
  def POST(self):
    db = get_db()
    
    input = get_input()
    
    envelope = json.loads(input['envelope'])
    to_addresses = envelope['to']
    
    print 'received email to', to_addresses
    
    for to_address in to_addresses:
      
      lookup = db.select(USER_TABLE, where="address='%s'" % to_address)
      
      if len(lookup) == 1:
        result = lookup[0]
        
        access_token = str(result['token'])
        access_token_secret = str(result['secret'])
        
        rdio, current_user, user_id = get_rdio_and_current_user(access_token=access_token, access_token_secret=access_token_secret)
        
        print 'found user', current_user['username']
        
        stats.got_email(user_id)
        
        subject = input['subject']
        body = input['text']
        
        try:
          title, artist = parse(subject, body)
        except Exception as e:
          print e.message
          return None
        
        print 'parsed artist', artist, 'title', title
        
        prefs = BSONPostgresSerializer.to_dict(result['prefs'])
        
        or_search = prefs.get(Preferences.NoOrSearch, False)
        one_result = prefs.get(Preferences.OneResult, False)
        playlist_key = prefs[Preferences.PlaylistToSaveTo]
        add_to_collection = prefs.get(Preferences.AddToCollection, False)
        
        never_or = 'false' if or_search else 'true'
        
        if never_or:
          print 'searching strictly, no fallback to or'
        
        stats.made_search(user_id)
        search_result = rdio.call('search', {'query': ' '.join([title, artist]), 'types': 'Track', 'never_or': never_or})
        
        track_keys = []
        name_artist_pairs_found = {}
        
        for possible_hit in search_result['result']['results']:
          
          if possible_hit['canStream']:
            
            name = possible_hit['name']
            artist_name = possible_hit['artist']
            
            if name_artist_pairs_found.has_key((name, artist_name)):
              continue
            
            name_artist_pairs_found[(name, artist_name)] = True
            
            track_key = possible_hit['key']
            track_keys.append(track_key)
            
            if one_result:
              break
        
        print 'found tracks', track_keys
        
        playlists = rdio.call('getPlaylists')['result']['owned']
        p_keys = [playlist['key'] for playlist in playlists]
        p_names = [playlist['name'] for playlist in playlists]
        
        print playlist_key, 'existing playlists', p_keys
        
        if playlist_key in ['new', 'alwaysnew'] or playlist_key not in p_keys:
          
          new_name = generate_playlist_name(p_names)
          
          print 'creating new playlist', new_name
          
          result = rdio.call('createPlaylist', {'name': new_name,
                                                'description': 'Songs found by discoversong on %s.' % datetime.datetime.now().strftime('%A, %d %b %Y %H:%M'),
                                                'tracks': ', '.join(track_keys)})
          new_key = result['result']['key']
          
          if playlist_key == 'new' or playlist_key not in p_keys:
            
            print 'setting', new_key, 'as the playlist to use next time'
            prefs[Preferences.PlaylistToSaveTo] = new_key
            db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict(prefs))
          
          # else leave 'alwaysnew' to repeat this behavior every time
        
        elif playlist_key == 'noplaylist':
          
          print 'not adding to playlist'
          
        else:
          
          print 'adding to existing playlist', playlist_key
          rdio.call('addToPlaylist', {'playlist': playlist_key, 'tracks': ', '.join(track_keys)})
        
        if add_to_collection:
          
          print 'adding to collection'
          rdio.call('addToCollection', {'keys': ', '.join(track_keys)})
        
        stats.found_songs(user_id, len(track_keys))
    
    return None

if __name__ == "__main__":
    app.run()
