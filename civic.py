import sqlite3
import os
from datetime import datetime

# -------------------------------
# FOLDERS
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_FOLDER = os.path.join(BASE_DIR, "database")
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "civic.db")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")


# -------------------------------
# DATABASE CONNECTION
# -------------------------------

def connect():
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    return sqlite3.connect(DATABASE_FILE)


# -------------------------------
# CREATE / UPDATE DATABASE
# -------------------------------

def init_db():

    conn = connect()
    cursor = conn.cursor()

    # ---------------------------
    # USERS TABLE
    # ---------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT
        )
    """)

    # ---------------------------
    # COMPLAINTS TABLE
    # ---------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            citizen_name TEXT,
            citizen_phone TEXT,
            description TEXT,
            location TEXT,
            latitude TEXT,
            longitude TEXT,
            image_path TEXT,
            category TEXT,
            priority TEXT,
            department TEXT,
            language TEXT,
            status TEXT,
            assigned_officer TEXT,
            assigned_worker TEXT,
            ai_report TEXT,
            confidence REAL,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    # ---------------------------
    # AUTOMATICALLY ADD MISSING
    # COLUMNS TO OLD DATABASE
    # ---------------------------

    cursor.execute("PRAGMA table_info(complaints)")
    existing_columns = [row[1] for row in cursor.fetchall()]

    required_columns = {
        "citizen_phone": "TEXT",
        "description": "TEXT",
        "location": "TEXT",
        "latitude": "TEXT",
        "longitude": "TEXT",
        "image_path": "TEXT",
        "category": "TEXT",
        "priority": "TEXT",
        "department": "TEXT",
        "language": "TEXT",
        "status": "TEXT",
        "assigned_officer": "TEXT",
        "assigned_worker": "TEXT",
        "ai_report": "TEXT",
        "confidence": "REAL",
        "created_at": "TEXT",
        "updated_at": "TEXT"
    }

    for column, datatype in required_columns.items():

        if column not in existing_columns:

            cursor.execute(
                f"ALTER TABLE complaints ADD COLUMN {column} {datatype}"
            )

    # ---------------------------
    # FEEDBACK TABLE
    # ---------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT,
            rating INTEGER,
            feedback TEXT,
            created_at TEXT
        )
    """)

    # ---------------------------
    # AUDIT LOG TABLE
    # ---------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT,
            actor TEXT,
            action TEXT,
            created_at TEXT
        )
    """)

    # ---------------------------
    # DEFAULT USERS
    # ---------------------------

    users = [
        (
            "citizen",
            "1234",
            "Citizen",
            ""
        ),
        (
            "officer",
            "1234",
            "Officer",
            "Public Works Department"
        ),
        (
            "worker",
            "1234",
            "Worker",
            ""
        ),
        (
            "admin",
            "admin123",
            "Admin",
            ""
        )
    ]

    for user in users:

        cursor.execute(
            """
            INSERT OR IGNORE INTO users
            (username, password, role, department)
            VALUES (?, ?, ?, ?)
            """,
            user
        )

    conn.commit()
    conn.close()


# -------------------------------
# ADD AUDIT LOG
# -------------------------------

def log_action(complaint_id, actor, action):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs
        (
            complaint_id,
            actor,
            action,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            complaint_id,
            actor,
            action,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()