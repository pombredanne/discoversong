#!/usr/bin/env python

import os
import tweepy
from discoversong.parse import parse_tweet
from discoversong.rdio import get_discoversong_user_by_twitter, get_rdio, get_db_prefs, get_rdio_and_current_user

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
  print 'found twitter name', mention.author.screen_name
  disco_user_row = get_discoversong_user_by_twitter(mention.author.screen_name)
  
  artist, title = parse_tweet(mention.text)
  print 'found artist, title', artist, title
  token, secret = str(disco_user_row['token']), str(disco_user_row['secret'])
  
  rdio, current_user, user_id = get_rdio_and_current_user(access_token=token, access_token_secret=secret)
  well_formed_search(rdio, user_id, get_db_prefs(user_id), artist, title)
  read_to_mention(mention.id)
