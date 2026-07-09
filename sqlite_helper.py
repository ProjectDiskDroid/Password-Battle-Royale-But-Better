
'''
DEAD SIMPLE SQLITE
We're just gonna use this to store the 3 k/v pairs, representing:
    Rules list -> JSON string of all rules
    Living Users -> JSON string of all living users
    Dead Users -> JSON string of all dead users
This is just for backup in case a problem happens with Vercel so we can keep it real simple
'''

import sqlite3
from pathlib import Path
import json
DB_PATH = Path(__file__).parent / "passwords.db"

def get_connection() -> sqlite3.Connection:
    """Return a connection with Row factory enabled for dict-like row access."""
    conn = sqlite3.connect(DB_PATH, timeout=30)  # wait up to 30s if another process holds a write lock
    conn.row_factory = sqlite3.Row  # access columns by name: row["username"]
    conn.execute("PRAGMA foreign_keys = ON")  # enforce FK constraints
    conn.execute("PRAGMA journal_mode = WAL")   # WAL lets reads happen during writes (better for multiple threads accessing this)
    return conn

# ---------------------------------------------------------------------------
# Table creation
# ---------------------------------------------------------------------------

def create_tables() -> None:
    """Create all tables if they don't already exist."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS passwords (
                key         TEXT PRIMARY KEY,
                value       TEXT NOT NULL,
                updated_at DATETIME DEFAULT (datetime('now'))
            );

        """)
    print("Tables created (or already exist).")

def save_to_db(key: str, value: str) -> None:
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO passwords (key, value, updated_at) VALUES (?, ?, datetime('now'))",
                (key, value),
            )
    finally:
        conn.close()

# An sqlite3.Row is a special object, it behaves like a dictionary
# e.g.
#       row = get_user_by_id(1)
#       row["username"]   # access by column name  -> "Alice"
#       row["score"]      # access by column name  -> 180
#       row[0]            # access by position     -> 1  (the id)
# If you want to convert this into a regular dict, e.g. you want to put it into json or hand off the data somewhere etc, then just do:
#       dict(row)         # convert to plain dict  -> {"id": 1, "username": "Alice", ...}

def get_all_values() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM passwords").fetchall()

# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

def reset_all() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM passwords")

# Only use for testing
def drop_all_tables() -> None:
    """Destroy all tables — useful for resetting during development."""
    with get_connection() as conn:
        conn.executescript("""
            DROP TABLE IF EXISTS passwords;
        """)
    print("All tables dropped.")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Start fresh for the demo
    drop_all_tables()
    create_tables()

    # Mock Data
    rules = ["Must include a Pokemon", "Must contain at least 9 characters", "Include the last name of a US President"]
    # List of users with valid passwords, in order of when they were received (we'll sort it by password length before sending to server)
    living_users = [
        {'username': 'DougDoug3000', 'password': 'asdjajbsdk', 'submission_timestamp': '7:12pm 15sec 20ms' },
        {'username': 'omgjerry', 'password': 'dooomsmsm', 'submission_timestamp': '7:12pm 16sec 40ms' },
        {'username': 'katherin2000', 'password': 'twt232321s', 'submission_timestamp': '7:12pm 16sec 70ms' },
        {'username': 'jambalan', 'password': 'san53gomoon', 'submission_timestamp': '7:12pm 23sec 10ms' },
    ]
    # List of dead users, plus the reason why they died, ordered by the time they submitted
    dead_users = [
        {'username': 'toddhoward2', 'password': 'asdjajbsdk', 'submission_timestamp': '7:12pm 15sec 20ms', 'failure_message': 'Heres why you failed...'},
        {'username': 'BigBoyBen', 'password': 'dooomsmsm', 'submission_timestamp': '7:12pm 16sec 40ms', 'failure_message': 'Heres why you failed...'},
        {'username': 'flatpancake99', 'password': 'twt232321s', 'submission_timestamp': '7:12pm 16sec 70ms', 'failure_message': 'Heres why you failed...'},
        {'username': 'BigDumbIdiot', 'password': 'san53gomoon', 'submission_timestamp': '7:12pm 23sec 10ms', 'failure_message': 'Heres why you failed...'},
    ]

    # --- INSERT ---
    rules_id = save_to_db("rules", json.dumps(rules))
    living_users_id = save_to_db("living_users", json.dumps(living_users))
    dead_users_id = save_to_db("dead_users", json.dumps(dead_users))
    print(f"\nInserted users.")
    
    # --- UPDATE EXISTING KEY ---
    save_to_db("rules", json.dumps(["this is an updated rule", "and a second updated rule"]))

    # --- SELECT ---
    all_values = get_all_values()

    # Now you can grab each row and do stuff with it
    # If you json.dumped a data structure into the db, you'll need to json.loads() that back into a proper python data structure (otherwise its just a json string)
    for row in all_values:
        raw_string = row["value"]              # This is a JSON string, e.g. '["Must include a Pokemon", ...]'
        parsed = json.loads(raw_string)         # Now it's a real Python list/dict again
        print(f'\n{row["key"]}:')


