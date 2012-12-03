class DiscoversongSourceApp(object):
  capabilities = tuple()
  
  @classmethod
  def parse(subject, body):
    raise NotImplementedError()

class ParseError(ValueError):
  pass
