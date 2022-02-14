import sqlite3

def initUsersDb():
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS users")

    cur.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""")

    con.commit()
    con.close()

def makeUser(username, password):
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    con.commit()
    con.close()

def returnUsers():
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM users")
    elements = cur.fetchall()

    print(elements)
    return elements

def returnOneUser(username):
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM users WHERE username = :user", {"user":username})
    user = cur.fetchone()

    print(user)
    return user


# initUsersDb()
# makeUser("test4", "test4")
# returnUsers()
# returnOneUser("test2aa")