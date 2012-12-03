from discoversong.source_apps import DiscoversongSourceApp, ParseError
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = 'I just used @musixmatch to discover '
  separator = ' by '
  terminator = ' #lyrics'
  
  if not has_parts(body, lead, separator, terminator):
    raise ParseError('Not MusixMatch!')
  return get_parts(body, lead, separator, terminator)

class MusixMatchApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse),)
  appname = 'musixmatch'
  applabel = 'MusiXmatch'
  url = 'http://www.musixmatch.com'
