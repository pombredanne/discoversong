from discoversong.source_apps import DiscoversongSourceApp
from discoversong.source_apps.capabilities import Capabilities

def parse(subject, body):
  return subject, ''

class UnknownApp(DiscoversongSourceApp):
  capabilities = (Capabilities.Email(parse),)

