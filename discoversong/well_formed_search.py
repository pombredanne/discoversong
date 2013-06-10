import datetime
from discoversong import BSONPostgresSerializer, Preferences, stats, generate_playlist_name
from discoversong.db import USER_TABLE, get_db
from discoversong.rdio import get_db_prefs, get_discoversong_user
from discoversong.source_apps.capabilities import Capabilities
from discoversong.twitter import tweet_about_found_song

def well_formed_search(rdio, user_id, artist, title):
  db = get_db()
  prefs = get_db_prefs(user_id, db=db)
  or_search = prefs.get(Preferences.NoOrSearch, False)
  one_result = prefs.get(Preferences.OneResult, False)
  results = []
  never_or = 'false' if or_search else 'true'
  
  stats.made_search(user_id)
  search_result = rdio.call('search', {'query': ' '.join([artist, title]), 'types': 'Track', 'never_or': never_or})
  
  name_artist_pairs_found = {}
  
  for possible_hit in search_result['result']['results']:
    
    if possible_hit['canStream']:
      name = possible_hit['name']
      artist_name = possible_hit['artist']
      
      if name_artist_pairs_found.has_key((name, artist_name)):
        continue
      
      name_artist_pairs_found[(name, artist_name)] = True
      
      results.append((name, artist_name, possible_hit['shortUrl'], possible_hit['key']))
      if one_result:
        break
  
  return results

def return_results(rdio, user_id, song_artist_url_list, from_tweet_id=None):
  db = get_db()
  prefs = get_db_prefs(user_id, db=db)
  
  playlist_key = prefs.get(Preferences.PlaylistToSaveTo, 'new')
  add_to_collection = prefs.get(Preferences.AddToCollection, False)
  track_keys_list = [s[3] for s in song_artist_url_list]
  
  playlists_call = rdio.call('getPlaylists')
  if 'result' in playlists_call:
    playlists = playlists_call['result']['owned']
  else:
    playlists = []
  p_keys = [playlist['key'] for playlist in playlists]
  p_names = [playlist['name'] for playlist in playlists]
  
  if playlist_key in ['new', 'alwaysnew'] or playlist_key not in p_keys:
    new_name = generate_playlist_name(p_names)
    result = rdio.call('createPlaylist', {'name': new_name,
                                          'description': 'Songs found by discoversong on %s.' % datetime.datetime.now().strftime('%A, %d %b %Y %H:%M'),
                                          'tracks': ', '.join(track_keys_list)})
    new_key = result['result']['key']
    
    if playlist_key == 'new' or playlist_key not in p_keys:
      prefs[Preferences.PlaylistToSaveTo] = new_key
      db.update(USER_TABLE, where="rdio_user_id=%i" % user_id, prefs=BSONPostgresSerializer.from_dict(prefs))
    
    # else leave 'alwaysnew' to repeat this behavior every time
  
  else:
    rdio.call('addToPlaylist', {'playlist': playlist_key, 'tracks': ', '.join(track_keys_list)})
  
  if add_to_collection:
    rdio.call('addToCollection', {'keys': ', '.join(track_keys_list)})
  
  stats.found_songs(user_id, len(song_artist_url_list))
  
  can_mention_config = Capabilities.Twitter().config_options_dict()['mention_in_reply']
  twitter_name_config = Capabilities.Twitter().config_options_dict()['twitter_name']
  user, message = get_discoversong_user(user_id)
  
  should_mention = can_mention_config.get_value(user)
  
  twitter_name = ('@' + twitter_name_config.get_value(user)) if should_mention else None
  reply_to_tweet_id = from_tweet_id if should_mention else None
  
  song, artist, url, track_key = song_artist_url_list[0]
  tweet_about_found_song(song, artist, url, mention_name=twitter_name, reply_to_tweet_id=reply_to_tweet_id)
