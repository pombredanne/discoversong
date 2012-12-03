class DiscoversongSourceApp(object):
  capabilities = tuple()
  
  def parse(self, subject, body):
    raise NotImplementedError()

class ParseError(ValueError):
  pass
