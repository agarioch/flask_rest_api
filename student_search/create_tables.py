import sqlite3

from user import UserRegister

connection = sqlite3.connect("data.sqlite")
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS students (id text, name text)"
cursor.execute(create_table)

connection.commit()

connection.close()
