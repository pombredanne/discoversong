import logging
import os
import twython

from discoversong.stats import get_last_mention

def api():
  token = os.environ['TWITTER_KEY']
  secret = os.environ['TWITTER_SECRET']
  
  user_token = os.environ['TWITTER_USER_TOKEN']
  user_secret = os.environ['TWITTER_USER_SECRET']
  
  api = twython.Twython(token, secret, user_token, user_secret)
  return api

def get_mentions():
  return api().get_mentions_timeline(since_id=get_last_mention())

def tweet_about_found_song(title, artist, url, mention_name=None, reply_to_tweet_id=None):
  response = '"%(title)s" by %(artist)s %(link)s was new to %(mention)s!' % {
    'title': title,
    'artist': artist,
    'link': url,
    'mention': mention_name or 'someone'}
  logging.debug(response)
  api().update_status(status=response, in_reply_to_status_id=reply_to_tweet_id)

def announce_new_user(user_count):
  status = '*ding* New user #%i on @dscvrsng!' % user_count
  logging.debug(status)
  api().update_status(status)
