import sqlite3
import json
import os
from datetime import datetime

# Database file location
DB_PATH = "data/fitcoach.db"

def get_connection():
    """
    Create and return a database connection.
    SQLite is built into Python — no installation needed.
    Creates the file automatically if it doesn't exist.
    """
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn

def initialize_database():
    """
    Create all tables if they don't exist yet.
    Run this once when the app starts.
    
    Tables:
    - users         → stores user profiles
    - chat_history  → stores conversation history per user
    - progress      → stores weight/workout logs per user
    - plans         → stores generated plans per user
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     TEXT PRIMARY KEY,
            profile     TEXT NOT NULL,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )
    """)

    # Chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT NOT NULL,
            role        TEXT NOT NULL,
            message     TEXT NOT NULL,
            timestamp   TEXT NOT NULL
        )
    """)

    # Progress tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT NOT NULL,
            date        TEXT NOT NULL,
            weight      REAL,
            workout     TEXT,
            notes       TEXT,
            timestamp   TEXT NOT NULL
        )
    """)

    # Plans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         TEXT NOT NULL,
            plan_type       TEXT NOT NULL,
            plan_content    TEXT NOT NULL,
            created_at      TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")

# ── User functions ─────────────────────────────────────────────────

def save_user_profile(user_id: str, profile: dict):
    """Save or update a user's profile"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO users (user_id, profile, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile = excluded.profile,
            updated_at = excluded.updated_at
    """, (user_id, json.dumps(profile), now, now))

    conn.commit()
    conn.close()

def load_user_profile(user_id: str) -> dict:
    """Load a user's profile, returns None if not found"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT profile FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return json.loads(row["profile"])
    return None

# ── Chat history functions ─────────────────────────────────────────

def save_chat_message(user_id: str, role: str, message: str):
    """Save a single chat message for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (user_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, role, message, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def load_chat_history(user_id: str, limit=20) -> list:
    """
    Load the last N messages for a user.
    limit=20 means last 20 messages — keeps context manageable.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, message, timestamp
        FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()
    conn.close()

    # Reverse so oldest message is first
    messages = [{"role": r["role"], "message": r["message"],
                 "timestamp": r["timestamp"]} for r in reversed(rows)]
    return messages

def clear_chat_history(user_id: str):
    """Clear all chat history for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# ── Progress functions ─────────────────────────────────────────────

def save_progress_entry(user_id: str, weight: float,
                        workout: str, notes: str):
    """Save a progress entry for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO progress (user_id, date, weight, workout, notes, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, datetime.now().strftime("%Y-%m-%d"),
          weight, workout, notes, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def load_progress(user_id: str) -> list:
    """Load all progress entries for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, weight, workout, notes
        FROM progress
        WHERE user_id = ?
        ORDER BY timestamp ASC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{"date": r["date"], "weight": r["weight"],
             "workout": r["workout"], "notes": r["notes"]} for r in rows]

# ── Plans functions ────────────────────────────────────────────────

def save_plan(user_id: str, plan_type: str, plan_content: str):
    """Save a generated plan for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO plans (user_id, plan_type, plan_content, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, plan_type, plan_content, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def load_latest_plan(user_id: str, plan_type: str) -> str:
    """Load the most recent plan of a given type for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT plan_content FROM plans
        WHERE user_id = ? AND plan_type = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id, plan_type))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row["plan_content"]
    return None