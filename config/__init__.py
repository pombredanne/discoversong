import os

ENVIRONMENT = os.environ['DISCOSONG_ENVIRONMENT'] if os.environ.has_key('DISCOSONG_ENVIRONMENT') else 'localhost'

RDIO_CONSUMER_KEY = 'mkmkjz9d7jakc5uwhcy8n6ae'
RDIO_CONSUMER_SECRET = 'SB3YVT7Hjd'

#import overrides
if ENVIRONMENT == 'staging':
  from config.staging import *
elif ENVIRONMENT == 'production':
  from config.production import *
elif ENVIRONMENT == 'localhost':
  from config.localhost import *

ADMIN_USERS = [103]
