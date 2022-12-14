import sqlite3

connection = sqlite3.connect("db.sqlite3")

sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""

# Creating cursor object using connection object
cursor = connection.cursor()

# executing our sql query
cursor.execute(sql_query)
print("List of tables\n")

# printing all tables list
print(cursor.fetchall())
connection.commit()

cursor.execute("""SELECT * FROM watchlist_app_movie;""")
print("watchlist_app_movie\n")

# printing all tables list
print(cursor.fetchall())
connection.commit()

cursor.execute("INSERT INTO watchlist_app_movie VALUES(?, ?, ?, ?)", (2,'fsd','gfd',False,))
connection.commit()

connection.close()
