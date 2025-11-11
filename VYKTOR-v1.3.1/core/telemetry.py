import os, sqlite3, json, time

DB_PATH = os.environ.get("VYKTOR_TELEMETRY_DB", "results/telemetry.sqlite")
SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts_start REAL, ts_end REAL,
  meta TEXT, summary TEXT
);
CREATE TABLE IF NOT EXISTS generations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER,
  task TEXT, gen INTEGER,
  ok_rate REAL, avg_runtime REAL, best_score REAL,
  ts REAL, bandit TEXT
);
"""

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with _conn() as c:
        c.executescript(SCHEMA)

def start_session(meta=None):
    meta = meta or {}
    with _conn() as c:
        c.execute("INSERT INTO sessions (ts_start, meta) VALUES (?,?)",
                  (time.time(), json.dumps(meta)))
        sid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
        c.commit()
        return sid

def record_generation(session_id, task, gen, ok_rate, avg_runtime, best_score, bandit=None):
    with _conn() as c:
        c.execute(
            "INSERT INTO generations (session_id, task, gen, ok_rate, avg_runtime, best_score, ts, bandit) VALUES (?,?,?,?,?,?,?,?)",
            (session_id, task, int(gen), float(ok_rate or 0.0), float(avg_runtime or 0.0), float(best_score or 0.0), time.time(), json.dumps(bandit or {}))
        )
        c.commit()

def end_session(session_id, summary=None):
    with _conn() as c:
        c.execute("UPDATE sessions SET ts_end=?, summary=? WHERE id=?",
                  (time.time(), json.dumps(summary or {}), session_id))
        c.commit()
