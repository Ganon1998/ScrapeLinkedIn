import sqlite3

# get access to a db file
conn = sqlite3.connect('jobDB.db')
# create cursor object to gain access to methods like commit and execute
cur = conn.cursor()

conn.commit()

try:
    cur.execute('''DROP TABLE JobsTable''')
    conn.commit()
except:
    pass

# create a new table
cur.execute('''CREATE TABLE JobsTable(
Title TEXT,
Company TEXT,
Location TEXT,
Date TEXT);''')

conn.commit()