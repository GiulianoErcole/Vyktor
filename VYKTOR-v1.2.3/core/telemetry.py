import os, sqlite3, time, json
DB_PATH = "results/telemetry.sqlite"
SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, ts_start REAL NOT NULL, ts_end REAL, meta TEXT, summary TEXT);
CREATE TABLE IF NOT EXISTS gens (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER NOT NULL, task TEXT NOT NULL, gen INTEGER NOT NULL, ok_rate REAL NOT NULL, avg_runtime REAL NOT NULL, best_score REAL NOT NULL, ts REAL NOT NULL, FOREIGN KEY(session_id) REFERENCES sessions(id));
"""
def _conn():
    os.makedirs("results", exist_ok=True); return sqlite3.connect(DB_PATH)
def init_db():
    with _conn() as c: c.executescript(SCHEMA)
def start_session(meta=None):
    with _conn() as c:
        cur=c.execute("INSERT INTO sessions (ts_start, meta) VALUES (?,?)",(time.time(), json.dumps(meta or {}))); c.commit(); return cur.lastrowid
def record_generation(session_id, task, gen, ok_rate, avg_runtime, best_score):
    with _conn() as c:
        c.execute("INSERT INTO gens (session_id, task, gen, ok_rate, avg_runtime, best_score, ts) VALUES (?,?,?,?,?,?,?)",
                  (session_id, task, gen, ok_rate, avg_runtime, best_score, time.time())); c.commit()
def end_session(session_id, summary=None):
    with _conn() as c: c.execute("UPDATE sessions SET ts_end=?, summary=? WHERE id=?", (time.time(), json.dumps(summary or {}), session_id)); c.commit()
def recent_sessions(limit=5):
    with _conn() as c: return c.execute("SELECT id, ts_start, ts_end, meta FROM sessions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
