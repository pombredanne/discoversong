__author__ = 'Eugene Efremov'

def make_unique_email(user):
  return '%s@discoversong.com' % user['key']

def generate_playlist_name(existing_names):
  base_name = "discoversong's finds"
  name = base_name
  i = 0
  while name in existing_names:
    i += 1
    name = '%s %i' % (base_name, i)
  return name