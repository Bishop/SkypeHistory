CREATE TABLE IF NOT EXISTS main.message (
	id INTEGER NOT NULL PRIMARY KEY,
	chatname TEXT NOT NULL,
	timestamp INTEGER NOT NULL,
	author TEXT NOT NULL,
	message TEXT,
	UNIQUE (chatname, timestamp, author) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS main.chat (
	id INTEGER NOT NULL PRIMARY KEY,
	name TEXT NOT NULL,
	timestamp INTEGER NOT NULL,
	participants TEXT NOT NULL,
	UNIQUE (name) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS main.contact (
	id INTEGER NOT NULL PRIMARY KEY,
	skypename TEXT NOT NULL,
	fullname TEXT,
	birthday INTEGER,
	gender INTEGER,
	UNIQUE (skypename) ON CONFLICT IGNORE
);