from discoversong.source_apps import DiscoversongSourceApp

class UnknownApp(DiscoversongSourceApp):
  @classmethod
  def parse(subject, body):
    return subject, ''
