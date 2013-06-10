#!/usr/bin/env python

from discoversong.parse import parse_twitter
from discoversong.rdio import get_discoversong_user_by_twitter, get_rdio_and_current_user
from discoversong.twitter import get_mentions
from discoversong.stats import read_to_mention
from discoversong.well_formed_search import well_formed_search, return_results

mentions = get_mentions()
for mention in mentions:
  disco_user_row = get_discoversong_user_by_twitter(mention.author.screen_name)
  if disco_user_row is None:
    continue
  try:
    title, artist = parse_twitter(mention.text)
  except:
    continue
  
  token, secret = str(disco_user_row['token']), str(disco_user_row['secret'])
  
  rdio, current_user, user_id = get_rdio_and_current_user(access_token=token, access_token_secret=secret)
  search_results = well_formed_search(rdio, user_id, artist, title)
  return_results(rdio, user_id, search_results, from_tweet_id=mention.id)
  read_to_mention(mention.id)
