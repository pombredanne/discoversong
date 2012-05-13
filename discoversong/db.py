import os
import web

import config

def get_db(dbname=config.DB_URL_NAME):
  
  dburl = os.environ[dbname]
  dbn, remainder = dburl.split('://')
  dbuser, dbpw_host, port_dbname = remainder.split(':')
  dbpw, host = dbpw_host.split('@')
  port, db_name = port_dbname.split('/')
  
  db = web.database(dburl=dburl,
                    dbn=dbn,
                    host=host,
                    port=port,
                    user=dbuser,
                    pw=dbpw,
                    db=db_name)
  return db

USER_TABLE = 'discodb.discoversong_user'
STATS_TABLE = 'discodb.stats'

MASTER_PROD_DB_URL = 'HEROKU_POSTGRESQL_COBALT_URL'

MASTER_STAGE_DB_URL = 'HEROKU_POSTGRESQL_AMBER_URL'

