import os
import web

import config

def get_db(dbname=config.DB_URL_NAME):
  
  print 'get_db', dbname
  
  dburl = os.environ[dbname]
  
  print 'dburl', dburl
  
  dbn, dburl = dburl.split('://')
  
  print 'dbn', dbn, 'dburl', dburl
  
  dbuser, dbpw_host, port_etc = dburl.split(':')
  
  print 'dbuser', dbuser, 'dbpw_host', dbpw_host, 'port_etc', port_etc
  
  dbpw, host = dbpw_host.split('@')
  
  print 'dbpw', dbpw, 'host', host
  
  port, db_name = port_etc.split('/')
  
  print 'port', port, 'db_name', db_name
  
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

