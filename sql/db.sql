DROP TABLE discodb.discoversong_user;

CREATE TABLE discodb.discoversong_user
(
  id serial NOT NULL,
  rdio_user_id integer,
  token text,
  secret text,
  address text,
  prefs bytea,
  CONSTRAINT pk PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
