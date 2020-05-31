import sqlite3

connection = sqlite3.connect("data.sqlite")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES (?, ?, ?)"

users = [
    (100, "alistair", "test_001"),
    (101, "marta", "asdf"),
    (102, "anne", "qwer"),
    (103, "claire", "zxcv"),
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
