from discoversong.source_apps import DiscoversongSourceApp, ParseError
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts

  lead = 'Music ID: "'
  separator = '" by '
  
  if not has_parts(subject, lead, separator):
    raise ParseError('not VCast!')
  return get_parts(subject, lead, separator)

class VcastSongidApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse),)
  appname = 'vcast_songid'
  applabel = 'VCast SongID'
  url = 'https://mediastore.verizonwireless.com/'
