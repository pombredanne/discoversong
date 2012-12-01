from discoversong.source_apps import DiscoversongSourceApp
from discoversong.source_apps.capabilities import Capabilities

class RedLaserApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email,)
  appname = 'redlaser'
  applabel = 'RedLaser'
  url = 'http://www.redlaser.com'
  
  def parse(subject, body):
    # circular import
    from discoversong.parse import has_parts, get_parts
    lead = "Check out '"
    separator = ' - '
    terminator = "' from RedLaser!"
    
    if not has_parts(subject, lead, separator, terminator):
      raise ValueError('Not RedLaser!')
    return get_parts(lead, separator, terminator, reversed=True)
