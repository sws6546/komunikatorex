from ast import excepthandler
import sqlite3

def initMessagesDb():
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS messages")

    cur.execute("""CREATE TABLE messages (
        id_messages INTEGER PRIMARY KEY AUTOINCREMENT,
        user_from TEXT NOT NULL,
        user_to TEXT NOT NULL,
        text_messages TEXT NOT NULL
    )""")

    con.commit()
    con.close()

def addMessage(user_from, user_to, text_messages):
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("INSERT INTO messages (user_from, user_to, text_messages) VALUES (?, ?, ?)", (user_from, user_to, text_messages))

    con.commit()
    con.close()

def getUserMessages(from_user, to_user):
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM messages WHERE user_from = :user_from AND user_to = :user_to", {"user_from": from_user, "user_to": to_user})
    messages_from_user = cur.fetchall()

    cur.execute("SELECT * FROM messages WHERE user_from = :user_from AND user_to = :user_to", {"user_from": to_user, "user_to": from_user})
    messages_to_user = cur.fetchall()

    messages = messages_from_user + messages_to_user

    messages = sorted(messages, key=lambda x: x[0])

    for message in messages:
        if message[1] == from_user:
            i = [message, "aqua"]
            messages[messages.index(message)] = i
        else:
            i = [message, "red"]
            messages[messages.index(message)] = i

    print(messages)
    return messages

def returnAllMessages():
    con = sqlite3.connect("baza.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM messages")

    print(cur.fetchall())

# initMessagesDb()
# addMessage("bartosz", "szymon", "do szymona")
# addMessage("szymon", "bartosz", "od szymona")
# getUserMessages("test1", "test2")
# returnAllMessages()