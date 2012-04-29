from web import form

def editform(playlists, selected, prefs):
  
  new_playlist = ('new', '*** create a new playlist')
  always_new = ('alwaysnew', '*** always create a new playlist')
  playlist_options = [(playlist['key'], playlist['name']) for playlist in playlists]
  args = [new_playlist, always_new]
  args.extend(playlist_options)
  or_search = prefs.get('or_search', False)
  
  editform = form.Form(
      form.Dropdown(name='playlist',
                    description='Playlist to save songs to',
                    value=selected,
                    args=args),
      form.Checkbox(name='or_search', value=or_search, checked=or_search, description='Fall back to "or" search'),
      form.Button('button', value='save', html='Save'),
      form.Button('button', value='new_name', html='I want a new email address, mine sucks or has been compromised'),
  )
  
  return editform()
    
