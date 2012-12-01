from web import form
from discoversong import Preferences
from discoversong.forms import Label

class RequiredValue(object):
  name = None
  description = None
  def __init__(self, name, description):
    self.name = name
    self.description = description
  
  def render(self, prefs):
    value = prefs.get(self.name)
    return self.description + ':' + form.Textbox(name=self.name, value=value).render()

class Capability(object):
  label = None
  
  @classmethod
  def render(cls, for_user):
    return '<strong>%s</strong>: configure it to %s' % (cls.label, cls._render(for_user))
  
  @staticmethod
  def _render(for_user):
    raise NotImplementedError()
  
  @staticmethod
  def required_values():
    raise NotImplementedError()

class Capabilities(object):
  
  class Email(Capability):
    label = 'Send email'
    parser = None
    
    def __init__(self, parser):
      self.parser = parser
    
    @classmethod
    def _render(cls, for_user):
      return 'send to <font style="color: green; font-size: larger;">%s</font>' % for_user['address']
    
    def required_values(self):
      return ()
    
    def parse(self, **kwargs):
      return self.parser(**kwargs)
  
  class Twitter(Capability):
    label = 'Post to Twitter'
    @classmethod
    def _render(cls, for_user):
      return 'mention <a href="https://twitter.com/dscvrsng">@dscvrsng</a> and'
    
    @staticmethod
    def required_values():
      return (RequiredValue(name=Preferences.TwitterName, description='tell us your Twitter name'),)
