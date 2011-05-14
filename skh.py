import sqlite3
import sys
import options

VERSION = "0.0.1"

options = options.get_options(VERSION)

print options

def check_export_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message (date INTEGER, message TEXT, author TEXT)
    """)

    conn.commit()

conn = sqlite3.connect('skh.db')

check_export_table(conn)


conn.close()