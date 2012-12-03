DROP TABLE discodb.discoversong_user;

CREATE TABLE discodb.discoversong_user
(
  id serial NOT NULL,
  rdio_user_id integer,
  token text,
  secret text,
  address text,
  prefs bytea,
  emails bigint,
  searches bigint,
  songs bigint,
  last_use date,
  CONSTRAINT pk PRIMARY KEY (id )
);

CREATE TABLE discodb.stats
(
  emails bigint,
  searches bigint,
  songs bigint,
  visits bigint,
  last_read_mention text
);
