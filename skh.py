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

def export_to_xml(cursor):
    from xml.dom.minidom import Document
    doc = Document()
    
    def text_node(name, value):
        node = doc.createElement(name)
        node.appendChild(doc.createTextNode(value))
        return node
        
    cursor.execute(""" SELECT * FROM main.message ORDER BY chatname, timestamp """)
    
    h = doc.createElement("history")
    doc.appendChild(h)
    
    conversation_id = ''
    
    for row in cursor:
        if conversation_id != row['chatname']:
            conversation = doc.createElement("conversation")
            conversation.setAttribute("id", row['chatname'])
            h.appendChild(conversation)
            conversation_id = row['chatname']
        
        m = doc.createElement("message")
        
        m.appendChild(text_node("author", row['author']))
        m.appendChild(text_node("date", str(row['timestamp'])))
        
        if row['message'] is not None:
            m.appendChild(text_node("text", row['message']))
            
        conversation.appendChild(m)
    
    return doc.toprettyxml(indent="\t")

def convert_data(c, files):
    for source in files:
        c.execute(""" ATTACH DATABASE "%s" AS source """ % source)

        c.execute(""" INSERT INTO main.contact (skypename, fullname, birthday, gender) SELECT skypename, fullname, birthday, gender FROM source.Contacts ORDER BY skypename """)
        c.execute(""" INSERT INTO main.chat (name, timestamp, participants) SELECT name, timestamp, participants FROM source.Chats ORDER BY timestamp """)
        c.execute(""" INSERT INTO main.message (chatname, timestamp, author, message) SELECT chatname, timestamp, author, body_xml FROM source.Messages ORDER BY timestamp """)

        c.execute(""" DETACH DATABASE source """)
    
conn = sqlite3.connect(options.destination + '.db')
conn.row_factory = sqlite3.Row

c = conn.cursor()

logging.info('Check export table')
check_export_table(c)

logging.info('Convert data')
convert_data(c, options.filename)

logging.info('Export to XML')
xml = export_to_xml(c)

with tempfile.NamedTemporaryFile(dir='.', delete=False) as xml_file:
    xml_file.write(xml.encode('utf-8'))

conn.close()

logging.info('Finished')