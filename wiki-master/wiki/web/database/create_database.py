import sqlite3;


conn = sqlite3.connect('../database.db')
cursor = conn.cursor()

# cursor.execute("DROP TABLE Users")
# cursor.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT, username TEXT, password TEXT)")
# cursor.execute(("INSERT INTO Users('name', 'username', 'password') VALUES('Tommy', 'Tommy', 'Check')"))


query = ("SELECT * FROM Users")
# cursor.execute(query)


# find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
username = 'Tommy'
password = 'Check'
cursor.execute(query)
# cursor.execute(find_user, [(username), (password)])
results = cursor.fetchall()

if results:
    for i in results:
        print(i)
else:
    print("Not in database")

conn.commit()
conn.close()