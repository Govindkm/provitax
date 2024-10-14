# auth.py

import sqlite3
import hashlib

# Function to connect to the database and create user table
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    # Create users table if it doesn't exist, adding role field
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            email TEXT,
            full_name TEXT,
            role TEXT
        )
    """)
    
    # Create chat_history table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            chat_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(username)
        )
    """)
    
    conn.commit()
    conn.close()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a new user with a specified role
def add_user(username, password, email, full_name, role):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, email, full_name, role) VALUES (?, ?, ?, ?, ?)", 
              (username, hash_password(password), email, full_name, role))
    conn.commit()
    conn.close()

# Function to validate login and get the user role
def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Function to check if a username already exists
def user_exists(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Function to add chat history for a user
def add_chat_history(username, chat_data):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_id, chat_data) VALUES (?, ?)", (username, chat_data))
    conn.commit()
    conn.close()   

# Function to update chat history for a user
def update_chat_history(chat_id, chat_data):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE chat_history SET chat_data=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (chat_data, chat_id))
    conn.commit()
    conn.close()
    
# Function to get chat history for a user
def get_chat_history(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT id, chat_data, created_at, updated_at FROM chat_history WHERE user_id=?", (username,))
    result = c.fetchall()
    conn.close()
    return result

# Function to get chat history by chat id
def get_chat_by_id(chat_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT chat_data FROM chat_history WHERE id=?", (chat_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None