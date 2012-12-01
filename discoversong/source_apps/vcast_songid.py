from discoversong.source_apps import DiscoversongSourceApp
from discoversong.source_apps.capabilities import Capabilities

class VcastSongidApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email,)
  appname = 'vcast_songid'
  applabel = 'VCast SongID'
  url = 'https://mediastore.verizonwireless.com/'
  
  @classmethod
  def parse(subject, body):
    # circular import
    from discoversong.parse import has_parts, get_parts

    lead = 'Music ID: "'
    separator = '" by '
    
    if not has_parts(subject, lead, separator):
      raise ValueError('not VCast!')
    return get_parts(subject, lead, separator)
  
  
