from discoversong.db import get_db, USER_TABLE, STATS_TABLE

def got_email(user_id):
  db = get_db()
  t = db.transaction()
  db.query('UPDATE %s SET emails = emails + 1, last_use = current_date WHERE rdio_user_id = %i' % (USER_TABLE, user_id))
  db.query('UPDATE %s SET emails = emails + 1' % STATS_TABLE)
  t.commit()

def made_search(user_id):
  db = get_db()
  t = db.transaction()
  db.query('UPDATE %s SET searches = searches + 1 WHERE rdio_user_id = %i' % (USER_TABLE, user_id))
  db.query('UPDATE %s SET searches = searches + 1' % STATS_TABLE)
  t.commit()

def found_songs(user_id, songs):
  db = get_db()
  t = db.transaction()
  db.query('UPDATE %s SET songs = songs + %i WHERE rdio_user_id = %i' % (USER_TABLE, songs, user_id))
  db.query('UPDATE %s SET songs = songs + %i' % (STATS_TABLE, songs))
  t.commit()

def visited(user_id):
  db = get_db()
  t = db.transaction()
  db.query('UPDATE %s SET last_use = current_date WHERE rdio_user_id = %i' % (USER_TABLE, user_id))
  db.query('UPDATE %s SET visits = visits + 1' % STATS_TABLE)
  t.commit()
