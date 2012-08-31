ALTER TABLE discodb.discoversong_user ADD COLUMN first_use date;

UPDATE discodb.discoversong_user SET first_use=current_date();
