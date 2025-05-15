
import sqlite3

conn = sqlite3.connect("events.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT,
    time_options TEXT,
    message_id INTEGER,
    chat_id INTEGER
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS votes (
    event_id INTEGER,
    user_id INTEGER,
    choice TEXT,
    PRIMARY KEY (event_id, user_id)
)""")

conn.commit()

def add_event(title, options, message_id, chat_id):
    cur.execute("INSERT INTO events (title, time_options, message_id, chat_id) VALUES (?, ?, ?, ?)",
                (title, "\n".join(options), message_id, chat_id))
    conn.commit()
    return cur.lastrowid

def get_event(event_id):
    cur.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    return cur.fetchone()

def save_vote(event_id, user_id, choice):
    cur.execute("REPLACE INTO votes (event_id, user_id, choice) VALUES (?, ?, ?)", (event_id, user_id, choice))
    conn.commit()

def get_votes(event_id):
    cur.execute("SELECT choice, COUNT(*) FROM votes WHERE event_id = ? GROUP BY choice", (event_id,))
    return cur.fetchall()
