import datetime
from discoversong import BSONPostgresSerializer, Preferences, stats, generate_playlist_name
from discoversong.db import USER_TABLE, get_db
from discoversong.rdio import get_db_prefs

def well_formed_search(rdio, user_id, artist, title):
  db = get_db()
  prefs = get_db_prefs(user_id, db=db)
  or_search = prefs.get(Preferences.NoOrSearch, False)
  one_result = prefs.get(Preferences.OneResult, False)
  playlist_key = prefs.get(Preferences.PlaylistToSaveTo, 'new')
  add_to_collection = prefs.get(Preferences.AddToCollection, False)
  actual_name_artist_pairs = []
  never_or = 'false' if or_search else 'true'
  
  if never_or:
    print 'searching strictly, no fallback to or'
  
  stats.made_search(user_id)
  search_result = rdio.call('search', {'query': ' '.join([artist, title]), 'types': 'Track', 'never_or': never_or})
  
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
      actual_name_artist_pairs.append((name, artist_name))
      if one_result:
        break
  
  print 'found tracks', track_keys
  
  playlists_call = rdio.call('getPlaylists')
  if 'result' in playlists_call:
    playlists = playlists_call['result']['owned']
  else:
    playlists = []
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
  return actual_name_artist_pairs

