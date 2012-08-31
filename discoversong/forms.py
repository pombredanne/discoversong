from web import form
from discoversong import Preferences
from discoversong.db import get_db, USER_TABLE, STATS_TABLE

def editform(playlists, prefs):
  
  new_playlist = ('new', '*** create a new playlist')
  always_new = ('alwaysnew', '*** always create a new playlist')
  no_playlist = ('noplaylist', '*** do not add to a playlist')
  playlist_options = [(playlist['key'], playlist['name']) for playlist in playlists]
  args = [new_playlist, always_new, no_playlist]
  args.extend(playlist_options)
  
  or_search = prefs.get(Preferences.NoOrSearch, False)
  one_result = prefs.get(Preferences.OneResult, False)
  add_to_collection = prefs.get(Preferences.AddToCollection, False)
  selected = prefs.get(Preferences.PlaylistToSaveTo, 'new')
  
  editform = form.Form(
      form.Dropdown(name=Preferences.PlaylistToSaveTo,
                    description='Playlist to save songs to',
                    value=selected,
                    args=args),
      form.Checkbox(name=Preferences.NoOrSearch, value=or_search, checked=or_search, description='Strict search, no "or" fallback'),
      form.Checkbox(name=Preferences.OneResult, value=one_result, checked=one_result, description='Save only the best match'),
      form.Checkbox(name=Preferences.AddToCollection, value=add_to_collection, checked=add_to_collection, description='Add to collection'),
      form.Button('button', value='save', html='Save'),
      form.Button('button', value='new_name', html='I want a new email address, mine sucks or has been compromised'),
  )
  
  return editform()

class Label(form.Input):
    def is_hidden(self):
        return False
        
    def get_type(self):
        return 'hidden'

def get_admin_content():
  
  fields = tuple()
  
  db = get_db()
  user_count = db.select(USER_TABLE, what='count(*)')[0]['count']
  
  stats = db.select(STATS_TABLE, what='emails, searches, songs, visits')[0]
  fields += (Label(name='', description='ADMIN'),)
  fields += (Label(name='', description='User Count: %i' % user_count),)
  fields += (form.Button(name='button', value='clear_preferences', html='clear my preferences'),)
  fields += (form.Button(name='button', value='doitnow_go_on_killme', html='delete my user row'),)
  fields += (Label(name='', description='Visits: %i' % stats['visits']),)
  fields += (Label(name='', description='Emails: %i' % stats['emails']),)
  fields += (Label(name='', description='Searches: %i' % stats['searches']),)
  fields += (Label(name='', description='Songs: %i' % stats['songs']),)
  adminform = form.Form(*fields)
  
  return adminform()
