from discoversong.source_apps import DiscoversongSourceApp, ParseError
from discoversong.source_apps.capabilities import Capabilities

def parse_1(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = 'I just used Shazam to tag '
  separator = ' by '
  terminator = '.'
  
  if not has_parts(subject, lead, separator, terminator):
    raise ParseError('Not Shazam!')
  return get_parts(subject, lead, separator, terminator)

def parse_2(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts
  expected_subject = 'I just used Shazam'
  lead = 'I just used #Shazam to discover '
  separator = ' by '
  terminator = '.'

  if subject != expected_subject or not has_parts(body, lead, separator, terminator):
    raise ParseError('Not Shazam!')
  return get_parts(body, lead, separator, terminator)

def parse(subject, body):
  try:
    return parse_1(subject, body)
  except:
    return parse_2(subject, body)

def parse_twitter_1(twit_content):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = 'discover '
  separator = ' by '
  terminator = '.'
  if not has_parts(twit_content, lead, separator, terminator):
    raise ParseError('%s Not Shazam!' % twit_content)
  title, artist = get_parts(twit_content, lead, separator, terminator)
  return title, artist

def parse_twitter_2(twit_content):
  # I just used #Shazam to tag Lights by Ellie Goulding. http://shz.am/t53069421
  from discoversong.parse import has_parts, get_parts
  lead = '#Shazam to tag '
  separator = ' by '
  terminator = '. http'
  if not has_parts(twit_content, lead, separator, terminator):
    raise ParseError('%s Not Shazam 2!' % twit_content)
  title, artist = get_parts(twit_content, lead, separator, terminator)
  return title, artist

def parse_twitter(twit_content):
  try:
    return parse_twitter_1(twit_content)
  except:
    return parse_twitter_2(twit_content)

class ShazamApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse), Capabilities.Twitter(parse_twitter, app_specific_text='before the word "discover" '))
  appname = 'shazam'
  applabel = 'Shazam'
  url = 'http://www.shazam.com'
