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

def parse_twitter(twit_content):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = 'discover '
  separator = ' by '
  terminator = '.'
  if not has_parts(twit_content, lead, separator, terminator):
    raise ParseError('%s Not Shazam!' % twit_content)
  title, artist = get_parts(twit_content, lead, separator, terminator)
  return title, artist

class ShazamApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse), Capabilities.Twitter(parse_twitter, app_specific_text='before the word "discover" '))
  appname = 'shazam'
  applabel = 'Shazam'
  url = 'http://www.shazam.com'
