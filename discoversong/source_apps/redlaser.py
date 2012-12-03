from discoversong.source_apps import DiscoversongSourceApp, ParseError
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = "Check out '"
  separator = ' - '
  terminator = "' from RedLaser!"
  
  if not has_parts(subject, lead, separator, terminator):
    raise ParseError('Not RedLaser!')
  return get_parts(lead, separator, terminator, reversed=True)

class RedLaserApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse),)
  appname = 'redlaser'
  applabel = 'RedLaser'
  url = 'http://www.redlaser.com'
  
