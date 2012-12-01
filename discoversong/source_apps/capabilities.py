class Capability(object):
  @classmethod
  def render(cls, for_user):
    return '<strong>%s</strong>: configure it to %s' % (cls.label, cls._render(for_user))
  
  @staticmethod
  def _render(for_user):
    raise NotImplementedError()
  
  label = '<ERROR>'

class Capabilities(object):
  
  class Email(Capability):
    label = 'Send email'
    @staticmethod
    def _render(for_user):
      return 'send to <font style="color: green; font-size: larger;">%s</font>' % for_user['address']
  
  class Twitter(Capability):
    label = 'Post to Twitter'
    @staticmethod
    def _render(for_user):
      return 'mention <a href="https://twitter.com/dscvrsng">@dscvrsng</a> (discoversong without the vowels)'

