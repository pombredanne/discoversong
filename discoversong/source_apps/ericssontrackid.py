from discoversong.source_apps import DiscoversongSourceApp, ParseError
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = 'Check out '
  separator = ' by '
  terminator = '! I just found it using TrackID'
  
  if not has_parts(body, lead, separator, terminator):
    raise ParseError('Not TrackID!')
  return get_parts(body, lead, separator, terminator)

class EricssonTrackIdApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse),)
  appname = 'ericssontrackid'
  applabel = 'Sony Ericsson Track ID'
  url = 'https://play.google.com/store/apps/details?id=com.sonyericsson.trackid'
