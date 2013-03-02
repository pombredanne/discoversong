#!/usr/bin/env python

import os
import tweepy
from discoversong.parse import parse_twitter
from discoversong.rdio import get_discoversong_user_by_twitter, get_rdio_and_current_user

from discoversong.stats import get_last_mention, read_to_mention
from discoversong.well_formed_search import well_formed_search

token = os.environ['TWITTER_KEY']
secret = os.environ['TWITTER_SECRET']

user_token = os.environ['TWITTER_USER_TOKEN']
user_secret = os.environ['TWITTER_USER_SECRET']

auther = tweepy.auth.OAuthHandler(token, secret)
auther.set_access_token(user_token, user_secret)

api = tweepy.API(auther)

last_read = get_last_mention()
mentions = api.mentions(since_id=last_read)
for mention in mentions:
  disco_user_row = get_discoversong_user_by_twitter(mention.author.screen_name)
  if disco_user_row is None:
    continue
  read_to_mention(mention.id)
  try:
    title, artist = parse_twitter(mention.text)
  except:
    continue
  
  token, secret = str(disco_user_row['token']), str(disco_user_row['secret'])
  
  rdio, current_user, user_id = get_rdio_and_current_user(access_token=token, access_token_secret=secret)
  found = well_formed_search(rdio, user_id, artist, title)
  if len(found) > 0:
    title, artist, url = found[0]
    response = '"%(title)s" by %(artist)s %(link)s was new to @%(mention)s' % {
      'mention': mention.author.screen_name,
      'artist': artist,
      'title': title,
      'link': url}
    api.update_status(status=response, in_reply_to_status_id=mention.id)

  read_to_mention(mention.id)
