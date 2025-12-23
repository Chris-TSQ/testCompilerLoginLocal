import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import sqlite3

# Register adapters for SQLite datetime
sqlite3.register_adapter(datetime, lambda d: d.isoformat())
sqlite3.register_converter("TIMESTAMP", lambda s: datetime.fromisoformat(s.decode()))

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return secrets.token_urlsafe(32)

def create_user(username, email, password):
    password_hash = hash_password(password)
    
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        return True, 'User created successfully'
    except sqlite3.IntegrityError:
        return False, 'Username or email already exists'

def verify_user(username, password):
    password_hash = hash_password(password)
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password_hash = ?',
        (username, password_hash)
    ).fetchone()
    conn.close()
    
    return user

def create_session(user_id):
    token = generate_token()
    expires_at = datetime.now() + timedelta(hours=24)
    
    conn = get_db_connection()
    
    conn.execute(
        'INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)',
        (user_id, token, expires_at)
    )
    
    user = conn.execute(
        'SELECT username FROM users WHERE id = ?',
        (user_id,)
    ).fetchone()
    
    conn.commit()
    conn.close()
    
    return token, user['username']

def delete_session(token):
    conn = get_db_connection()
    conn.execute('DELETE FROM sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()

def verify_session(token):
    conn = get_db_connection()
    
    session = conn.execute(
        'SELECT * FROM sessions WHERE token = ? AND expires_at > ?',
        (token, datetime.now())
    ).fetchone()
    
    if session is None:
        conn.close()
        return None
    
    user = conn.execute(
        'SELECT username, email FROM users WHERE id = ?',
        (session['user_id'],)
    ).fetchone()
    conn.close()
    
    return user