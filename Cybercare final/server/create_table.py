import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS articles (name text PRIMARY KEY, objet text, auteur text, date de publication text, contenu text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS events (name text PRIMARY KEY, date text, lieu text, objet text)"
cursor.execute(create_table)


connection.commit()

connection.close()