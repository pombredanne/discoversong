from web import form
from discoversong.parse import parse_bool

def editform(playlists, selected, prefs):
  
  def map_type(tp):
    if tp is bool:
      return form.Checkbox
    raise ValueError("can't handle %s" % str(tp))
  
  new_playlist = ('new', '*** create a new playlist')
  always_new = ('alwaysnew', '*** always create a new playlist')
  playlist_options = [(playlist['key'], playlist['name']) for playlist in playlists]
  args = [new_playlist, always_new]
  args.extend(playlist_options)
  
  form_elements = (
    form.Dropdown(name='playlist',
                      description='Playlist to save songs to',
                      value=selected,
                      args=args),
    form.Checkbox(name='or_search', value=prefs['or_search'], checked=parse_bool(prefs['or_search']), html='Run a less-strict "or" search'),
    form.Button('button', value='save', html='Save'),
    form.Button('button', value='new_name', html='I want a new email address, mine sucks or has been compromised'),
  )
  
  editform = form.Form(*form_elements)
  
  return editform()
    
