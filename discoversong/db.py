import os
import web

from discoversong.includes import *

def get_db():

  dburl = os.environ['HEROKU_SHARED_POSTGRESQL_JADE_URL'] if os.environ.has_key('HEROKU_SHARED_POSTGRESQL_JADE_URL') else HEROKU_SHARED_POSTGRESQL_JADE_URL
  
  db = web.database(dburl=dburl,
                    dbn='postgres',
                    host='pg60.sharedpg.heroku.com',
                    user='tguaspklkhnrpn',
                    pw='4KBnjLB1n5wbuvzNB4p7DyQEpF',
                    db='vivid_winter_30977')
  return db

