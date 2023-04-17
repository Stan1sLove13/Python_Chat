CREATE TABLE IF NOT EXISTS user (
	id integer,
	login text NOT NULL UNIQUE,
	email text NOT NULL CHECK("email" LIKE '%___@___%.__%') UNIQUE,
	password text NOT NULL,
	password_recovery_code text UNIQUE,
	PRIMARY KEY(id AUTOINCREMENT)
);