import sqlite3
from flask import g

DATABASE = 'events.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rout TEXT NOT NULL,
                quantity_teams INTEGER NOT NULL,
                teams TEXT NOT NULL
            )
        ''')
        db.commit()

def add_event(name, rout, quantity_teams, teams):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO events (name, rout, quantity_teams, teams) VALUES (?, ?, ?, ?)
    ''', (name, rout, quantity_teams, str(teams)))
    db.commit()

def get_events():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM events')
    rows = cursor.fetchall()
    events = []
    for row in rows:
        event = {
            "id": row['id'],
            "name": row['name'],
            "rout": row['rout'],
            "quantity_teams": row['quantity_teams'],
            "teams": eval(row['teams'])
        }
        events.append(event)
    return events

def delete_event(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    db.commit()