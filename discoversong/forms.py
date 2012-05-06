from web import form
from discoversong import Preferences
from discoversong.db import get_db, USER_TABLE

def editform(playlists, prefs):
  
  new_playlist = ('new', '*** create a new playlist')
  always_new = ('alwaysnew', '*** always create a new playlist')
  playlist_options = [(playlist['key'], playlist['name']) for playlist in playlists]
  args = [new_playlist, always_new]
  args.extend(playlist_options)
  
  or_search = prefs.get(Preferences.NoOrSearch, False)
  one_result = prefs.get(Preferences.OneResult, False)
  selected = prefs.get(Preferences.PlaylistToSaveTo, 'new')
  
  editform = form.Form(
      form.Dropdown(name=Preferences.PlaylistToSaveTo,
                    description='Playlist to save songs to',
                    value=selected,
                    args=args),
      form.Checkbox(name=Preferences.NoOrSearch, value=or_search, checked=or_search, description='Strict search, no "or" fallback'),
      form.Checkbox(name=Preferences.OneResult, value=one_result, checked=one_result, description='Save only the best match'),
      form.Button('button', value='save', html='Save'),
      form.Button('button', value='new_name', html='I want a new email address, mine sucks or has been compromised'),
  )
  
  return editform()

class Label(form.Input):
    def is_hidden(self):
        return False
        
    def get_type(self):
        return 'hidden'

def get_admin_content(is_admin):
  
  fields = tuple()
  
  if is_admin:
    db = get_db()
    user_count = db.select(USER_TABLE, what='count(*)')[0]['count']
    fields += (Label(name='', description='ADMIN'),)
    fields += (Label(name='', description='User Count: %i' % user_count),)
    fields += (form.Button(name='button', value='clear_preferences', html='clear my preferences'),)
    fields += (form.Button(name='button', value='doitnow_go_on_killme', html='delete my user row'),)
  
  adminform = form.Form(*fields)
  
  return adminform()
