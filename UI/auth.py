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
