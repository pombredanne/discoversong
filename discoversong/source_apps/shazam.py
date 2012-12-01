from discoversong.source_apps import DiscoversongSourceApp
from discoversong.source_apps.capabilities import Capabilities

class ShazamApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email, Capabilities.Twitter)
  appname = 'shazam'
  applabel = 'Shazam'
  url = 'http://www.shazam.com'
  
  @classmethod
  def parse_1(subject, body):
    # circular import
    from discoversong.parse import has_parts, get_parts
    lead = 'I just used Shazam to tag '
    separator = ' by '
    terminator = '.'
    
    if not has_parts(subject, lead, separator, terminator):
      raise ValueError('Not Shazam!')
    return get_parts(subject, lead, separator, terminator)
  
  @classmethod
  def parse_2(subject, body):
    # circular import
    from discoversong.parse import has_parts, get_parts
    expected_subject = 'I just used Shazam'
    lead = 'I just used #Shazam to discover '
    separator = ' by '
    terminator = '.'
  
    if subject != expected_subject or not has_parts(body, lead, separator, terminator):
      raise ValueError('Not Shazam2!')
    return get_parts(body, lead, separator, terminator)
  
  @classmethod
  def parse(subject, body):
    try:
      return ShazamApp.parse_1(subject, body)
    except:
      return ShazamApp.parse_2(subject, body)
