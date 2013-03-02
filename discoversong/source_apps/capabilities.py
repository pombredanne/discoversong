from web import form
from discoversong import BSONPostgresSerializer

class ConfigOption(object):
  name = None
  description = None
  def __init__(self, name, description):
    self.name = name
    self.description = description
  
  def render(self, user):
    raise NotImplementedError()

class ConfigTextValue(ConfigOption):
  store_as_db_field = False
  def __init__(self, name, description, store_as_db_field=False):
    super(ConfigTextValue, self).__init__(name, description)
    self.store_as_db_field = store_as_db_field
  
  def render(self, user):
    if self.store_as_db_field:
      value = getattr(user, self.name, 'None')
    else:
      prefs = BSONPostgresSerializer.to_dict(user['prefs'])
      value = prefs.get(self.name)
    return self.description % form.Textbox(name=self.name, value=value).render()

class ConfigButton(ConfigOption):
  def __init__(self, name, description, label):
    super(ConfigButton, self).__init__(name, description)
    self.label = label

  def render(self, user):
    return self.description % form.Button(id=self.name, name='button', value=self.name, html=self.label).render()

class Capability(object):
  label = None
  
  def render(self, for_user):
    return 'Configure it to %s' % (self._render(for_user))
  
  def _render(self, for_user):
    raise NotImplementedError()
  
  def config_options(self):
    raise NotImplementedError()

class Capabilities(object):
  
  class Email(Capability):
    label = 'send email'
    parser = None
    
    def __init__(self, parser):
      self.parser = parser
    
    def _render(self, for_user):
      return 'send to <font style="color: green; font-size: larger;">%s</font>' % for_user['address']
    
    def config_options(self):
      return (ConfigButton(name='new_email', description='You can also get a %s email address (if you hate yours, or it\'s no longer secret)', label='New!'),)
    
    def parse(self, *args, **kwargs):
      return self.parser(*args, **kwargs)
  
  class Twitter(Capability):
    label = 'post to Twitter'
    parser = None
    
    def __init__(self, parser, app_specific_text=''):
      self.parser = parser
      self.app_specific_text = app_specific_text
    
    def _render(self, for_user):
      return '%smention <a href="https://twitter.com/dscvrsng">@dscvrsng</a>' % self.app_specific_text
    
    def config_options(self):
      return (ConfigTextValue(name='twitter_name', description='Also, tell us your Twitter name so we know it\'s you: %s', store_as_db_field=True),)
    
    def parse(self, *args, **kwargs):
      return self.parser(*args, **kwargs)
