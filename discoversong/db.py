import os
import web

import config
import urlparse

urlparse.uses_netloc.append('postgres')

def get_db(dbname=config.DB_URL_NAME):
  
  dburl = os.environ[dbname]
  db = urlparse.urlparse(dburl, scheme='postgres')
  
  db = web.database(dburl=dburl,
                    dbn=db.scheme,
                    host=db.hostname,
                    port=db.port,
                    user=db.username,
                    pw=db.password,
                    db=db.path[1:])
  return db

USER_TABLE = 'discodb.discoversong_user'
STATS_TABLE = 'discodb.stats'

MASTER_PROD_DB_URL = 'HEROKU_POSTGRESQL_COBALT_URL'

MASTER_STAGE_DB_URL = 'HEROKU_POSTGRESQL_AMBER_URL'

