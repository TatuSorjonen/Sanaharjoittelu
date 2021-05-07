DROP TABLE estimate;
DROP TABLE test_results;
DROP TABLE words;
DROP TABLE deck;
DROP TABLE dictionary_users;

CREATE TABLE dictionary_users (
	user_id SERIAL PRIMARY KEY,
	username VARCHAR (20) UNIQUE NOT NULL CHECK (username <> ''),
	password VARCHAR (20) NOT NULL CHECK (password <> ''),
	teacher INTEGER NOT NULL
);

CREATE TABLE deck (
        deck_id SERIAL PRIMARY KEY,
        difficulty INTEGER NOT NULL,
        name VARCHAR (20) NOT NULL CHECK (name <> ''),
        user_id INTEGER REFERENCES dictionary_users
);

CREATE TABLE words (
	card_id SERIAL PRIMARY KEY,
	deck_id INTEGER REFERENCES deck NOT NULL,
	word VARCHAR (50) NOT NULL CHECK (word <> ''),
	translation VARCHAR (50) NOT NULL CHECK (translation <> ''),
	UNIQUE (deck_id, word)
);

CREATE TABLE test_results (
	test_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES dictionary_users NOT NULL,
	deck_id INTEGER REFERENCES deck NOT NULL,
	right_answers INTEGER NOT NULL,
	wrong_answers INTEGER NOT NULL
);

CREATE TABLE estimate (
	estimate_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES dictionary_users NOT NULL,
	deck_id INTEGER REFERENCES deck NOT NULL,
	grade INTEGER NOT NULL,
	comment VARCHAR (1000)
);
