import sqlite3
import sys
import options

VERSION = "0.0.1"

options = options.get_options(VERSION)

print options

def check_export_table(conn):
    c = conn.cursor()

    sqls = [
        """
            CREATE TABLE IF NOT EXISTS main.message (
                id INTEGER NOT NULL PRIMARY KEY,
                timestamp INTEGER NOT NULL,
                adder TEXT NOT NULL,
                message TEXT,
                UNIQUE (timestamp, adder) ON CONFLICT IGNORE
            )
        """,
        """
            CREATE TABLE IF NOT EXISTS main.contact (
                id INTEGER NOT NULL PRIMARY KEY,
                skypename TEXT,
                fullname TEXT,
                birthday INTEGER,
                gender INTEGER,
                UNIQUE (skypename) ON CONFLICT IGNORE
            )
        """
    ]

    for sql in sqls:
        c.execute(sql)

conn = sqlite3.connect('export.db')

check_export_table(conn)

c = conn.cursor()
for source in options.filename:
    c.execute(""" ATTACH DATABASE "%s" AS source """ % source)

    c.execute(""" INSERT INTO main.contact (skypename, fullname, birthday, gender) SELECT skypename, fullname, birthday, gender FROM source.Contacts ORDER BY skypename """)

    c.execute(""" DETACH DATABASE source """)

conn.close()