import sqlite3
import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ats_database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite database tables for users and scans if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Scans Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            job_domain TEXT NOT NULL,
            resume_filename TEXT NOT NULL,
            scan_date TEXT NOT NULL,
            results_json TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[DATABASE] SQLite Database initialized successfully.")

def create_user(email, password, full_name):
    """Hashes password and inserts a new user record. Returns user dict or None if email exists."""
    email_clean = email.lower().strip()
    password_hash = generate_password_hash(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)",
            (email_clean, password_hash, full_name.strip())
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "email": email_clean, "full_name": full_name.strip()}
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    """Fetches user record by email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    """Fetches user record by user ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT id, email, full_name, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

def verify_user_credentials(email, password):
    """Verifies email and password. Returns user dict if valid, else None."""
    user = get_user_by_email(email)
    if not user:
        return None
    if check_password_hash(user["password_hash"], password):
        return {"id": user["id"], "email": user["email"], "full_name": user["full_name"]}
    return None

def save_user_scan(user_id, score, job_domain, resume_filename, results):
    """Saves a resume scan result to the user's database profile."""
    scan_date = datetime.now().strftime("%B %d, %Y")
    results_json = json.dumps(results)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scans (user_id, score, job_domain, resume_filename, scan_date, results_json) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, score, job_domain, resume_filename, scan_date, results_json)
    )
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return {"id": scan_id, "score": score, "job_domain": job_domain, "scan_date": scan_date}

def get_user_scans(user_id):
    """Fetches all saved scans for a user ordered by date descending."""
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, score, job_domain, resume_filename, scan_date, results_json FROM scans WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    
    scans = []
    for row in rows:
        item = dict(row)
        try:
            item["results"] = json.loads(item["results_json"])
        except Exception:
            item["results"] = {}
        scans.append(item)
    return scans

def delete_user_scan(user_id, scan_id):
    """Deletes a specific scan record belonging to a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE id = ? AND user_id = ?", (scan_id, user_id))
    conn.commit()
    conn.close()
    return True

# Auto-initialize database on import
init_db()
