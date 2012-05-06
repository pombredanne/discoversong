import os
import web

import config

def get_db(dbname=config.DB_URL_NAME):
  
  dburl = os.environ[dbname]
  
  dbn, dburl = dburl.split('://')
  
  dbuser, dburl = dburl.split(':')
  
  dbpw, dburl = dburl.split('@')
  
  host, db_name = dburl.split('/')
  
  db = web.database(dburl=dburl,
                    dbn=dbn,
                    host=host,
                    user=dbuser,
                    pw=dbpw,
                    db=db_name)
  return db

USER_TABLE = 'discodb.discoversong_user'

MASTER_PROD_DB_URL = 'HEROKU_POSTGRESQL_COBALT_URL'

MASTER_STAGE_DB_URL = 'HEROKU_POSTGRESQL_AMBER_URL'

