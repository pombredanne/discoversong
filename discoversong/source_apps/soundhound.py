# encoding: utf-8
from lxml import etree
import requests

from discoversong.source_apps import DiscoversongSourceApp, ParseError
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = 'Just found '
  separator = ' by '
  terminator = ' on #SoundHound'
  
  if not has_parts(body, lead, separator, terminator):
    raise ParseError('Not SoundHound!')
  return get_parts(body, lead, separator, terminator)

def parse_twitter(twit_content):
  # circular import
  from discoversong.parse import has_parts, get_parts
  lead = u'@dscvrsng – '
  separator = ' by '
  url_prefix = ', from #SoundHound '
  if not has_parts(twit_content, lead, separator, url_prefix):
    raise ParseError('%s Not SoundHound!' % twit_content)
  title, artist_twit_name = get_parts(twit_content, lead, separator, url_prefix)
  url = twit_content[twit_content.find(url_prefix) + len(url_prefix):]
  tree = etree.HTML(requests.get(url).text)
  artist = tree.xpath('//div[@class="artistName"]/a/text()')[0]
  return title, artist

class SoundHoundApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse), Capabilities.Twitter(parse_twitter))
  appname = 'soundhound'
  applabel = 'SoundHound'
  url = 'http://www.soundhound.com'
