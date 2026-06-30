"""
HealthFit AI Chatbot — Database Manager

Provides all SQLite CRUD operations for the application.
This module is the only layer that directly interacts with
the SQLite database. All other modules use this interface.

Design Decisions
----------------
- Context manager ensures connections are always closed.
- Parameterized queries prevent SQL injection attacks.
- WAL journal mode enables concurrent reads.
- Tables and indexes are created idempotently on init.
- The instance/ directory is auto-created if missing.

Functions
---------
init_db(db_path)
    Create tables and indexes if they do not exist.
get_connection(db_path)
    Context manager yielding a database connection.
save_chat(db_path, chat_message)
    Insert a chat exchange and return its ID.
save_feedback(db_path, feedback_entry)
    Insert a feedback record.
get_history(db_path, session_id, limit)
    Retrieve chat history for a session.
clear_session(db_path, session_id)
    Delete all chat records for a session.
chat_exists(db_path, chat_id)
    Check whether a chat record exists.
"""

import os
import sqlite3
from contextlib import contextmanager

from models.chat_model import ChatMessage
from models.feedback_model import FeedbackEntry


# ============================================================
# SQL Statements
# ============================================================

_CREATE_CHAT_TABLE = """
CREATE TABLE IF NOT EXISTS chat_history (
    id               INTEGER  PRIMARY KEY AUTOINCREMENT,
    session_id       TEXT     NOT NULL,
    user_message     TEXT     NOT NULL,
    detected_intent  TEXT     NOT NULL,
    confidence_score REAL     DEFAULT 0.0,
    bot_response     TEXT     NOT NULL,
    timestamp        DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_FEEDBACK_TABLE = """
CREATE TABLE IF NOT EXISTS feedback (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    chat_id   INTEGER  NOT NULL,
    rating    INTEGER  NOT NULL CHECK(rating IN (0, 1)),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chat_history(id)
        ON DELETE CASCADE
);
"""

_CREATE_SESSION_PROFILE_TABLE = """
CREATE TABLE IF NOT EXISTS session_profile (
    session_id       TEXT     PRIMARY KEY,
    weight           TEXT,
    height           TEXT,
    age              INTEGER,
    gender           TEXT,
    goal             TEXT,
    activity_level   TEXT,
    water_intake     TEXT,
    updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_CHAT_INDEX = """
CREATE INDEX IF NOT EXISTS idx_chat_session
    ON chat_history(session_id);
"""

_CREATE_FEEDBACK_INDEX = """
CREATE INDEX IF NOT EXISTS idx_feedback_chat
    ON feedback(chat_id);
"""


# ============================================================
# Connection Management
# ============================================================

@contextmanager
def get_connection(db_path: str):
    """Yield a SQLite connection with Row factory enabled.

    The connection is committed on successful exit and
    rolled back on exception. Always closed on exit.

    Parameters
    ----------
    db_path : str
        Absolute path to the SQLite database file, or
        ':memory:' for an in-memory database.

    Yields
    ------
    sqlite3.Connection
        A configured database connection.
    """
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL;")
    connection.execute("PRAGMA foreign_keys=ON;")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# ============================================================
# Initialization
# ============================================================

def init_db(db_path: str) -> None:
    """Create database tables and indexes if they do not exist.

    Also ensures the parent directory (instance/) exists so
    that SQLite can create the database file.

    Parameters
    ----------
    db_path : str
        Absolute path to the SQLite database file.
    """
    # Create the instance/ directory if it does not exist
    if db_path != ":memory:":
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    with get_connection(db_path) as conn:
        conn.execute(_CREATE_CHAT_TABLE)
        conn.execute(_CREATE_FEEDBACK_TABLE)
        conn.execute(_CREATE_SESSION_PROFILE_TABLE)
        conn.execute(_CREATE_CHAT_INDEX)
        conn.execute(_CREATE_FEEDBACK_INDEX)


# ============================================================
# Chat History Operations
# ============================================================

def save_chat(db_path: str, chat_message: ChatMessage) -> int:
    """Insert a chat exchange into the database.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.
    chat_message : ChatMessage
        The chat exchange data to persist.

    Returns
    -------
    int
        The auto-generated primary key of the inserted row.
    """
    sql = """
        INSERT INTO chat_history
            (session_id, user_message, detected_intent,
             confidence_score, bot_response)
        VALUES (?, ?, ?, ?, ?)
    """
    with get_connection(db_path) as conn:
        cursor = conn.execute(sql, (
            chat_message.session_id,
            chat_message.user_message,
            chat_message.detected_intent,
            chat_message.confidence_score,
            chat_message.bot_response,
        ))
        return cursor.lastrowid


def get_history(db_path: str, session_id: str,
                limit: int = 50) -> list[dict]:
    """Retrieve chat history for a specific session.

    Fetches the most recent records up to the limit, returning
    them in chronological (ascending) order.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.
    session_id : str
        The session identifier to filter by.
    limit : int, optional
        Maximum number of records to return (default 50).

    Returns
    -------
    list[dict]
        A list of dictionaries, each representing a chat
        exchange, ordered by timestamp ascending.
    """
    sql = """
        SELECT id, session_id, user_message, detected_intent,
               confidence_score, bot_response, timestamp
        FROM chat_history
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """
    with get_connection(db_path) as conn:
        rows = conn.execute(sql, (session_id, limit)).fetchall()
        result = [dict(row) for row in rows]
        result.reverse()
        return result


def clear_session(db_path: str, session_id: str) -> int:
    """Delete all chat records for a session.

    Feedback records linked to deleted chats are also
    removed automatically via ON DELETE CASCADE.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.
    session_id : str
        The session identifier whose records to delete.

    Returns
    -------
    int
        Number of chat records deleted.
    """
    sql = "DELETE FROM chat_history WHERE session_id = ?"
    with get_connection(db_path) as conn:
        cursor = conn.execute(sql, (session_id,))
        return cursor.rowcount


def chat_exists(db_path: str, chat_id: int) -> bool:
    """Check whether a chat record exists by its primary key.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.
    chat_id : int
        The primary key to look up.

    Returns
    -------
    bool
        True if the record exists, False otherwise.
    """
    sql = "SELECT 1 FROM chat_history WHERE id = ? LIMIT 1"
    with get_connection(db_path) as conn:
        row = conn.execute(sql, (chat_id,)).fetchone()
        return row is not None


# ============================================================
# Feedback Operations
# ============================================================

def save_feedback(db_path: str, feedback: FeedbackEntry) -> int:
    """Insert a feedback record into the database.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.
    feedback : FeedbackEntry
        The feedback data to persist.

    Returns
    -------
    int
        The auto-generated primary key of the inserted row.
    """
    sql = """
        INSERT INTO feedback (chat_id, rating)
        VALUES (?, ?)
    """
    with get_connection(db_path) as conn:
        cursor = conn.execute(sql, (
            feedback.chat_id,
            feedback.rating,
        ))
        return cursor.lastrowid


# ============================================================
# Session Profile Operations
# ============================================================

def save_profile(db_path: str, session_id: str, profile_data: dict) -> None:
    """Insert or update session profile parameters (weight, height, age, gender, goal, activity_level, water_intake)."""
    # Fetch existing profile if any to merge updates
    existing = get_profile(db_path, session_id)
    merged = {
        "weight": profile_data.get("weight") or existing.get("weight"),
        "height": profile_data.get("height") or existing.get("height"),
        "age": profile_data.get("age") if profile_data.get("age") is not None else existing.get("age"),
        "gender": profile_data.get("gender") or existing.get("gender"),
        "goal": profile_data.get("goal") or existing.get("goal"),
        "activity_level": profile_data.get("activity_level") or existing.get("activity_level"),
        "water_intake": profile_data.get("water_intake") or existing.get("water_intake")
    }

    sql = """
        INSERT INTO session_profile 
            (session_id, weight, height, age, gender, goal, activity_level, water_intake, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(session_id) DO UPDATE SET
            weight=excluded.weight,
            height=excluded.height,
            age=excluded.age,
            gender=excluded.gender,
            goal=excluded.goal,
            activity_level=excluded.activity_level,
            water_intake=excluded.water_intake,
            updated_at=CURRENT_TIMESTAMP
    """
    with get_connection(db_path) as conn:
        conn.execute(sql, (
            session_id,
            merged["weight"],
            merged["height"],
            merged["age"],
            merged["gender"],
            merged["goal"],
            merged["activity_level"],
            merged["water_intake"]
        ))


def get_profile(db_path: str, session_id: str) -> dict:
    """Retrieve the session profile data for a session. Returns a dict of profile metrics."""
    sql = """
        SELECT weight, height, age, gender, goal, activity_level, water_intake
        FROM session_profile
        WHERE session_id = ?
    """
    with get_connection(db_path) as conn:
        row = conn.execute(sql, (session_id,)).fetchone()
        if row:
            return dict(row)
        return {
            "weight": None,
            "height": None,
            "age": None,
            "gender": None,
            "goal": None,
            "activity_level": None,
            "water_intake": None
        }


def clear_profile(db_path: str, session_id: str) -> int:
    """Delete session profile data for a session."""
    sql = "DELETE FROM session_profile WHERE session_id = ?"
    with get_connection(db_path) as conn:
        cursor = conn.execute(sql, (session_id,))
        return cursor.rowcount
