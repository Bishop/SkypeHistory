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
                chatname TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                author TEXT NOT NULL,
                message TEXT,
                UNIQUE (chatname, timestamp, author) ON CONFLICT IGNORE
            )
        """,
        """
            CREATE TABLE IF NOT EXISTS main.chat (
                id INTEGER NOT NULL PRIMARY KEY,
                name TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                participants TEXT NOT NULL,
                UNIQUE (name) ON CONFLICT IGNORE
            )
        """,
        """
            CREATE TABLE IF NOT EXISTS main.contact (
                id INTEGER NOT NULL PRIMARY KEY,
                skypename TEXT NOT NULL,
                fullname TEXT,
                birthday INTEGER,
                gender INTEGER,
                UNIQUE (skypename) ON CONFLICT IGNORE
            )
        """
    ]

    for sql in sqls:
        c.execute(sql)

def export_to_xml(cursor):
    from xml.dom.minidom import Document
    
    cursor.execute(""" SELECT * FROM main.message ORDER BY chatname, timestamp """)
    
    doc = Document()

    h = doc.createElement("history")
    doc.appendChild(h)

    conversation = doc.createElement("conversation")
    conversation.setAttribute("id", "main")
    h.appendChild(conversation)
    
    return doc.toprettyxml(indent="\t")

        
conn = sqlite3.connect('export.db')

check_export_table(conn)

c = conn.cursor()
for source in options.filename:
    c.execute(""" ATTACH DATABASE "%s" AS source """ % source)

    c.execute(""" INSERT INTO main.contact (skypename, fullname, birthday, gender) SELECT skypename, fullname, birthday, gender FROM source.Contacts ORDER BY skypename """)
    c.execute(""" INSERT INTO main.chat (name, timestamp, participants) SELECT name, timestamp, participants FROM source.Chats ORDER BY timestamp """)
    c.execute(""" INSERT INTO main.message (chatname, timestamp, author, message) SELECT chatname, timestamp, author, body_xml FROM source.Messages ORDER BY timestamp """)

    c.execute(""" DETACH DATABASE source """)


    
conn.close()