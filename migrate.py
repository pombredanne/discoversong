#!/usr/bin/env python
from discoversong import BSONPostgresSerializer

from discoversong.db import get_db

db_from = get_db('HEROKU_SHARED_POSTGRESQL_JADE_URL')
db_to = get_db('HEROKU_POSTGRESQL_COBALT_URL')

for user in db_from.select('discoversong_user', what='id, rdio_user_id, token, secret, address, playlist, prefs'):
  db_to.insert('discodb.discoversong_user',
    id=user['id'],
    rdio_user_id=user['rdio_user_id'],
    address=user['address'],
    token=user['token'],
    secret=user['secret'],
    prefs=BSONPostgresSerializer.from_dict(BSONPostgresSerializer.to_dict(user['prefs'])) if user['prefs'] else BSONPostgresSerializer.from_dict({})
    )
