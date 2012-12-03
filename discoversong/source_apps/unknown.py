from discoversong.source_apps import DiscoversongSourceApp
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  return subject, ''

def parse_twitter(twitter):
  return twitter.replace('#', '').replace('@', '').replace('_', ' '), ''

class UnknownApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse), Capabilities.Twitter(parse_twitter),)

