from discoversong.source_apps import DiscoversongSourceApp
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = 'Just found '
  separator = ' by '
  terminator = ' on #SoundHound'
  
  if not has_parts(body, lead, separator, terminator):
    raise ValueError('Not SoundHound!')
  return get_parts(body, lead, separator, terminator)

class SoundHoundApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse), Capabilities.Twitter)
  appname = 'soundhound'
  applabel = 'SoundHound'
  url = 'http://www.soundhound.com'
