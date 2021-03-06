import sqlite3
import sys
import options
import tempfile
import os
import logging

__version__ = "0.0.3"

options = options.get_options(__version__)
app_dir = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO, format='%(levelname)-10s %(asctime)-24s %(message)s')
logging.info('Started with options: ' + str(options))

def check_export_table(c):
    with open(os.path.join(app_dir, 'schema.sql')) as f:
        sqls = f.read().split(';')

    for sql in sqls:
        c.execute(sql)

def export_to_xml(row_set):
    try:
        from lxml.etree import Element, SubElement, tostring
        format = { 'pretty_print': True, 'xml_declaration': True}
    except ImportError:
        from xml.etree.ElementTree import Element, SubElement, tostring
        format = {}

    doc = Element('history')

    chat_id = ''

    for row in row_set:
        if chat_id != row['chatname']:
            chat = SubElement(doc, 'conversation', { 
                'id': row['chatname'], 
                'timestamp': str(row['chattimestamp'])
            })
            chat_id = row['chatname']

        msg = SubElement(chat, 'message')

        SubElement(msg, 'author').text = row['author']
        SubElement(msg, 'timestamp').text = str(row['timestamp'])

        SubElement(msg, 'message').text = row['message'] if row['message'] is not None else ''

    return tostring(doc, encoding="utf-8", **format)

def convert_data(c, files):
    for source in files:
        c.execute(""" ATTACH DATABASE "%s" AS source """ % source)

        c.execute(""" INSERT INTO main.contact (skypename, fullname, birthday, gender) SELECT skypename, fullname, birthday, gender FROM source.Contacts ORDER BY skypename """)
        c.execute(""" INSERT INTO main.chat (name, timestamp, participants) SELECT name, timestamp, participants FROM source.Chats ORDER BY timestamp """)
        c.execute(""" INSERT INTO main.message (chatname, timestamp, author, message) SELECT chatname, timestamp, author, body_xml FROM source.Messages ORDER BY timestamp """)

        c.execute(""" DETACH DATABASE source """)

def prepare_export_rowset(c):
    c.execute(""" CREATE TEMP TABLE ordered_chat (chatname TEXT NOT NULL, chattimestamp INTEGER NOT NULL) """)
    c.execute(""" INSERT INTO ordered_chat SELECT name, timestamp FROM main.chat ORDER BY timestamp """)
    c.execute(""" SELECT * FROM main.message JOIN ordered_chat ON main.message.chatname = ordered_chat.chatname ORDER BY chattimestamp, chatname, timestamp """)

conn = sqlite3.connect(options.destination + '.db')
conn.row_factory = sqlite3.Row

c = conn.cursor()

logging.info('Check export table')
check_export_table(c)

logging.info('Convert data')
convert_data(c, options.filename)

logging.info('Export to XML')
prepare_export_rowset(c)
xml = export_to_xml(c)

with tempfile.NamedTemporaryFile(dir='.', delete=False) as xml_file:
    xml_file.write(xml)

conn.close()

logging.info('Finished')