import os
import web

import config

def get_db(dbname=config.DB_URL_NAME):
  print 'get_db', dbname
  dburl = os.environ[dbname]
  print dburl
  dbn, dburl = dburl.split('://')
  print dbn, dburl
  dbuser, dburl, port_etc = dburl.split(':')
  print dbuser, dburl, port_etc
  dburl = dburl + ':' + port_etc
  print dburl
  dbpw, dburl = dburl.split('@')
  print dbpw, dburl
  host, db_name = dburl.split('/')
  print host, db_name
  db = web.database(dburl=dburl,
                    dbn=dbn,
                    host=host,
                    user=dbuser,
                    pw=dbpw,
                    db=db_name)
  return db

USER_TABLE = 'discodb.discoversong_user'
STATS_TABLE = 'discodb.stats'

MASTER_PROD_DB_URL = 'HEROKU_POSTGRESQL_COBALT_URL'

MASTER_STAGE_DB_URL = 'HEROKU_POSTGRESQL_AMBER_URL'

