DROP TABLE words;
DROP TABLE deck;
DROP TABLE dictionary_users;

CREATE TABLE dictionary_users (
	user_id SERIAL PRIMARY KEY,
	username VARCHAR (20) UNIQUE NOT NULL,
	password VARCHAR (20) NOT NULL,
	teacher INTEGER NOT NULL
);

CREATE TABLE deck (
	deck_id SERIAL PRIMARY KEY,
	difficulty INTEGER,
	name VARCHAR (20),
	user_id INTEGER REFERENCES dictionary_users
);

CREATE TABLE words (
	card_id SERIAL PRIMARY KEY,
	word VARCHAR (50) NOT NULL,
	translation VARCHAR (50) NOT NULL,
	deck_id INTEGER REFERENCES deck NOT NULL
);


