from web import form

class RequiredValue(object):
  name = None
  description = None
  db_field = False
  def __init__(self, name, description, db_field=False):
    self.name = name
    self.description = description
    self.db_field = db_field
  
  def render(self, prefs):
    value = prefs.get(self.name)
    return self.description + ':' + form.Textbox(name=self.name, value=value).render()

class Capability(object):
  label = None
  
  def render(self, for_user):
    return '<strong>%s</strong>: configure it to %s' % (self.label, self._render(for_user))
  
  def _render(self, for_user):
    raise NotImplementedError()
  
  def required_values(self):
    raise NotImplementedError()

class Capabilities(object):
  
  class Email(Capability):
    label = 'Send email'
    parser = None
    
    def __init__(self, parser):
      self.parser = parser
    
    def _render(self, for_user):
      return 'send to <font style="color: green; font-size: larger;">%s</font>' % for_user['address']
    
    def required_values(self):
      return ()
    
    def parse(self, *args, **kwargs):
      return self.parser(*args, **kwargs)
  
  class Twitter(Capability):
    label = 'Post to Twitter'
    parser = None
    
    def __init__(self, parser, app_specific_text=''):
      self.parser = parser
      self.app_specific_text = app_specific_text
    
    def _render(self, for_user):
      return '%smention <a href="https://twitter.com/dscvrsng">@dscvrsng</a> and' % self.app_specific_text
    
    def required_values(self):
      return (RequiredValue(name='twitter_name', description='tell us your Twitter name'),)
    
    def parse(self, *args, **kwargs):
      return self.parser(*args, **kwargs)
