from discoversong.source_apps import DiscoversongSourceApp
from discoversong.source_apps.capabilities import Capabilities

class EricssonTrackIdApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email)
  appname = 'ericssontrackid'
  applabel = 'Sony Ericsson Track ID'
  url = 'https://play.google.com/store/apps/details?id=com.sonyericsson.trackid'
  
  @classmethod
  def parse(subject, body):
    # circular import
    from discoversong.parse import has_parts, get_parts
    lead = 'Check out '
    separator = ' by '
    terminator = '! I just found it using TrackID'
    
    if not has_parts(body, lead, separator, terminator):
      raise ValueError('Not TrackID!')
    return get_parts(body, lead, separator, terminator)
  
  
